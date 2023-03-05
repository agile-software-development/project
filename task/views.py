from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib import messages


def home(request):
    return render(request, 'homepage.html')


def register_request(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You registered successfully")
            return redirect('home')
        print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegisterForm()
    return render(request=request, template_name="register.html", context={"form": form})
