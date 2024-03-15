# **Task Management System**     

This is a Task Management System web application built using Django and FastAPI. It allows users to create, update, delete, and assign tasks. The system also supports asynchronous task processing using Celery.

**Features**
- User Authentication: Users can register, login, and logout from the system. Authentication is handled using Django's built-in authentication system.
- Task Management: Users can create tasks with title, description, due date, priority, and assignee. They can view a list of tasks they have created or assigned to them, and filter tasks based on status. Tasks can be edited and deleted by the creator.
- Asynchronous Task Processing: Email notifications are sent asynchronously using Celery when a task is created.
- API Integration: Provides RESTful API endpoints using FastAPI for CRUD operations on tasks.
- Unit Tests: Comprehensive unit tests ensure the reliability and correctness of the implemented functionalities.

**Installation**
Clone the repository:

git clone https://github.com/osamaliaqat/task-management-system.git

**Install dependencies:**

cd task-management-system
pip install -r requirements.txt

**Run migrations:**
python manage.py migrate

**Start the Django server:**
python manage.py runserver

**Start Celery worker:**
celery -A task_management_system worker --loglevel=info

**Start FastAPI server:**
uvicorn task_management_system.fastapi_app:app --host 0.0.0.0 --port 8001 --reload

**Usage**
- Access the web application at http://localhost:8000.
- Access the FastAPI documentation at http://localhost:8001/docs.
- Use the RESTful API endpoints for task management.
