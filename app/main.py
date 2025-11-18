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
