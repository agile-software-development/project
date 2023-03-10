from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Task, Board


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(label='شماره تلفن', required=True, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "username", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'ایجاد حساب کاربری', css_class='btn-success'))
        self.helper.form_method = 'POST'
        self.helper.form_action = '.'

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
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'
        self.helper.form_action = '/login/'


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone', required=False, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created', 'updated')


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('created', 'updated', 'creator')
