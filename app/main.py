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

