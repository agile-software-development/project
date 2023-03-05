from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=200)

    class Meta:
        model = User
        fields = ("phone_number", "username", "first_name", "last_name", "password1", "password2", "avatar")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user
