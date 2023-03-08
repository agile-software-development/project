from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskStates(models.IntegerChoices):
    Todo = 1
    Doing = 2
    Done = 3
    Closed = 4


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    phone_number = models.CharField(max_length=200, unique=True)
    avatar = models.FileField(upload_to='uploads/avatars/')
    themes = (
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
    )
    theme = models.CharField(max_length=255, choices=themes)


class Task(BaseModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    state = models.PositiveSmallIntegerField(choices=TaskStates.choices, default=TaskStates.Todo.value)
    description = models.TextField()
    members = models.ManyToManyField(User)

