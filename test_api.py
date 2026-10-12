
"""Tests for the Student Task Management System API."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_student_and_task_crud():
    # Create a student
    student_response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "program": "BSIT",
            "course_title": "IT5",
        },
    )

    assert student_response.status_code == 200
    student = student_response.json()["student"]
    student_id = student["student_id"]

    # Read the student
    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["student"]["name"] == "Test Student"

    # Create a task
    task_response = client.post(
        "/tasks",
        json={
            "student_id": student_id,
            "title": "Test Assignment",
            "details": "Testing task creation",
            "deadline": "2026-10-20",
            "status": "Pending",
        },
    )

    assert task_response.status_code == 200
    task = task_response.json()["task"]
    task_id = task["task_id"]

    # Read the task
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["task"]["title"] == "Test Assignment"

    # Read tasks assigned to the student
    response = client.get(f"/students/{student_id}/tasks")

    assert response.status_code == 200
    assert len(response.json()["tasks"]) >= 1

    # Update the task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "student_id": student_id,
            "title": "Updated Assignment",
            "details": "Testing task updates",
            "deadline": "2026-10-25",
            "status": "In Progress",
        },
    )

    assert response.status_code == 200
    assert response.json()["task"]["status"] == "In Progress"

    # Update the student
    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "Updated Student",
            "program": "BSIT",
            "course_title": "IT5",
        },
    )

    assert response.status_code == 200
    assert response.json()["student"]["name"] == "Updated Student"

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    # Delete the student
    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 200


def test_invalid_task_status():
    response = client.post(
        "/tasks",
        json={
            "student_id": 1,
            "title": "Invalid Status Test",
            "details": "",
            "deadline": "2026-10-20",
            "status": "Finished",
        },
    )

    assert response.status_code == 422


def test_nonexistent_student():
    response = client.get("/students/999999999")

    assert response.status_code == 404


def test_nonexistent_task():
    response = client.get("/tasks/999999999")

    assert response.status_code == 404
