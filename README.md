# Student Task Management System (FastAPI + SQLite)

## Problem and solution

Students often manage their assignments, deadlines, and school requirements using notebooks, chat messages, or separate applications. This can make it difficult to organize tasks, monitor progress, and remember upcoming deadlines.

The Student Task Management System provides a simple API for managing student records and their academic tasks in one place. Users can register student information, create tasks, set deadlines, update task statuses, and track which tasks are pending, in progress, or completed.

**Intended users:** Students who want a simple way to organize academic tasks and monitor their progress.

## Features

- **Student management:** Create, list, view, update, and delete student records.
- **Task management:** Create, list, view, update, and delete academic tasks.
- **Task assignment:** Connect each task to an existing student.
- **Task status tracking:** Mark tasks as Pending, In Progress, or Completed.
- **Student task list:** View all tasks assigned to a specific student.
- **Input validation:** Validate required fields and reject invalid task statuses.
- **Error handling:** Return clear errors when a student or task does not exist or when a task references an invalid student.
- **API documentation:** Use FastAPI's interactive `/docs` page to test endpoints.

## Database design

The system uses two related tables with primary keys and foreign keys.

| Table | Key columns | Purpose |
| --- | --- | --- |
| `students` | `student_id` (PK), `name`, `program`, `course_title` | Stores student information |
| `tasks` | `task_id` (PK), `student_id` (FK), `title`, `details`, `deadline`, `status` | Stores academic tasks assigned to students |

### Relationships

```text
students 1 -------- * tasks
```

One student can have multiple tasks. Each task belongs to one student through `student_id`.

### Integrity rules

- Each table has its own primary key.
- Every task must reference an existing student.
- Foreign key enforcement is enabled using `PRAGMA foreign_keys = ON`.
- Deleting a student also deletes their assigned tasks through `ON DELETE CASCADE`.
- Task status is limited to `Pending`, `In Progress`, or `Completed`.
- Parameterized SQL queries use `?` placeholders to safely pass values to the database.

## Transaction handling

Database operations use a connection context manager in `app/database.py`.

1. Open a database connection.
2. Execute the database operation.
3. Commit changes when the operation succeeds.
4. Roll back changes if an error occurs.
5. Close the connection.

This helps keep database operations consistent and prevents incomplete changes from being saved when an error occurs.

## OOP design

| Class | File | Responsibility |
| --- | --- | --- |
| `StudentInput` | `app/models.py` | Validates student input |
| `Student` | `app/models.py` | Handles student database operations |
| `TaskInput` | `app/models.py` | Validates task input and status |
| `Task` | `app/models.py` | Handles task database operations |
| `database_connection()` | `app/database.py` | Manages database connections and transactions |
| `initialize_database()` | `app/database.py` | Creates the database tables |
| FastAPI application and route functions | `main.py` | Handles HTTP requests, responses, and errors |

**OOP and programming concepts used:** Classes, inheritance through Pydantic models, encapsulation of database operations in model classes, functions, exception handling, and separation of responsibilities between routes, models, and database setup.

## Project structure

```text
main.py             FastAPI application and endpoints
requirements.txt    Required Python packages
test_api.py         Automated API tests
students.db         SQLite database, created automatically
app/
    __init__.py     Application package
    database.py     Database connection and table setup
    models.py       Pydantic models and database operations
```

The `students.db` file is created automatically when the application initializes. Keep a backup before deleting or replacing an existing database.

## Run it on Windows (VS Code)

1. Open the project folder in VS Code.
2. Open a terminal using **Terminal > New Terminal**.
3. Create a virtual environment:

```powershell
py -m venv .venv
```

4. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can allow local scripts for your Windows user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

5. Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

6. Start the FastAPI server:

```powershell
python -m uvicorn main:app --reload
```

7. Open the interactive API documentation:

http://127.0.0.1:8000/docs

Press `Ctrl+C` in the terminal to stop the server.

## Endpoints

### General

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Displays a welcome message |

### Student endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/students` | Lists all students |
| GET | `/students/{student_id}` | Retrieves one student |
| POST | `/students` | Creates a student |
| PUT | `/students/{student_id}` | Updates a student |
| DELETE | `/students/{student_id}` | Deletes a student and their assigned tasks |

### Task endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/tasks` | Lists all tasks |
| GET | `/tasks/{task_id}` | Retrieves one task |
| POST | `/tasks` | Creates a task |
| PUT | `/tasks/{task_id}` | Updates a task |
| DELETE | `/tasks/{task_id}` | Deletes a task |
| GET | `/students/{student_id}/tasks` | Lists tasks belonging to a student |

### Common errors

- **400:** A task references a student ID that does not exist.
- **404:** The requested student or task does not exist.
- **422:** The request data is invalid, such as an unsupported task status or missing required field.

## Test it from the docs page

1. Open `/docs` in your browser.
2. Expand `POST /students` and click **Try it out**.
3. Create a student using this example:

```json
{
  "name": "Test Student",
  "program": "BSIT",
  "course_title": "IT5"
}
```

4. Execute the request and note the returned `student_id`.
5. Expand `POST /tasks` and create a task using that ID:

```json
{
  "student_id": 1,
  "title": "IT5 Project",
  "details": "Complete the FastAPI project",
  "deadline": "2026-10-20",
  "status": "Pending"
}
```

Replace `1` with the actual student ID returned by your request.

6. Use `GET /tasks` to view the task.
7. Use `GET /students/{student_id}/tasks` to view tasks assigned to that student.
8. Use `PUT /tasks/{task_id}` to change the task status to `In Progress` or `Completed`.
9. Use `DELETE /tasks/{task_id}` to remove the task.
10. Use `DELETE /students/{student_id}` to remove the test student.

You can also run the automated tests from the VS Code terminal:

```powershell
python -m pytest -v
```

## How the safe SQL works

The system uses parameterized SQL queries instead of directly inserting user input into SQL statements.

Example:

```python
connection.execute(
    "DELETE FROM tasks WHERE task_id = ?",
    (task_id,)
)
```

The `?` placeholder keeps the supplied value separate from the SQL command. This helps protect database operations against SQL injection.

## Common problems

- **`python` is not recognized:** Try using `py` or reinstall Python with the PATH option enabled.
- **`No module named fastapi`:** Activate the virtual environment and install the packages.
- **Port already in use:** Start the server on another port:

```powershell
python -m uvicorn main:app --reload --port 8001
```

- **Old database schema:** If the existing `students.db` has the original starter project's table structure, back it up before replacing it. The current table creation code does not automatically migrate an existing table to the new schema.
- **Want a fresh database:** Stop the server and back up or delete `students.db`. The application will create the tables again on startup.
