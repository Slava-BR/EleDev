from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField, CharField


class CharacteristicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        characteristic = kwargs['characteristic']
        kwargs = {}
        super().__init__(*args, **kwargs)
        for section_title, section_value in characteristic.items():
            self.fields[section_title] = CharField(disabled=True)
            for key, value in section_value.items():
                value.insert(0, " ")
                self.fields[key] = ChoiceField(choices=[(i, i) for i in value])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

