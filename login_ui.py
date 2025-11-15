"""
Login UI module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module provides a modern login interface with inline account creation.
Features a single window that toggles between login and registration modes,
with consistent button styling and form validation.

Author: Jonathan
Date: 10/24/2025
"""

import tkinter as tk
from tkinter import messagebox
from auth import AuthenticationSystem, UserRole


class LoginWindow:
    """Login window that toggles between login and registration."""

    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_system = AuthenticationSystem()
        self.is_register_mode = False  # Start in login mode

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configure window."""
        self.root.title("Banner Web - Login")
        self.root.geometry("750x1150")  # MAXIMUM size to show all buttons completely
        self.root.configure(bg="#f0f4f8")

    def create_widgets(self):
        """Create all widgets."""
        # Main container
        self.main = tk.Frame(self.root, bg="#f0f4f8")
        self.main.pack(fill='both', expand=True, padx=50, pady=20)

        # Title
        self.title_label = tk.Label(
            self.main,
            text="Banner Web",
            font=('Arial', 24, 'bold'),
            bg="#f0f4f8",
            fg="#1f2937"
        )
        self.title_label.pack(pady=(15, 5))

        self.subtitle_label = tk.Label(
            self.main,
            text="Please login to continue",
            font=('Arial', 11),
            bg="#f0f4f8",
            fg="#6b7280"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Login Form
        form = tk.Frame(self.main, bg="white", relief=tk.SOLID, bd=1)
        form.pack(fill='both', expand=True, pady=10)

        self.form_inner = tk.Frame(form, bg="white")
        self.form_inner.pack(padx=40, pady=25)

        # Username
        tk.Label(self.form_inner, text="Username", font=('Arial', 11, 'bold'), bg="white", anchor='w').pack(fill='x', pady=(0, 5))
        self.username_entry = tk.Entry(self.form_inner, font=('Arial', 12), width=40)
        self.username_entry.pack(pady=(0, 15), ipady=8)
        self.username_entry.focus()

        # Password
        tk.Label(self.form_inner, text="Password", font=('Arial', 11, 'bold'), bg="white", anchor='w').pack(fill='x', pady=(0, 5))
        self.password_entry = tk.Entry(self.form_inner, font=('Arial', 12), show="*", width=40)
        self.password_entry.pack(pady=(0, 15), ipady=8)

        # Confirm Password (hidden initially, shown only in register mode)
        self.confirm_label = tk.Label(self.form_inner, text="Confirm Password", font=('Arial', 11, 'bold'), bg="white", anchor='w')
        self.confirm_entry = tk.Entry(self.form_inner, font=('Arial', 12), show="*", width=40)

        # Student ID (always visible)
        self.student_id_label = tk.Label(self.form_inner, text="Student ID", font=('Arial', 11, 'bold'), bg="white", anchor='w')
        self.student_id_label.pack(fill='x', pady=(0, 5))
        self.student_id_entry = tk.Entry(self.form_inner, font=('Arial', 12), width=40)
        self.student_id_entry.pack(pady=(0, 20), ipady=8)

        # Primary Action Button (LOGIN or REGISTER)
        self.action_button = tk.Button(
            self.form_inner,
            text="LOGIN",
            font=('Arial', 13, 'bold'),
            bg="#2563eb",
            fg="white",
            command=self.handle_action,
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.action_button.pack(pady=(0, 20), fill='x', ipady=12, padx=0)

        # Separator
        separator = tk.Frame(self.form_inner, bg="#e5e7eb", height=2)
        separator.pack(fill='x', pady=15)

        # Toggle text
        self.toggle_text = tk.Label(
            self.form_inner,
            text="Don't have an account?",
            font=('Arial', 12),
            bg="white",
            fg="#6b7280"
        )
        self.toggle_text.pack(pady=(0, 10))

        # Toggle Button (CREATE ACCOUNT or LOGIN)
        self.toggle_button = tk.Button(
            self.form_inner,
            text="CREATE ACCOUNT",
            font=('Arial', 13, 'bold'),
            bg="#2563eb",
            fg="white",
            command=self.toggle_mode,
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.toggle_button.pack(fill='x', ipady=12, padx=0)

        # Bind Enter key (initially for login mode)
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.student_id_entry.focus())
        self.student_id_entry.bind('<Return>', lambda e: self.handle_action())

    def handle_enter_from_password(self):
        """Handle Enter key from password field."""
        if self.is_register_mode:
            self.confirm_entry.focus()
        else:
            self.student_id_entry.focus()

    def toggle_mode(self):
        """Toggle between login and registration mode."""
        self.is_register_mode = not self.is_register_mode

        # Clear all fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)

        if self.is_register_mode:
            # Switch to registration mode
            self.subtitle_label.config(text="Create a new account")
            self.action_button.config(text="REGISTER")
            self.toggle_text.config(text="Already have an account?")
            self.toggle_button.config(text="LOGIN")

            # Show confirm password field BEFORE student ID label
            self.confirm_label.pack(fill='x', pady=(0, 5), before=self.student_id_label)
            self.confirm_entry.pack(pady=(0, 20), ipady=8, before=self.student_id_label)

            # Update Enter key binding for register mode
            self.password_entry.bind('<Return>', lambda e: self.confirm_entry.focus())
            self.confirm_entry.bind('<Return>', lambda e: self.student_id_entry.focus())
        else:
            # Switch to login mode
            self.subtitle_label.config(text="Please login to continue")
            self.action_button.config(text="LOGIN")
            self.toggle_text.config(text="Don't have an account?")
            self.toggle_button.config(text="CREATE ACCOUNT")

            # Hide confirm password field
            self.confirm_label.pack_forget()
            self.confirm_entry.pack_forget()

            # Update Enter key binding for login mode
            self.password_entry.bind('<Return>', lambda e: self.student_id_entry.focus())

        self.username_entry.focus()

    def handle_action(self):
        """Handle primary action (login or register)."""
        if self.is_register_mode:
            self.register()
        else:
            self.login()

    def login(self):
        """Handle login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        student_id = self.student_id_entry.get().strip()

        if not username or not password or not student_id:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        success, message, user = self.auth_system.login(username, password)

        if success:
            if not user.student_id:
                # Check if this student ID is already taken by another user
                for existing_user in self.auth_system.users.values():
                    if existing_user.student_id == student_id and existing_user.username != username:
                        messagebox.showerror("Error", f"Student ID {student_id} is already registered to another account.")
                        return

                user.student_id = student_id
                self.auth_system.save_users()
            self.on_login_success(self.auth_system, user)
        else:
            messagebox.showerror("Login Failed", message)

    def register(self):
        """Handle registration."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        student_id = self.student_id_entry.get().strip()

        if not username or not password or not student_id:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match!")
            return

        success, message = self.auth_system.register_user(username, password, UserRole.STUDENT, student_id)

        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            # Switch to login mode and pre-fill username and student ID
            self.toggle_mode()
            self.username_entry.insert(0, username)
            self.student_id_entry.insert(0, student_id)
            self.password_entry.focus()
        else:
            messagebox.showerror("Error", message)
