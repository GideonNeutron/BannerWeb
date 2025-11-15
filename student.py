"""
Student class module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module contains the Student class that represents a student in the system.
Uses a Set data structure for O(1) course membership lookups.

Author: Gideon
Date: 10/24/2025
"""

from typing import Set


class Student:
    """
    Represents a student in the university system.

    Attributes:
        student_id (str): Unique identifier for the student
        name (str): Name of the student
        registered_courses (Set[str]): Set of course IDs the student is enrolled in
                                      Uses Set for O(1) membership testing
    """

    def __init__(self, student_id: str, name: str):
        """
        Initialize a Student object.

        Args:
            student_id (str): Unique identifier for the student
            name (str): Name of the student
        """
        self.student_id = student_id
        self.name = name
        # Use Set for O(1) membership testing and automatic duplicate prevention
        self.registered_courses: Set[str] = set()

    def add_course(self, course_id: str) -> None:
        """
        Add a course to the student's registered courses.

        Args:
            course_id: ID of the course to add
        """
        self.registered_courses.add(course_id)

    def remove_course(self, course_id: str) -> None:
        """
        Remove a course from the student's registered courses.

        Args:
            course_id: ID of the course to remove
        """
        self.registered_courses.discard(course_id)

    def get_course_count(self) -> int:
        """
        Get the number of courses the student is enrolled in.

        Returns:
            Number of registered courses
        """
        return len(self.registered_courses)

    def is_enrolled_in(self, course_id: str) -> bool:
        """
        Check if the student is enrolled in a specific course.

        Args:
            course_id: ID of the course to check

        Returns:
            True if enrolled, False otherwise
        """
        return course_id in self.registered_courses

    def __str__(self) -> str:
        """String representation of the student."""
        courses = ', '.join(self.registered_courses) if self.registered_courses else 'None'
        return f"Student ID: {self.student_id}, Name: {self.name}, Courses: {courses}"

    def __repr__(self) -> str:
        """Developer-friendly representation of the student."""
        return f"Student(student_id='{self.student_id}', name='{self.name}', courses={len(self.registered_courses)})"
