from django.forms import ModelForm

from users.models import CustomUser


class UserSettingsForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'password', 'about_me', 'phone_number', 'email')
