# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import authenticate


class LoginWindow(tk.Toplevel):
    """Login window for Admin/Teacher/Student."""

    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("Login")
        self.geometry("350x250")
        self.resizable(False, False)

        tk.Label(self, text="Login to Continue", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Username or Email").pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", width=12, command=self.try_login).pack(pady=15)

    def try_login(self):
        """Validate credentials."""
        uname = self.username_entry.get().strip()
        pwd = self.password_entry.get()

        user = authenticate(uname, pwd)

        if user:
            messagebox.showinfo("Success", f"Welcome, {user.full_name or user.username}!")
            self.on_success(user)
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
