# app/models/course.py

class Course:
    """Course model representing a single course."""

    def __init__(self, course_id, title, description):
        self.id = course_id
        self.title = title
        self.description = description

    def __repr__(self):
        return f"<Course {self.title}>"
