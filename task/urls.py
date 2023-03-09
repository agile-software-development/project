from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.update_profile_view, name="profile"),
    path('create-task/', views.create_task_view, name="create-task"),
    path('tasks/', views.TaskListView.as_view(), name='list-tasks'),
    path('tasks/delete/<pk>', views.TaskDeleteView.as_view()),
    path('', views.home, name='home'),
]