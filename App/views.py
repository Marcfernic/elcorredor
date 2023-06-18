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
class LoggedIn(View):
    def get(self, request):
        return render(request, 'logged_in.html')


class LoggedOut(View):
    def get(self, request):
        return render(request, 'logged_out.html')


@method_decorator(login_required, name = 'dispatch')
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

@method_decorator(login_required, name = 'dispatch')
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

@method_decorator(login_required, name = 'dispatch')
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

@method_decorator(login_required, name = 'dispatch')
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

@method_decorator(verification_required, name = 'dispatch')
class EmailVerified(View):
    def get(self, request):
        return render(request, 'email_verified.html')


class Catastro(View):

    def get(self, request):
        try:
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
                print(latitude, longitude)
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
                print("Tipos:", typ)
                floor = proFloor(inm, us)
                print("Superficie:", floor)
                mez = mix(typ,floor)
                print("Datos:", mez)
                print(address)

                #if (address != None and address != "") and (catastral_reference != None and catastral_reference != "") and 
                #(address != None and address != "") and (catastral_reference != None and catastral_reference != ""):

                return render(request, 'catastro_found.html', context = {'address': address, 'longitude' : longitude,
                'catastral_reference': catastral_reference, 'cla' : cla, 'us' : us, 'latitude': latitude, 'mez' : mez,
                'provincie': prov, 'municipality': mun,'property': property})
            
            elif res['consulta_coordenadas']['control']['cuerr'] == '1':
                mensaje = res['consulta_coordenadas']['lerr']['err']['des']
                return render(request, 'catastro_not_found.html', context = {'mensaje': mensaje})
            
            else:
                return render(request, 'catastro_error.html',)
        except:
            return render(request, 'catastro_error.html',)



@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyCreate(View):
    
    def get(self, request):

        latitude = request.GET.get('latitude', '')
        longitude = request.GET.get('longitude', '')
        catastral_reference = request.GET.get('catastral_reference', '')
        provincie = request.GET.get('provincie', '')
        municipality = request.GET.get('municipality', '')
        address = request.GET.get('address', '')
        price = request.GET.get('price', '')
        
        template_name = 'property_create.html'
        
        context = {'catastral_reference' : catastral_reference, 'latitude' : latitude, 'longitude' : longitude, 
        'provincie' : provincie, 'municipality' : municipality, 'address' : address, 'price' : price}
        
        return render(request, template_name, context)




@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class CreateProperty(View):
    def post(self, request):
        fields = {
            'catastral_reference': request.POST.get('catastral_reference', ''),
            'price': request.POST.get('price', ''),
            'latitude' : request.POST.get('latitude', ),
            'longitude' : request.POST.get('longitude', ),
            'provincie' : request.POST.get('provincie', ),
            'municipality' : request.POST.get('municipality', ),
            'address' : request.POST.get('address', )
        }
        fields['form'] = PropertyForm()
        
        if Property.objects.filter(catastral_reference = fields['catastral_reference']).count() != 0:
            fields['catastral_reference_errors'] = ['La referencia catastral ya ha sido introducida por otro usuario']
            return render(request, 'property_create.html', context = fields)
        else:
            new_property = Property.objects.create(catastral_reference = fields['catastral_reference'], 
                price = fields['price'], user = request.user, address = fields['address'],
                latitude = fields['latitude'], longitude = fields['longitude'], 
                provincie = fields['provincie'], municipality = fields['municipality'])
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
@method_decorator(verification_required, name = 'dispatch')
class UnverifiedProperties(View):
    def get(self, request):
        properties = Property.objects.filter(verified = False)
        return render(request, 'unverified_properties.html', context = {'properties': properties})


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class VerifyProperty(View):
    def post(self, request):
        property_id = request.POST.get('property_id', 0)
        property = Property.objects.get(id = property_id)
        property.verify()
        return redirect('property_verified')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class UnverifyProperty(View):
    def post(self, request):
        property_id = request.POST.get('property_id', 0)
        property = Property.objects.get(id = property_id)
        property.unverify()
        return redirect('property_unverified')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyVerified(View):
    def get(self, request):
        return render(request, 'property_verified.html')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
class PropertyUnverified(View):
    def get(self, request):
        return render(request, 'property_unverified.html')


@method_decorator(login_required, name = 'dispatch')
@method_decorator(verification_required, name = 'dispatch')
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
@method_decorator(verification_required, name = 'dispatch')
class PropertyContacted(View):
    def get(self, request):
        return render(request, 'property_contacted.html')


class SearchProperties(View):
    def get(self, request):
        properties = Property.objects.filter(verified = True)

        valor1 = request.GET.get('valor1', '')
        valor2 = request.GET.get('valor2', '')
        valor3 = request.GET.get('valor3', '')
        valor4 = request.GET.get('valor4', '')
        print(valor1,valor2,valor3,valor4)
        if valor1 != '' and valor1 is not None:
            properties = Property.objects.filter(provincie__icontains=valor1)

        if valor2 != '' and valor2 is not None:
            properties = Property.objects.filter(municipality__icontains=valor2)

        if valor3 != '' and valor3 is not None:
            properties = Property.objects.filter(address__icontains=valor3)

        if valor4 != '' and valor4 is not None:
            properties = Property.objects.filter(price__icontains=valor4)

        return render(request, 'search_properties.html', context = {'properties': properties})