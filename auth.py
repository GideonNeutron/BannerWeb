"""
Authentication module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module handles user authentication, password management, and user roles.
Uses SHA-256 hashing for secure password storage and validates unique Student IDs.
Implements CSV file persistence for user credentials.

Author: Jonathan
Date: 10/24/2025
"""

import hashlib
import csv
import os
from typing import Optional, Tuple
from enum import Enum


class UserRole(Enum):
    """Enumeration of user roles in the system."""
    STUDENT = "student"
    ADMIN = "admin"


class User:
    """Represents a user in the authentication system."""

    def __init__(self, username: str, password_hash: str, role: UserRole, student_id: Optional[str] = None):
        """
        Initialize a User object.

        Args:
            username: Username for login
            password_hash: Hashed password
            role: User role (STUDENT or ADMIN)
            student_id: Student ID if the user is a student
        """
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.student_id = student_id

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return self.password_hash == self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()


class AuthenticationSystem:
    """Manages user authentication and credentials."""

    def __init__(self, data_directory: str = "."):
        """
        Initialize the authentication system.

        Args:
            data_directory: Directory where user credentials are stored
        """
        self.data_directory = data_directory
        self.users = {}
        self.current_user: Optional[User] = None
        self.load_users()

        # Create default admin account if no users exist
        if not self.users:
            self._create_default_accounts()

    def _get_file_path(self, filename: str) -> str:
        """Get the full path for a data file."""
        return os.path.join(self.data_directory, filename)

    def load_users(self) -> None:
        """Load user credentials from CSV file."""
        users_file = self._get_file_path('users_auth.csv')
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        role = UserRole.STUDENT if row['role'] == 'student' else UserRole.ADMIN
                        student_id = row.get('student_id', '') if row.get('student_id') else None
                        user = User(
                            row['username'],
                            row['password_hash'],
                            role,
                            student_id
                        )
                        self.users[user.username] = user
            except Exception as e:
                print(f"Error loading users: {e}")

    def save_users(self) -> None:
        """Save user credentials to CSV file."""
        users_file = self._get_file_path('users_auth.csv')
        try:
            with open(users_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['username', 'password_hash', 'role', 'student_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for user in self.users.values():
                    writer.writerow({
                        'username': user.username,
                        'password_hash': user.password_hash,
                        'role': user.role.value,
                        'student_id': user.student_id if user.student_id else ''
                    })
        except Exception as e:
            print(f"Error saving users: {e}")

    def _create_default_accounts(self) -> None:
        """Create default admin and demo accounts."""
        # Create admin account
        admin = User(
            "admin",
            User._hash_password("admin123"),
            UserRole.ADMIN,
            None
        )
        self.users["admin"] = admin

        # Create a demo student account
        student = User(
            "student",
            User._hash_password("student123"),
            UserRole.STUDENT,
            "S001"
        )
        self.users["student"] = student

        self.save_users()

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate a user.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Tuple of (success: bool, message: str, user: Optional[User])
        """
        if not username or not password:
            return False, "Username and password cannot be empty.", None

        if username not in self.users:
            return False, "Invalid username or password.", None

        user = self.users[username]
        if not user.check_password(password):
            return False, "Invalid username or password.", None

        self.current_user = user
        return True, f"Welcome, {username}!", user

    def logout(self) -> None:
        """Log out the current user."""
        self.current_user = None

    def register_user(self, username: str, password: str, role: UserRole, student_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Register a new user.

        Args:
            username: Username
            password: Plain text password
            role: User role
            student_id: Student ID (required for students)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty."

        if username in self.users:
            return False, "Username already exists."

        if role == UserRole.STUDENT and not student_id:
            return False, "Student ID is required for student accounts."

        if len(password) < 6:
            return False, "Password must be at least 6 characters long."

        # Check if student ID is already taken
        if student_id:
            for existing_user in self.users.values():
                if existing_user.student_id == student_id:
                    return False, f"Student ID {student_id} is already registered to another account."

        user = User(
            username,
            User._hash_password(password),
            role,
            student_id
        )
        self.users[username] = user
        self.save_users()

        return True, f"User {username} registered successfully."

    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change a user's password.

        Args:
            username: Username
            old_password: Current password
            new_password: New password

        Returns:
            Tuple of (success: bool, message: str)
        """
        if username not in self.users:
            return False, "User not found."

        user = self.users[username]
        if not user.check_password(old_password):
            return False, "Current password is incorrect."

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long."

        user.password_hash = User._hash_password(new_password)
        self.save_users()

        return True, "Password changed successfully."

    def get_current_user(self) -> Optional[User]:
        """Get the currently logged-in user."""
        return self.current_user

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self.current_user is not None

    def is_admin(self) -> bool:
        """Check if the current user is an admin."""
        return self.current_user is not None and self.current_user.role == UserRole.ADMIN

    def is_student(self) -> bool:
        """Check if the current user is a student."""
        return self.current_user is not None and self.current_user.role == UserRole.STUDENT
