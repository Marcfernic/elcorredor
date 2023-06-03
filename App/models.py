# Import your functions here
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now

# Create your models here.
class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_update_to = models.CharField(max_length = 128, null = True, blank = True)
    email_verification_token = models.CharField(max_length = 128, null = True, blank = True)
    email_verified = models.BooleanField(default = False)
    password_reset_token = models.CharField(max_length = 128, null = True, blank = True)

    def email_verified_successfully(self):
        self.email_verified = True
        self.email_verification_token = None
        self.save()

    def email_updated_successfully(self):
        self.user.email = self.email_update_to
        self.user.save()

        self.email_verified = True
        self.email_verification_token = None
        self.email_update_to = None
        self.save()

    def generate_email_verification_token(self):
        self.email_verification_token = get_random_string(length = 32)
        self.save()

    def generate_password_reset_token(self):
        self.password_reset_token = get_random_string(length = 32)
        self.save()

    def password_reset_successfully(self):
        self.password_reset_token = None
        self.save()


class Property(models.Model):
    catastral_reference = models.CharField(max_length=14, help_text="Introduce solo los primeros 14 caracteres de la referencia", unique = True)
    price = models.FloatField(blank = False, null = False)
    verified = models.BooleanField(default =  False)
    created_at = models.DateTimeField(default = now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["user","created_at"]

    def get_absolute_url(self):
         return reverse('model-detail-view', args=[str(self.id)])

    def status_css_class(self):
        return 'success' if self.verified else 'danger'

    def status(self):
        return 'Publicada' if self.verified else 'Pendiente de revisión'

    def verify(self):
        self.verified = True
        self.save()
