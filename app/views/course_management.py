# app/views/course_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.services.course_service import (
    get_all_courses,
    add_course,
    update_course,
    delete_course
)


class CourseManager(tk.Toplevel):
    """CRUD interface for managing courses."""

    def __init__(self, master, user):
        super().__init__(master)
        self.title("Course Management")
        self.geometry("700x450")
        self.resizable(False, False)

        self.user = user

        tk.Label(self, text="Course Management", font=("Arial", 16, "bold")).pack(pady=10)

        # ----------- Course Form -----------
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Course Title").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Description").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Add", width=12, command=self.create_course).grid(row=2, column=0, pady=15)
        ttk.Button(form_frame, text="Update", width=12, command=self.modify_course).grid(row=2, column=1)
        ttk.Button(form_frame, text="Delete", width=12, command=self.remove_course).grid(row=2, column=2)

        # ----------- Course Table -----------
        self.tree = ttk.Treeview(self, columns=("id", "title", "desc"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Course Title")
        self.tree.heading("desc", text="Description")
        self.tree.pack(fill="x", padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_courses()

    # ---------------- CRUD METHODS ----------------

    def load_courses(self):
        """Load courses from DB."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for course in get_all_courses():
            self.tree.insert("", "end", values=(course.id, course.title, course.description))

    def create_course(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Course title cannot be empty.")
            return

        add_course(title, desc)
        self.load_courses()
        messagebox.showinfo("Success", "Course added successfully.")

    def modify_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a course to update.")
            return

        item = self.tree.item(selected)
        course_id = item["values"][0]

        update_course(course_id, self.title_entry.get(), self.desc_entry.get())
        self.load_courses()
        messagebox.showinfo("Updated", "Course updated successfully.")

    def remove_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a course to delete.")
            return

        item = self.tree.item(selected)
        course_id = item["values"][0]

        delete_course(course_id)
        self.load_courses()
        messagebox.showinfo("Deleted", "Course removed.")

    def on_select(self, event):
        """Load selected course details into form."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            _id, title, desc = item["values"]

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)

            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, desc)
