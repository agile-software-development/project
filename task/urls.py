from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.update_profile_view, name="profile"),

    path('create-task/', views.create_task_view, name="create-task"),
    path('tasks/', login_required(views.TaskListView.as_view()), name='list-tasks'),
    path('tasks/delete/<pk>', login_required(views.TaskDeleteView.as_view())),
    path('tasks/update/<pk>', login_required(views.TaskUpdateView.as_view()), name='update-task'),

    path('create-board/', login_required(views.BoardCreateView.as_view()), name="create-board"),
    path('boards/', login_required(views.BoardListView.as_view()), name='list-boards'),
    path('boards/delete/<pk>', login_required(views.BoardDeleteView.as_view()), name='delete-board'),
    path('boards/update/<pk>', login_required(views.BoardUpdateView.as_view()), name='update-board'),

    path('', views.home, name='home'),
]