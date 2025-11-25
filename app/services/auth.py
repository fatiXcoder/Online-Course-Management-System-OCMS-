# app/services/auth.py
from app.models.user import User

# Temporary in-memory users (DB will replace this later)
USERS = [
    {"id": 1, "username": "admin", "email": "admin@example.com",
     "full_name": "System Admin", "role": "Admin", "password": "admin123"},

    {"id": 2, "username": "teacher1", "email": "t1@example.com",
     "full_name": "John Teacher", "role": "Teacher", "password": "teacher123"},

    {"id": 3, "username": "student1", "email": "s1@example.com",
     "full_name": "Ali Student", "role": "Student", "password": "student123"},
]


def authenticate(username_or_email, password):
    """
    Authenticate user using username/email and password.
    DB version will replace this logic.
    """
    for u in USERS:
        if (u["username"] == username_or_email or u["email"] == username_or_email) \
                and u["password"] == password:
            return User(u["id"], u["username"], u["email"], u["full_name"], u["role"])
    return None
