# app/utils/style.py
"""
This module stores styling-related helpers.
Add themes, fonts, and common UI formatting here.
"""

DEFAULT_FONT = ("Arial", 12)
HEADER_FONT = ("Arial", 16, "bold")

def apply_style(widget):
    """Apply default styling to widgets (future enhancement)."""
    widget.configure(font=DEFAULT_FONT)
