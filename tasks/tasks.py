from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task


@shared_task
def send_task_notification_email(task_pk):
    task = Task.objects.get(pk=task_pk)
    assigned_user = task.assigned_to
    if assigned_user:
        subject = f"New Task Assigned: {task.title}"
        message = f"Task: {task.title}\nDescription: {task.description}\nDue Date: {task.due_date}\nPriority: {task.priority}\nStatus: {task.status}"
        from_email = "your@example.com"
        to_email = [assigned_user.email]
        send_mail(subject, message, from_email, to_email)


@receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if created or instance.status_changed:
        send_task_notification_email.delay(instance.pk)
