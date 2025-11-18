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

