# app/models/user.py

class User:
    """User model representing Admin / Teacher / Student."""

    def __init__(self, user_id, username, email, full_name, role):
        self.id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.role = role

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
