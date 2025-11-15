"""
Enrollment System module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module contains the EnrollmentSystem class that manages student-course
registrations and maintains records with CSV file persistence.

Uses Dictionary data structures for O(1) lookups of students and courses by ID.
Implements file I/O with CSV format for data persistence.

Author: Chinyemba
Date: 10/24/2025
"""

import csv
import os
from typing import Dict, Tuple
from student import Student
from course import Course


class EnrollmentSystem:
    """
    Manages student-course registrations and maintains records.

    Attributes:
        data_directory (str): Directory where CSV files are stored
        students (Dict[str, Student]): Dictionary mapping student IDs to Student objects
                                       Uses Dict for O(1) student lookup
        courses (Dict[str, Course]): Dictionary mapping course IDs to Course objects
                                     Uses Dict for O(1) course lookup
    """

    def __init__(self, data_directory: str = "."):
        """
        Initialize the enrollment system and load existing data from CSV files.

        Args:
            data_directory (str): Directory where CSV files are stored (default: current directory)
        """
        self.data_directory = data_directory
        # Use Dictionaries for O(1) lookups by ID
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        # Load existing data from CSV files
        self.load_data()

    def _get_file_path(self, filename: str) -> str:
        """
        Get the full path for a data file.

        Args:
            filename: Name of the file

        Returns:
            Full path to the file
        """
        return os.path.join(self.data_directory, filename)

    def load_data(self) -> None:
        """
        Load student and course data from CSV files into memory.
        Reads courses.csv and students.csv from the data directory.
        """
        # Load courses from CSV file
        courses_file = self._get_file_path('courses.csv')
        if os.path.exists(courses_file):
            try:
                with open(courses_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Create Course object from CSV row
                        course = Course(
                            row['course_id'],
                            row['name'],
                            row['instructor'],
                            int(row.get('max_students', 30)),
                            row.get('days', ''),
                            row.get('time', ''),
                            row.get('location', '')
                        )
                        # Parse enrolled students (semicolon-separated list)
                        enrolled = row.get('enrolled_students', '')
                        if enrolled:
                            course.enrolled_students = set(enrolled.split(';'))
                        # Store in dictionary for O(1) lookup
                        self.courses[course.course_id] = course
            except Exception as e:
                print(f"Error loading courses: {e}")

        # Load students
        students_file = self._get_file_path('students.csv')
        if os.path.exists(students_file):
            try:
                with open(students_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        student = Student(row['student_id'], row['name'])
                        # Load registered courses
                        courses = row.get('registered_courses', '')
                        if courses:
                            student.registered_courses = set(courses.split(';'))
                        self.students[student.student_id] = student
            except Exception as e:
                print(f"Error loading students: {e}")

    def save_data(self) -> None:
        """Save student and course data to CSV files."""
        # Save courses
        courses_file = self._get_file_path('courses.csv')
        try:
            with open(courses_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['course_id', 'name', 'instructor', 'max_students', 'enrolled_students', 'days', 'time', 'location']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for course in self.courses.values():
                    writer.writerow({
                        'course_id': course.course_id,
                        'name': course.name,
                        'instructor': course.instructor,
                        'max_students': course.max_students,
                        'enrolled_students': ';'.join(course.enrolled_students),
                        'days': course.days,
                        'time': course.time,
                        'location': course.location
                    })
        except Exception as e:
            print(f"Error saving courses: {e}")

        # Save students
        students_file = self._get_file_path('students.csv')
        try:
            with open(students_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['student_id', 'name', 'registered_courses']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow({
                        'student_id': student.student_id,
                        'name': student.name,
                        'registered_courses': ';'.join(student.registered_courses)
                    })
        except Exception as e:
            print(f"Error saving students: {e}")

        # Save enrollments
        enrollments_file = self._get_file_path('enrollments.csv')
        try:
            with open(enrollments_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['student_id', 'course_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students.values():
                    for course_id in student.registered_courses:
                        writer.writerow({
                            'student_id': student.student_id,
                            'course_id': course_id
                        })
        except Exception as e:
            print(f"Error saving enrollments: {e}")

    def register_student(self, student_id: str, name: str) -> Tuple[bool, str]:
        """
        Register a new student in the system.

        Args:
            student_id: Unique ID for the student
            name: Name of the student

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not student_id or not name:
            return False, "Student ID and name cannot be empty."

        if student_id in self.students:
            return False, f"Student ID {student_id} already exists."

        self.students[student_id] = Student(student_id, name)
        self.save_data()
        return True, f"Student {name} registered successfully with ID {student_id}."

    def add_course(self, course_id: str, name: str, instructor: str, max_students: int = 30) -> Tuple[bool, str]:
        """
        Add a new course to the system.

        Args:
            course_id: Unique ID for the course
            name: Name of the course
            instructor: Instructor name
            max_students: Maximum number of students

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not course_id or not name or not instructor:
            return False, "Course ID, name, and instructor cannot be empty."

        if course_id in self.courses:
            return False, f"Course ID {course_id} already exists."

        try:
            max_students = int(max_students)
            if max_students <= 0:
                return False, "Maximum students must be a positive number."
        except ValueError:
            return False, "Maximum students must be a valid number."

        self.courses[course_id] = Course(course_id, name, instructor, max_students)
        self.save_data()
        return True, f"Course {name} added successfully with ID {course_id}."

    def enroll_student(self, student_id: str, course_id: str) -> Tuple[bool, str]:
        """
        Enroll a student in a course.

        Args:
            student_id: ID of the student
            course_id: ID of the course

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate student exists
        if student_id not in self.students:
            return False, f"Student ID {student_id} not found."

        # Validate course exists
        if course_id not in self.courses:
            return False, f"Course ID {course_id} not found."

        student = self.students[student_id]
        course = self.courses[course_id]

        # Check if already enrolled
        if course_id in student.registered_courses:
            return False, f"Student is already enrolled in {course.name}."

        # Check if course is full
        if course.is_full():
            return False, f"Course {course.name} is full. No seats available."

        # Check for schedule conflicts with enrolled courses
        for enrolled_course_id in student.registered_courses:
            if enrolled_course_id in self.courses:
                enrolled_course = self.courses[enrolled_course_id]
                if course.has_schedule_conflict(enrolled_course):
                    return False, (f"⚠️ SCHEDULE CONFLICT: {course.name} ({course.days} {course.time}) "
                                   f"conflicts with {enrolled_course.name} ({enrolled_course.days} {enrolled_course.time}). "
                                   f"You cannot register for courses that meet at the same time.")

        # Enroll the student
        student.add_course(course_id)
        course.add_student(student_id)
        self.save_data()

        return True, f"Student {student.name} successfully enrolled in {course.name}."

    def drop_course(self, student_id: str, course_id: str) -> Tuple[bool, str]:
        """
        Drop a student from a course.

        Args:
            student_id: ID of the student
            course_id: ID of the course

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate student exists
        if student_id not in self.students:
            return False, f"Student ID {student_id} not found."

        # Validate course exists
        if course_id not in self.courses:
            return False, f"Course ID {course_id} not found."

        student = self.students[student_id]
        course = self.courses[course_id]

        # Check if student is enrolled
        if course_id not in student.registered_courses:
            return False, f"Student is not enrolled in {course.name}."

        # Drop the course
        student.remove_course(course_id)
        course.remove_student(student_id)
        self.save_data()

        return True, f"Student {student.name} successfully dropped {course.name}."

    def view_available_courses(self) -> str:
        """
        Get a formatted string of all available courses.

        Returns:
            Formatted string with course information
        """
        if not self.courses:
            return "No courses available."

        result = "Available Courses:\n" + "="*80 + "\n"
        for course in self.courses.values():
            available = course.get_available_seats()
            status = "FULL" if course.is_full() else f"{available} seats available"
            result += f"{course.course_id}: {course.name}\n"
            result += f"  Instructor: {course.instructor}\n"
            result += f"  Capacity: {len(course.enrolled_students)}/{course.max_students} ({status})\n"
            result += "-"*80 + "\n"
        return result

    def view_student_courses(self, student_id: str) -> Tuple[bool, str]:
        """
        View courses for a specific student.

        Args:
            student_id: ID of the student

        Returns:
            Tuple of (success: bool, message: str)
        """
        if student_id not in self.students:
            return False, f"Student ID {student_id} not found."

        student = self.students[student_id]

        if not student.registered_courses:
            return True, f"Student {student.name} is not enrolled in any courses."

        result = f"Courses for {student.name} (ID: {student_id}):\n" + "="*80 + "\n"
        for course_id in student.registered_courses:
            if course_id in self.courses:
                course = self.courses[course_id]
                result += f"{course.course_id}: {course.name}\n"
                result += f"  Instructor: {course.instructor}\n"
                result += "-"*80 + "\n"

        return True, result

    def get_all_students(self) -> Dict[str, Student]:
        """
        Get all registered students.

        Returns:
            Dictionary of all students
        """
        return self.students

    def get_all_courses(self) -> Dict[str, Course]:
        """
        Get all available courses.

        Returns:
            Dictionary of all courses
        """
        return self.courses

    def get_student(self, student_id: str) -> Student:
        """
        Get a specific student by ID.

        Args:
            student_id: ID of the student

        Returns:
            Student object or None if not found
        """
        return self.students.get(student_id)

    def get_course(self, course_id: str) -> Course:
        """
        Get a specific course by ID.

        Args:
            course_id: ID of the course

        Returns:
            Course object or None if not found
        """
        return self.courses.get(course_id)

    def get_formatted_schedule(self, student_id: str) -> str:
        """
        Generate a formatted printable schedule for a student.

        Args:
            student_id: ID of the student

        Returns:
            Formatted schedule string organized by day and time
        """
        if student_id not in self.students:
            return "Student not found."

        student = self.students[student_id]

        if not student.registered_courses:
            return "No courses enrolled."

        # Collect courses with schedule info
        scheduled_courses = []
        for course_id in student.registered_courses:
            if course_id in self.courses:
                course = self.courses[course_id]
                if course.days and course.time:
                    scheduled_courses.append(course)

        if not scheduled_courses:
            return "No courses with schedule information."

        # Create header
        header = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           STUDENT COURSE SCHEDULE                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Student: {student.name}
Student ID: {student_id}
Total Courses: {len(scheduled_courses)}

"""

        # Organize by day
        day_map = {
            'M': 'Monday',
            'T': 'Tuesday',
            'W': 'Wednesday',
            'Th': 'Thursday',
            'F': 'Friday'
        }

        # Build weekly schedule
        schedule_by_day = {'M': [], 'T': [], 'W': [], 'Th': [], 'F': []}

        for course in scheduled_courses:
            days = course.days
            # Parse days string (e.g., "MWF" or "TTh")
            if 'Th' in days:
                schedule_by_day['Th'].append(course)
                days = days.replace('Th', '')
            for day in days:
                if day in schedule_by_day:
                    schedule_by_day[day].append(course)

        # Format weekly schedule
        body = "=" * 80 + "\n"
        body += "                             WEEKLY SCHEDULE\n"
        body += "=" * 80 + "\n\n"

        day_order = ['M', 'T', 'W', 'Th', 'F']
        for day_abbr in day_order:
            day_name = day_map.get(day_abbr, day_abbr)
            courses = schedule_by_day[day_abbr]

            body += f"┌─ {day_name} " + "─" * (74 - len(day_name)) + "┐\n"

            if courses:
                # Sort by time
                sorted_courses = sorted(courses, key=lambda c: c.time)
                for course in sorted_courses:
                    body += f"│ {course.time:15} │ {course.course_id:8} │ {course.name[:42]:42} │\n"
                    body += f"│                 │          │ {course.instructor[:42]:42} │\n"
                    body += f"│                 │          │ {course.location[:42]:42} │\n"
            else:
                body += "│                           No classes scheduled                           │\n"

            body += "└" + "─" * 78 + "┘\n\n"

        return header + body
