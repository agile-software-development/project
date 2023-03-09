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
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone', required=False, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created', 'updated')