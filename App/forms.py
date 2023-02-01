from .models import User, Property
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = "__all__"
