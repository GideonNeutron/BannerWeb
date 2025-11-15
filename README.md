# Banner Web - Student Course Registration System

**CS 236: Data Structures and Algorithms - Final Lab Assignment #5**

A modern, web-inspired course registration system built with Python and Tkinter, featuring secure authentication, real-time enrollment management, and a clean card-based user interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Architecture](#technical-architecture)
- [File Structure](#file-structure)
- [Data Structures](#data-structures)
- [Security](#security)
- [CS 236 Requirements Coverage](#cs-236-requirements-coverage)
- [Author](#author)

---

## Overview

Banner Web is a university course registration system that allows students to browse available courses, enroll in classes, and manage their course schedule. The application implements Object-Oriented Programming principles, efficient data structures, and persistent file storage.

**Key Highlights:**
- 🎓 Modern card-based UI inspired by web applications
- 🔐 Secure authentication with SHA-256 password hashing
- 💾 CSV-based persistent data storage
- ⚡ O(1) lookups using Dictionary and Set data structures
- 🎨 Clean, professional interface with Tkinter

---

## Features

### Student Features
- **Secure Login/Registration**: Create accounts with unique Student IDs
- **Browse Courses**: View all available courses with real-time seat availability
- **Enroll in Courses**: One-click enrollment with automatic validation
- **Drop Courses**: Remove courses from your schedule
- **My Courses**: View all currently enrolled courses
- **Capacity Management**: See available seats and enrollment status

### System Features
- Unique Student ID validation
- Automatic seat availability tracking
- Real-time UI updates after enrollment/drop actions
- Data persistence across sessions
- Form validation and error handling

---

## Quick Start

### Demo Credentials
```
Username: student
Password: student123
Student ID: S001
```

### Run the Application
```bash
python main.py
```

---

## Installation

### Requirements
- Python 3.13 or higher
- Tkinter (usually included with Python)

### Setup Steps

1. **Navigate to the project directory**
   ```bash
   cd C:\Users\chiny\Code\CourseReg
   ```

2. **Install Python 3.13** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure "Add Python to PATH" is checked during installation

3. **Verify Installation**
   ```bash
   python --version
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

---

## Usage

### Creating an Account

1. Launch the application
2. Click the **CREATE ACCOUNT** button
3. Fill in:
   - Username (unique)
   - Password (min 6 characters)
   - Confirm Password
   - Student ID (unique, e.g., "S001")
4. Click **REGISTER**
5. You'll be redirected to the login screen

### Logging In

1. Enter your **Username**, **Password**, and **Student ID**
2. Click **LOGIN**
3. You'll be directed to the main application

### Browsing Courses

1. Navigate to the **Browse Courses** tab
2. View available courses with:
   - Course ID and name
   - Instructor information
   - Enrollment status (seats available/full)
   - Current enrollment count

### Enrolling in a Course

1. In the **Browse Courses** tab
2. Find a course with available seats
3. Click the **Enroll** button
4. Confirmation message will appear
5. Course will show "✓ Enrolled" badge

### Dropping a Course

1. Go to **My Courses** tab
2. Find the course you want to drop
3. Click the **Drop** button
4. Confirm the action
5. Course will be removed from your schedule

---

## Technical Architecture

### Object-Oriented Design

**Classes:**
- `Student`: Represents a student with enrolled courses
- `Course`: Represents a course with capacity management
- `EnrollmentSystem`: Manages students, courses, and enrollments
- `AuthenticationSystem`: Handles user accounts and authentication
- `LoginWindow`: Login/registration UI
- `RegistrationSystemGUI`: Main application interface

### MVC-Like Pattern
- **Models**: `Student`, `Course`, `User`
- **Business Logic**: `EnrollmentSystem`, `AuthenticationSystem`
- **Views**: `LoginWindow`, `RegistrationSystemGUI`

---

## File Structure

```
CourseReg/
├── main.py                  # Application entry point
├── student.py               # Student model class
├── course.py                # Course model class
├── enrollment_system.py     # Enrollment business logic
├── auth.py                  # Authentication system
├── login_ui.py             # Login/registration interface
├── gui_final.py            # Main application GUI
├── __init__.py             # Package initialization
├── README.md               # This file
├── courses.csv             # Course data (auto-generated)
├── students.csv            # Student data (auto-generated)
├── enrollments.csv         # Enrollment records (auto-generated)
└── users_auth.csv          # User credentials (auto-generated)
```

---

## Data Structures

### Dictionary (Hash Map)
**Purpose**: O(1) lookups for students and courses by ID

```python
self.students: Dict[str, Student] = {}
self.courses: Dict[str, Course] = {}
```

**Complexity**:
- Insert: O(1)
- Lookup: O(1)
- Delete: O(1)

### Set
**Purpose**: O(1) membership testing and automatic duplicate prevention

```python
self.registered_courses: Set[str] = set()
self.enrolled_students: Set[str] = set()
```

**Complexity**:
- Add: O(1)
- Contains: O(1)
- Remove: O(1)

### Why These Data Structures?

**Dictionaries** allow instant lookups of students and courses without iterating through lists. This is crucial when checking enrollment status or retrieving course information.

**Sets** ensure:
- No duplicate enrollments
- Fast membership checking (is student enrolled?)
- Automatic uniqueness constraints

---

## Security

### Password Protection
- **SHA-256 Hashing**: Passwords are never stored in plain text
- **Salted Hashing**: Uses Python's `hashlib` library
- **Validation**: Minimum 6-character password requirement

### Data Validation
- **Unique Student IDs**: System prevents duplicate Student IDs
- **Unique Usernames**: Each username must be unique
- **Capacity Checks**: Prevents over-enrollment in courses
- **Input Sanitization**: All fields are validated before processing

---

## CS 236 Requirements Coverage

✅ **Object-Oriented Programming**
- Student, Course, EnrollmentSystem, AuthenticationSystem classes
- Encapsulation of data and methods
- Clean separation of concerns

✅ **Data Structures**
- Dictionaries for O(1) student/course lookups
- Sets for O(1) enrollment membership testing
- Efficient algorithms for common operations

✅ **File I/O**
- CSV read/write for persistent storage
- Automatic data loading on startup
- Save operations after each modification

✅ **User Interface**
- Tkinter GUI with modern design
- Interactive elements (buttons, tabs, cards)
- Real-time feedback and validation

✅ **Error Handling**
- Try-catch blocks for file operations
- Input validation with user-friendly messages
- Graceful handling of edge cases

---

## Author

**CS 236 Student**  
Date: 2024  
Assignment: Final Lab #5 - Course Registration System

---

## Support

For issues or questions:
1. Review this README documentation
2. Check the code comments in each module
3. Verify Python 3.13 is installed correctly
4. Ensure CSV files have proper permissions

---

**Enjoy using Banner Web!** 🎓
