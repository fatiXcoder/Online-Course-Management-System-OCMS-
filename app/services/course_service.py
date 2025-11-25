# app/services/course_service.py
from app.models.course import Course

# Temporary in-memory list (DB later)
COURSES = [
    {"id": 1, "title": "Introduction to Python", "description": "Basics of Python programming."},
    {"id": 2, "title": "Database Fundamentals", "description": "SQL, ERD, normalization."}
]

_next_id = 3   # For auto-increment simulation


def get_all_courses():
    """Return all courses."""
    return [Course(c["id"], c["title"], c["description"]) for c in COURSES]


def add_course(title, description):
    """Add a new course."""
    global _next_id
    COURSES.append({
        "id": _next_id,
        "title": title,
        "description": description
    })
    _next_id += 1


def update_course(course_id, title, description):
    """Update an existing course."""
    for c in COURSES:
        if c["id"] == course_id:
            c["title"] = title
            c["description"] = description
            break


def delete_course(course_id):
    """Delete a course by ID."""
    global COURSES
    COURSES = [c for c in COURSES if c["id"] != course_id]
