from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .forms import UserRegisterForm, LoginForm, UserProfileForm, TaskForm, BoardForm
from .models import Task, Board


def home(request):
    if request.user.is_authenticated:
        return redirect('list-tasks')
    return render(request, 'newHome.html')


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


@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')


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


@login_required()
def create_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.creator = request.user
            instance.save()
            return redirect('list-tasks')
        form.add_error(None, "Unsuccessful registration. Invalid information.")
    else:
        form = TaskForm()
    return render(request=request, template_name="task.html", context={"form": form})


class TaskListView(ListView):
    model = Task
    paginate_by = 100  # if pagination is desired


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('list-tasks')
    template_name = "task/task_delete.html"

    success_message = "Task was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TaskDeleteView, self).delete(request, *args, **kwargs)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('list-tasks')


class BoardCreateView(CreateView):
    model = Board
    form_class = BoardForm
    success_url = reverse_lazy('list-boards')

    def form_valid(self, form):
        response = super(BoardCreateView, self).form_valid(form)
        self.object.creator = self.request.user
        self.object.save()
        return response


class BoardListView(ListView):
    model = Board
    paginate_by = 100


class BoardDeleteView(DeleteView):
    model = Board
    template_name = "task/board_delete.html"
    success_url = reverse_lazy('list-boards')


class BoardUpdateView(UpdateView):
    model = Board
    form_class = BoardForm
    success_url = reverse_lazy('list-boards')
