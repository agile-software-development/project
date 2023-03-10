from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Task


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(label='Phone', required=True, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', wrapper_class='mb-3', css_class='form-control', placeholder="Username"),
            Field('password', wrapper_class='mb-3', css_class='form-control', placeholder="Username"),
            Div(
                Div(
                    Submit(name='submit', value='ورود', css_class='btn-block'),
                    css_class='grid-4'),
                css_class='mt-4 mb-0'
            )
        )

    class Meta:
        labels = {
            'username': 'نام کاربری',
        }


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone', required=False, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created', 'updated')
