from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Verification, Property
from App.libs import PyCatastro
from App.mailer import Mailer
from App.forms import UserForm, PropertyForm
from App.decorators import verification_required
from App.catastro import * 

class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class UserCreate(CreateView):
    model= User
    template_name = 'user_create.html'
    fields = ['first_name', 'last_name', 'password', 'username', 'email']


class CreateUser(View):
    def post(self, request):
        fields = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'username': request.POST.get('username', ''),
            'password': request.POST.get('password', ''),
            'email': request.POST.get('email', '')
        }
        fields['form'] = UserForm()
        try:
            if User.objects.filter(email = fields['email']).count() != 0:
                fields['email_errors'] = ['El email está siendo usado por otro usuario']
                return render(request, UserCreate().template_name, context = fields)
            else:
                validate_password(fields['password'])
                user = User.objects.create_user(fields['username'], fields['email'], fields['password'])
                user.first_name = fields['first_name']
                user.last_name = fields['last_name']
                user.save()
                Verification.objects.create(user = user, email_verification_token = get_random_string(length = 32))
                Mailer.send_email_verification_mail(user)
                return render(request, 'user_created.html')
        except ValidationError as validation_errors:
            fields['password_errors'] = validation_errors
            return render(request, UserCreate().template_name, context = fields)
        except IntegrityError:
            fields['username_errors'] = ['El nombre de usuario está siendo usado por otro usuario']
            return render(request, UserCreate().template_name, context = fields)


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class LoggedIn(View):
    def get(self, request):
        return render(request, 'logged_in.html')


class LoggedOut(View):
    def get(self, request):
        return render(request, 'logged_out.html')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class UserProfile(View):
    def get(self, request):
        properties = Property.objects.filter(user = request.user.id)
        return render(request, 'user_profile.html', context = {'properties': properties})


@method_decorator(login_required, name = 'dispatch')
class UserUpdate(UpdateView):
    model = User
    template_name = 'user_update.html'
    fields = ['first_name','last_name']
    success_url = reverse_lazy('user_profile')


@method_decorator(login_required, name = 'dispatch')
class UserDelete(DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user_deleted')


class UserDeleted(View):
    def get(self, request):
        return render(request, 'user_deleted.html')


class PasswordResetRequest(View):
    def post(self, request):
        try:
            user = User.objects.get(email = request.POST.get('email', ''))
            if user.verification.password_reset_token is None:
                user.verification.generate_password_reset_token()
            Mailer.send_reset_password_mail(user)
        except ObjectDoesNotExist:
            print('El email no corresponde a ningún usuario.')
        finally:
            return redirect('password_reset_done')


class PasswordResetConfirm(View):
    template_name = 'password_reset_confirm.html'

    def get(self, request, token = None):
        if Verification.objects.filter(password_reset_token = token).count() == 0:
            print('El token no corresponde a ningún usuario.')
            validlink = False
            user_id = 0
        else:
            validlink = True
            user_id = Verification.objects.get(password_reset_token = token).user.id
        return render(request, self.template_name, context = {'validlink': validlink, 'user_id': user_id})

    def post(self, request, token = None):
        new_password = request.POST.get('new_password', '')
        user_id = request.POST.get('user_id', 0)
        try:
            validate_password(new_password)
            user = User.objects.get(id = user_id)
            user.set_password(new_password)
            user.save()
            user.verification.password_reset_successfully()
            return redirect('password_reset_complete')
        except ValidationError as validation_errors:
            password_errors = validation_errors
            return render(request, self.template_name, context = {'validlink': True, 'new_password': new_password, 'user_id': user_id, 'password_errors': password_errors})


@method_decorator(login_required, name = 'dispatch')
class UserUnverified(View):
    def get(self, request):
        return render(request, 'user_unverified.html')


class EmailVerificationRequest(View):
    def get(self, request):
        return render(request, 'email_verification_request.html')

    def post(self, request):
        email = request.POST.get('email', '')
        redirect_to = 'email_verification_requested'
        if User.objects.filter(email = email).count() == 0:
            print('El email no corresponde a ningún usuario.')
        else:
            user = User.objects.get(email = email)
            if user.verification.email_verified:
                redirect_to = 'email_verified'
            elif user.verification.email_verification_token is None:
                user.verification.generate_email_verification_token()
                Mailer.send_email_verification_mail(user)

        return redirect(redirect_to)


class EmailVerificationRequested(View):
    def get(self, request):
        return render(request, 'email_verification_requested.html')


@method_decorator(login_required, name = 'dispatch')
class EmailUpdateRequest(View):
    def get(self, request):
        return render(request, 'email_update_request.html')

    def post(self, request):
        new_email = request.POST.get('email', '')
        try:
            user = User.objects.get(email = new_email)
            return render(request, 'email_update_request.html', context = {'email': new_email, 'errors': ['Este email ya pertenece a otro usuario']})
        except ObjectDoesNotExist:
            user = request.user
            user.verification.email_update_to = new_email
            user.verification.save()
            if user.verification.email_verification_token is None:
                user.verification.generate_email_verification_token()
            Mailer.send_email_update_mail(user, new_email)
            return redirect('email_update_requested')


class EmailUpdateRequested(View):
    def get(self, request):
        return render(request, 'email_update_requested.html')


class VerifyEmail(View):
    def get(self, request, token = None):
        if Verification.objects.filter(email_verification_token = token).count() == 0:
            print('El email no corresponde a ningún usuario.')
            return render(request, 'email_verification_error.html')
        else:
            user = Verification.objects.get(email_verification_token = token).user
            if user.verification.email_update_to is not None:
                user.verification.email_updated_successfully()
            else:
                user.verification.email_verified_successfully()
            return redirect('email_verified')


class EmailVerified(View):
    def get(self, request):
        return render(request, 'email_verified.html')


class Catastro(View):

    def get(self, request):
        latitude = request.GET.get('latitude', '')
        longitude = request.GET.get('longitude', '')
        res = PyCatastro.Consulta_RCCOOR('EPSG:4258', longitude, latitude)
        if res['consulta_coordenadas']['control']['cucoor'] == '1':
            address = res['consulta_coordenadas']['coordenadas']['coord']['ldt']
            catastral_reference = res['consulta_coordenadas']['coordenadas']['coord']['pc']['pc1'] + res['consulta_coordenadas']['coordenadas']['coord']['pc']['pc2']
            if Property.objects.filter(catastral_reference = catastral_reference, verified = True).count() != 0:
                property = Property.objects.get(catastral_reference = catastral_reference, verified = True)
            else:
                property = None
            print("Referencia catastral:", catastral_reference)
            print("Direccion:", address)
            prov = extractProv(address)
            print(prov)
            mun = extractMun(address)
            print(mun)
            inm = PyCatastro.Consulta_DNPRC_Codigos(prov, mun, catastral_reference)
            print("inmueble:", inm)
            cla = sayCla(inm)
            print("Clase", cla)
            us = sayUs(inm)
            print("Uso", us)
            typ = proTyp(inm, us)
            floor = proFloor(inm, us)
            mez = mix(typ,floor)
            print("Datos:", mez)
            return render(request, 'catastro_found.html', context = {'address': address, 
            'catastral_reference': catastral_reference, 'cla' : cla, 'us' : us,
            'mez' : mez, 'property': property})
        
        elif res['consulta_coordenadas']['control']['cuerr'] == '1':
            mensaje = res['consulta_coordenadas']['lerr']['err']['des']
            return render(request, 'catastro_not_found.html', context = {'mensaje': mensaje})
        
        else:
            return render(request, 'catastro_error.html',)



@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyCreate(CreateView):
    model= Property
    template_name = 'property_create.html'
    fields = ['catastral_reference', 'price']


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class CreateProperty(View):
    def post(self, request):
        fields = {
            'catastral_reference': request.POST.get('catastral_reference', ''),
            'price': request.POST.get('price', ''),
        }
        fields['form'] = PropertyForm()
        if Property.objects.filter(catastral_reference = fields['catastral_reference']).count() != 0:
            fields['catastral_reference_errors'] = ['La referencia catastral ya ha sido introducida por otro usuario']
            return render(request, PropertyCreate().template_name, context = fields)
        else:
            new_property = Property.objects.create(catastral_reference = fields['catastral_reference'], price = fields['price'], user = request.user)
            Mailer.send_email_create_property(new_property)
            return render(request, 'property_created.html')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyDelete(DeleteView):
    model = Property
    template_name = 'property_delete.html'
    success_url = reverse_lazy('property_deleted')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyDeleted(View):
    def get(self, request):
        return render(request, 'property_deleted.html')


@method_decorator(login_required, name = 'dispatch')
class UnverifiedProperties(View):
    def get(self, request):
        properties = Property.objects.filter(verified = False)
        return render(request, 'unverified_properties.html', context = {'properties': properties})


@method_decorator(login_required, name = 'dispatch')
class VerifyProperty(View):
    def post(self, request):
        property_id = request.POST.get('property_id', 0)
        property = Property.objects.get(id = property_id)
        property.verify()
        return redirect('property_verified')


@method_decorator(login_required, name = 'dispatch')
class PropertyVerified(View):
    def get(self, request):
        return render(request, 'property_verified.html')


@method_decorator(login_required, name = 'dispatch')
class PropertyContact(View):
    def get(self, request, catastral_reference = None):
        property = Property.objects.get(catastral_reference = catastral_reference)
        return render(request, 'property_contact.html', context = {'property': property})

    def post(self, request, catastral_reference = None):
        property_id = request.POST.get('property_id', 0)
        property = Property.objects.get(id = property_id)
        message = request.POST.get('message', '')
        Mailer.send_email_property_contact(request.user, property, message)
        return redirect('property_contacted')


@method_decorator(login_required, name = 'dispatch')
class PropertyContacted(View):
    def get(self, request):
        return render(request, 'property_contacted.html')
