from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('profile/', views.update_profile_view, name="profile"),
    path('', views.home, name='home'),
]