from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task
from .tasks import send_task_notification_email


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "admin:login"
            )
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task_detail.html", {"task": task})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            send_task_notification_email.delay(task.id)
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_form.html", {"form": form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "task_confirm_delete.html", {"task": task})


def task_list(request):
    status = request.GET.get("status")
    if status:
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.all()
    return render(request, "task_list.html", {"tasks": tasks})


def create_task(request):
    if request.method == "POST":
        task = Task.objects.create(...)
        send_task_notification_email.delay(task.pk)
        return redirect("task_list")
