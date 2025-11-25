# app/views/dashboard.py
import tkinter as tk
from tkinter import ttk
from app.views.course_management import CourseManager


class Dashboard(tk.Frame):
    """Dashboard UI which loads after successful login."""

    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.pack(fill="both", expand=True)

        tk.Label(self, text=f"Welcome, {self.user.full_name or self.user.username}",
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text=f"Role: {self.user.role}",
                 font=("Arial", 12)).pack()

        # Navigation Buttons
        ttk.Button(self, text="Course Management",
                   width=25, command=self.open_course_manager).pack(pady=15)

    def open_course_manager(self):
        """Open course management window."""
        CourseManager(self.master, self.user)
