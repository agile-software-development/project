from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    return render(request, 'homepage.html')


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        form.add_error(None, "Unsuccessful registration. Invalid information.")
    else:
        form = UserRegisterForm()
    return render(request=request, template_name="register.html", context={"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def update_profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request=request, template_name="update_profile.html", context={"form": form, "user": request.user})
