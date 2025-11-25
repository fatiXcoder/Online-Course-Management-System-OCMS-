# app/main.py
import tkinter as tk
from app.views.login import LoginWindow

def start_app():
    """Application entry point."""
    root = tk.Tk()
    root.withdraw()  # Hide main window until login is successful

    def handle_login(user):
        """Callback after successful login."""
        root.deiconify()
        root.title(f"Dashboard - {user.username}")
        from app.views.dashboard import Dashboard
        Dashboard(root, user)

    LoginWindow(root, handle_login)
    root.mainloop()

if __name__ == "__main__":
    start_app()
# app/models/course.py
from dataclasses import dataclass

@dataclass
class Course:
    id: int
    title: str
    description: str | None
    teacher_id: int
# app/services/course_service.py
from app.models.course import Course

class CourseService:
    def __init__(self, db):
        self.db = db

    def create(self, title: str, description: str, teacher_id: int) -> int:
        return self.db.query(
            "INSERT INTO courses(title, description, teacher_id) VALUES(%s,%s,%s)",
            (title, description, teacher_id)
        )

    def list_by_teacher(self, teacher_id: int) -> list[Course]:
        rows = self.db.query(
            "SELECT * FROM courses WHERE teacher_id=%s",
            (teacher_id,),
            fetchall=True
        )
        return [Course(**r) for r in rows]

    def get(self, course_id: int) -> Course | None:
        row = self.db.query(
            "SELECT * FROM courses WHERE id=%s",
            (course_id,),
            fetchone=True
        )
        return Course(**row) if row else None

    def update(self, course_id: int, title: str, description: str) -> int:
        return self.db.query(
            "UPDATE courses SET title=%s, description=%s WHERE id=%s",
            (title, description, course_id)
        )

    def delete(self, course_id: int) -> int:
        return self.db.query("DELETE FROM courses WHERE id=%s", (course_id,))

# app/services/enrollment_service.py
class EnrollmentService:
    def _init_(self, db):
        self.db = db

    def enroll(self, course_id: int, student_id: int) -> int:
        return self.db.query(
            "INSERT INTO enrollments(course_id, student_id) VALUES(%s,%s)",
            (course_id, student_id)
        )

    def list_students(self, course_id: int) -> list[dict]:
        return self.db.query(
            "SELECT u.id, u.username FROM enrollments e JOIN users u ON e.student_id=u.id WHERE e.course_id=%s",
            (course_id,),
            fetchall=True
        )

    def list_courses(self, student_id: int) -> list[dict]:
        return self.db.query(
            "SELECT c.* FROM enrollments e JOIN courses c ON e.course_id=c.id WHERE e.student_id=%s",
            (student_id,),
            fetchall=True
        )

    def unenroll(self, course_id: int, student_id: int) -> int:
        return self.db.query(
            "DELETE FROM enrollments WHERE course_id=%s AND student_id=%s",
            (course_id, student_id)
        )

# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.views.dashboard import DashboardView

class LoginView(tk.Frame):
    def _init_(self, master, db):
        super()._init_(master)
        self.db = db
        self.auth = AuthService(db)
        tk.Label(self, text="Username").grid(row=0, column=0)
        tk.Label(self, text="Password").grid(row=1, column=0)
        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show="*")
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        tk.Button(self, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        user = self.auth.authenticate(self.username.get(), self.password.get())
        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return
        self.destroy()
        DashboardView(self.master, self.db, user).pack(fill="both", expand=True)
# app/views/dashboard.py
import tkinter as tk
from app.views.courses import CoursesView
from app.views.enrollment import EnrollmentView
from app.views.assignments import AssignmentsView
from app.views.progress import ProgressView
from app.views.grading import GradingView
from app.views.announcements import AnnouncementsView

class DashboardView(tk.Frame):
    def __init__(self, master, db, user):
        super().__init__(master)
        self.db, self.user = db, user
        tk.Label(self, text=f"Welcome {user.username} ({user.role})").pack()
        if user.role in ("ADMIN", "TEACHER"):
            tk.Button(self, text="Courses", command=self.open_courses).pack(fill="x")
            tk.Button(self, text="Assignments", command=self.open_assignments).pack(fill="x")
            tk.Button(self, text="Grading", command=self.open_grading).pack(fill="x")
            tk.Button(self, text="Announcements", command=self.open_announcements).pack(fill="x")
        if user.role == "STUDENT":
            tk.Button(self, text="My Enrollments", command=self.open_enrollment).pack(fill="x")
            tk.Button(self, text="Progress", command=self.open_progress).pack(fill="x")

    def open_courses(self): CoursesView(self.master, self.db, self.user).pack()
    def open_enrollment(self): EnrollmentView(self.master, self.db, self.user).pack()
    def open_assignments(self): AssignmentsView(self.master, self.db, self.user).pack()
    def open_progress(self): ProgressView(self.master, self.db, self.user).pack()
    def open_grading(self): GradingView(self.master, self.db, self.user).pack()
    def open_announcements(self): AnnouncementsView(self.master, self.db, self.user).pack()
# app/views/courses.py
import tkinter as tk
from tkinter import messagebox
from app.services.course_service import CourseService

class CoursesView(tk.Frame):
    def __init__(self, master, db, user):
        super().__init__(master)
        self.service = CourseService(db)
        self.user = user
        tk.Label(self, text="Title").grid(row=0, column=0)
        tk.Label(self, text="Description").grid(row=1, column=0)
        self.title = tk.Entry(self); self.title.grid(row=0, column=1)
        self.desc = tk.Entry(self); self.desc.grid(row=1, column=1)
        tk.Button(self, text="Create", command=self.create_course).grid(row=2, column=0)
        tk.Button(self, text="Refresh", command=self.refresh).grid(row=2, column=1)
        self.listbox = tk.Listbox(self, width=50); self.listbox.grid(row=3, column=0, columnspan=2)
        tk.Button(self, text="Update", command=self.update_course).grid(row=4, column=0)
        tk.Button(self, text="Delete", command=self.delete_course).grid(row=4, column=1)
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for c in self.service.list_by_teacher(self.user.id):
            self.listbox.insert(tk.END, f"{c.id}: {c.title}")

    def selected_id(self):
        sel = self.listbox.curselection()
        if not sel: return None
        return int(self.listbox.get(sel[0]).split(":")[0])

    def create_course(self):
        if not self.title.get():
            messagebox.showerror("Error", "Title required"); return
        self.service.create(self.title.get(), self.desc.get(), self.user.id)
        self.refresh()

    def update_course(self):
        cid = self.selected_id()
        if not cid: return
        self.service.update(cid, self.title.get(), self.desc.get())
        self.refresh()

    def delete_course(self):
        cid = self.selected_id()
        if not cid: return
        self.service.delete(cid)
        self.refresh()
# tests/test_services/test_auth.py
import pytest
from unittest.mock import MagicMock
from app.services.auth import AuthService

def test_authenticate_success():
    db = MagicMock()
    db.query.return_value = {"id":1,"username":"rida","password_hash":AuthService(db).hash_password("pass"),"role":"ADMIN"}
    auth = AuthService(db)
    user = auth.authenticate("rida", "pass")
    assert user is not None
    assert user.username == "rida"

def test_authenticate_failure():
    db = MagicMock()
    db.query.return_value = None
    auth = AuthService(db)
    assert auth.authenticate("x","y") is None
# tests/test_services/test_course_service.py
from unittest.mock import MagicMock
from app.services.course_service import CourseService

def test_create_course_calls_insert():
    db = MagicMock()
    svc = CourseService(db)
    svc.create("Title","Desc",1)
    db.query.assert_called_with(
        "INSERT INTO courses(title, description, teacher_id) VALUES(%s,%s,%s)",
        ("Title","Desc",1)
    )
# tests/test_views/test_login.py
import tkinter as tk
from unittest.mock import MagicMock
from app.views.login import LoginView

def test_login_invalid(monkeypatch):
    root = tk.Tk()
    db = MagicMock()
    lv = LoginView(root, db)
    lv.username.insert(0, "x"); lv.password.insert(0, "y")
    db.query.return_value = None
    # Ensure no crash on invalid login
    lv.login()

