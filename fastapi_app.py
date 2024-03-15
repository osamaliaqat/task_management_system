import os
from typing import List, Optional

from django.core.asgi import get_asgi_application
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .tasks.tasks import send_task_notification_email

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management_system.settings")

application = get_asgi_application()

app = FastAPI()
app.mount("/django", application)
app.mount("/admin", application)


class Task(BaseModel):
    title: str
    description: str
    due_date: str
    priority: str
    assigned_to: Optional[int] = None
    status: str


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI from Django!"}


@app.post("/tasks/")
def create_task(task: Task):
    from tasks.models import Task

    task_obj = Task.objects.create(**task.dict())
    send_task_notification_email.delay(task.pk)
    return task_obj


@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    from tasks.models import Task

    return Task.objects.all()


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    from tasks.models import Task

    try:
        task = Task.objects.get(pk=task_id)
        task.due_date = str(task.due_date)
        return task
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    from tasks.models import Task

    try:
        task_obj = Task.objects.get(pk=task_id)
        task_obj.title = task.title
        task_obj.description = task.description
        task_obj.due_date = task.due_date
        task_obj.priority = task.priority
        task_obj.assigned_to = task.assigned_to
        task_obj.status = task.status
        task_obj.save()
        return task_obj
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    from tasks.models import Task

    try:
        task_obj = Task.objects.get(pk=task_id)
        task_obj.delete()
        return {"message": "Task deleted successfully"}
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
