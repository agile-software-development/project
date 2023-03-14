from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('reset-password/', views.reset_password, name="reset-password"),
    path('profile/', views.update_profile_view, name="profile"),

    path('create-boards/', views.create_task_view, name="create-boards"),
    path('tasks/<task_id>/comment', login_required(views.CreateTaskCommentView.as_view()), name='comment-boards'),
    path('tasks/<pk>', login_required(views.TaskDetailView.as_view()), name='boards-detail'),
    path('tasks/', login_required(views.TaskListView.as_view()), name='list-tasks'),
    path('tasks/delete/<pk>', login_required(views.TaskDeleteView.as_view()), name='delete-boards'),
    path('tasks/update/<pk>', login_required(views.TaskUpdateView.as_view()), name='update-boards'),
    path('tasks/update/<pk>/state', views.change_task_state, name='change-boards-state'),

    path('create-board/', login_required(views.BoardCreateView.as_view()), name="create-board"),
    path('boards/', login_required(views.BoardListView.as_view()), name='list-boards'),
    path('boards/<pk>', login_required(views.BoardSingleView.as_view()), name='view-board'),
    path('boards/delete/<pk>', login_required(views.BoardDeleteView.as_view()), name='delete-board'),
    path('boards/update/<pk>', login_required(views.BoardUpdateView.as_view()), name='update-board'),

    path('create-workspace/', login_required(views.WorkspaceCreateView.as_view()), name="create-workspace"),
    path('workspaces/', login_required(views.WorkspacesListView.as_view()), name='list-workspaces'),
    path('workspaces/update/<pk>', login_required(views.WorkspaceUpdateView.as_view()), name='update-workspace'),

    path('', views.home, name='home'),
]
