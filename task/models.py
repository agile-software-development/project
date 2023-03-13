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


class Workspace(BaseModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_workspaces')
    members = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        super(Workspace, self).save(*args, **kwargs)
        self.members.add(self.creator)

    def __str__(self):
        return self.name


class Board(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_boards')
    members = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        super(Board, self).save(*args, **kwargs)
        self.members.add(self.creator)

    def __str__(self):
        return self.name


class Task(BaseModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    state = models.PositiveSmallIntegerField(choices=TaskStates.choices, default=TaskStates.Todo.value)
    description = models.TextField()
    members = models.ManyToManyField(User)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        self.members.add(self.creator)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_comments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, default=None)
