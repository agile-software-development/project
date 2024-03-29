from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import User, Task, Board, Comment, Workspace, InviteLink


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
        self.helper.add_input(Submit('submit', 'ورود', css_class='btn-primary'))
        self.helper.form_method = 'POST'
        self.helper.form_action = '/login/'


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone', required=False, max_length=200)
    theme = forms.Select(choices=User.themes)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "theme")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created', 'updated', 'creator')


class BoardForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(required=False, queryset=Task.objects.none())

    class Meta:
        model = Board
        exclude = ('created', 'updated', 'creator')

    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        self.fields['tasks'].queryset = Task.objects.filter(Q(board__isnull=True) | Q(board=self.instance))
        self.fields['tasks'].initial = Task.objects.filter(board=self.instance)

    def save(self, commit=True):
        instance = super(BoardForm, self).save(commit)
        for task in instance.task_set.all():
            task.board = None
            task.save()

        for task in self.cleaned_data['tasks']:
            task.board = instance
            task.save()

        link = InviteLink(board=instance)
        link.save()

        return instance


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'description')


class WorkspaceForm(forms.ModelForm):
    boards = forms.ModelMultipleChoiceField(required=False, queryset=Board.objects.none())

    class Meta:
        model = Workspace
        exclude = ('created', 'updated', 'creator')

    def __init__(self, *args, **kwargs):
        super(WorkspaceForm, self).__init__(*args, **kwargs)
        self.fields['boards'].queryset = Board.objects.filter(Q(workspace__isnull=True) | Q(workspace=self.instance))
        self.fields['boards'].initial = Board.objects.filter(workspace=self.instance)

    def save(self, commit=True):
        instance = super(WorkspaceForm, self).save(commit)
        for board in instance.board_set.all():
            board.workspace = None
            board.save()

        for board in self.cleaned_data['boards']:
            board.workspace = instance
            board.save()

        link = InviteLink(workspace=instance)
        link.save()

        return instance
