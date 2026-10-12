
"""Create the FastAPI app and connect its routes."""

from fastapi import FastAPI, HTTPException
import sqlite3
from app.database import database_connection, initialize_database
from app.models import Student, StudentInput, Task, TaskInput

app = FastAPI(title="Student Task Management System")


@app.get("/")
def home():
    return {"message": "Welcome! Visit /docs to try the API."}


# STUDENT ENDPOINTS

@app.get("/students")
def get_students():
    result = Student.list_students(database_connection)
    return {"students": result}


@app.get("/students/{student_id}")
def get_student(student_id: int):
    result = Student.get_student(student_id, database_connection)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"student": result}


@app.post("/students")
def create_student(student: StudentInput):
    result = Student.create_student(student, database_connection)
    return {"student": result}


@app.put("/students/{student_id}")
def edit_student(student_id: int, student: StudentInput):
    result = Student.update_student(
        student_id, student, database_connection
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"student": result}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    result = Student.delete_student(student_id, database_connection)

    if not result:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}


# TASK ENDPOINTS

@app.get("/tasks")
def get_tasks():
    result = Task.list_tasks(database_connection)
    return {"tasks": result}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    result = Task.get_task(task_id, database_connection)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task": result}


@app.post("/tasks")
def create_task(task: TaskInput):
    try:
        result = Task.create_task(task, database_connection)
        return {"task": result}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Student ID does not exist."
        )


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskInput):
    result = Task.update_task(task_id, task, database_connection)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task": result}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    result = Task.delete_task(task_id, database_connection)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


# GET TASKS BELONGING TO A STUDENT

@app.get("/students/{student_id}/tasks")
def get_student_tasks(student_id: int):
    student = Student.get_student(student_id, database_connection)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    result = Task.list_student_tasks(student_id, database_connection)
    return {"tasks": result}


initialize_database()
