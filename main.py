"""
Main entry point for the University Course Registration System - Student Version.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This is the main entry point to run the University Course Registration System.
It initializes the login screen and then the main GUI after successful authentication.

This version focuses on student features only - no admin features.

Usage:
    python main.py

Demo Login Credentials:
    Username: student
    Password: student123
    Student ID: S001

Or create a new account with your own Student ID!

Author: Gideon
Date: 10/24/2025
"""

import tkinter as tk
import os
from login_ui import LoginWindow
from gui_final import RegistrationSystemGUI


def on_login_success(auth_system, user):
    """
    Callback function called when login is successful.

    Args:
        auth_system: The authentication system instance
        user: The logged-in user object
    """
    # Close the login window
    for widget in root.winfo_children():
        widget.destroy()

    # Get the directory where this script is located (for CSV file storage)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create and show the main application GUI
    app = RegistrationSystemGUI(root, auth_system, user, data_directory=script_dir)


def main():
    """
    Main function to run the University Course Registration System application.

    This function:
    1. Creates the main Tkinter window
    2. Shows the login screen
    3. After successful login, shows the main application GUI
    4. Starts the GUI event loop
    """
    global root

    # Create the main window
    root = tk.Tk()

    # Show the login window
    login_window = LoginWindow(root, on_login_success)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    """
    Entry point when the script is run directly.
    """
    print("="*80)
    print("Banner Web - Student Version")
    print("CS 236: Data Structures and Algorithms - Final Lab Assignment #5")
    print("="*80)
    print("\nStarting the application...")
    print(f"Data files will be stored in: {os.path.dirname(os.path.abspath(__file__))}")
    print("\nTo get started:")
    print("   1. Create a new account with your Student ID")
    print("   2. Or use the demo account:")
    print("      Username: 'student', Password: 'student123', Student ID: 'S001'")
    print("\nFeatures:")
    print("   - View your enrolled courses")
    print("   - Enroll in new courses")
    print("   - Drop courses")
    print("   - Browse all available courses")
    print("="*80)

    # Run the main application
    main()
