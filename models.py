
"""Data models and database operations."""

from pydantic import BaseModel, Field, field_validator


# STUDENT MODELS

class StudentInput(BaseModel):
    """Fields required when creating or updating a student."""

    name: str = Field(min_length=1)
    program: str = Field(min_length=1)
    course_title: str = Field(min_length=1)


class Student(StudentInput):
    """Student record returned by the API."""

    student_id: int

    @staticmethod
    def list_students(database_connection):
        with database_connection() as connection:
            rows = connection.execute(
                """
                SELECT student_id, name, program, course_title
                FROM students
                ORDER BY student_id
                """
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def create_student(student_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO students (name, program, course_title)
                VALUES (?, ?, ?)
                """,
                (
                    student_input.name,
                    student_input.program,
                    student_input.course_title,
                ),
            )

            row = connection.execute(
                """
                SELECT student_id, name, program, course_title
                FROM students WHERE student_id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()

        return dict(row)

    @staticmethod
    def get_student(student_id, database_connection):
        with database_connection() as connection:
            row = connection.execute(
                """
                SELECT student_id, name, program, course_title
                FROM students WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        return dict(row) if row else None

    @staticmethod
    def update_student(student_id, student_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE students
                SET name = ?, program = ?, course_title = ?
                WHERE student_id = ?
                """,
                (
                    student_input.name,
                    student_input.program,
                    student_input.course_title,
                    student_id,
                ),
            )

            if cursor.rowcount == 0:
                return None

            row = connection.execute(
                """
                SELECT student_id, name, program, course_title
                FROM students WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()

        return dict(row) if row else None

    @staticmethod
    def delete_student(student_id, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,),
            )

        return cursor.rowcount > 0


# TASK MODELS

class TaskInput(BaseModel):
    """Fields required when creating or updating a task."""

    student_id: int = Field(gt=0)
    title: str = Field(min_length=1)
    details: str = ""
    deadline: str = Field(min_length=1)
    status: str = "Pending"

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        allowed_statuses = [
            "Pending",
            "In Progress",
            "Completed",
        ]

        if value not in allowed_statuses:
            raise ValueError("Invalid task status")

        return value


class Task(TaskInput):
    """Task record returned by the API."""

    task_id: int

    @staticmethod
    def list_tasks(database_connection):
        with database_connection() as connection:
            rows = connection.execute(
                """
                SELECT task_id, student_id, title, details, deadline, status
                FROM tasks
                ORDER BY task_id
                """
            ).fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def create_task(task_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks
                    (student_id, title, details, deadline, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task_input.student_id,
                    task_input.title,
                    task_input.details,
                    task_input.deadline,
                    task_input.status,
                ),
            )

            row = connection.execute(
                """
                SELECT task_id, student_id, title, details, deadline, status
                FROM tasks WHERE task_id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()

        return dict(row)

    @staticmethod
    def get_task(task_id, database_connection):
        with database_connection() as connection:
            row = connection.execute(
                """
                SELECT task_id, student_id, title, details, deadline, status
                FROM tasks WHERE task_id = ?
                """,
                (task_id,),
            ).fetchone()

        return dict(row) if row else None

    @staticmethod
    def update_task(task_id, task_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET student_id = ?, title = ?, details = ?,
                    deadline = ?, status = ?
                WHERE task_id = ?
                """,
                (
                    task_input.student_id,
                    task_input.title,
                    task_input.details,
                    task_input.deadline,
                    task_input.status,
                    task_id,
                ),
            )

            if cursor.rowcount == 0:
                return None

            row = connection.execute(
                """
                SELECT task_id, student_id, title, details, deadline, status
                FROM tasks WHERE task_id = ?
                """,
                (task_id,),
            ).fetchone()

        return dict(row) if row else None

    @staticmethod
    def delete_task(task_id, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE task_id = ?",
                (task_id,),
            )

        return cursor.rowcount > 0

    @staticmethod
    def list_student_tasks(student_id, database_connection):
        with database_connection() as connection:
            rows = connection.execute(
                """
                SELECT task_id, student_id, title, details, deadline, status
                FROM tasks
                WHERE student_id = ?
                ORDER BY task_id
                """,
                (student_id,),
            ).fetchall()

        return [dict(row) for row in rows]
