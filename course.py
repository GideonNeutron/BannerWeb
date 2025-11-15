"""
Course class module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module contains the Course class that represents a course in the system.
Uses a Set data structure for O(1) student enrollment lookups and automatic
duplicate prevention.

Author: Chinyemba
Date: 10/24/2025
"""

from typing import Set


class Course:
    """
    Represents a course in the university system.

    Features:
        course_id (str): Unique identifier for the course (e.g., "CS101")
        name (str): Name of the course (e.g., "Introduction to Programming")
        instructor (str): Name of the instructor teaching the course
        enrolled_students (Set[str]): Set of student IDs enrolled in this course
                                      Uses Set for O(1) membership testing
        max_students (int): Maximum capacity of the course (default: 30)
        days (str): Days the course meets (e.g., "MWF", "TTh")
        time (str): Time the course meets (e.g., "9:00-10:15")
        location (str): Building and room where course is held (e.g., "Engineering 201")
    """

    def __init__(self, course_id: str, name: str, instructor: str, max_students: int = 30,
                 days: str = "", time: str = "", location: str = ""):
        """
        Initialize a Course object with course details and enrollment tracking.

        Args:
            course_id (str): Unique identifier for the course
            name (str): Name of the course
            instructor (str): Name of the instructor
            max_students (int): Maximum number of students allowed (default: 30)
            days (str): Days the course meets (e.g., "MWF", "TTh")
            time (str): Time the course meets (e.g., "9:00-10:15")
            location (str): Building and room where course is held (e.g., "Engineering 201")
        """
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        # Use Set for O(1) lookups and automatic duplicate prevention
        self.enrolled_students: Set[str] = set()
        self.max_students = max_students
        self.days = days
        self.time = time
        self.location = location

    def add_student(self, student_id: str) -> bool:
        """
        Add a student to the course.

        Args:
            student_id: ID of the student to add

        Returns:
            True if student was added, False if course is full
        """
        if len(self.enrolled_students) >= self.max_students:
            return False
        self.enrolled_students.add(student_id)
        return True

    def remove_student(self, student_id: str) -> None:
        """
        Remove a student from the course.

        Args:
            student_id: ID of the student to remove
        """
        self.enrolled_students.discard(student_id)

    def is_full(self) -> bool:
        """
        Check if the course has reached maximum capacity.

        Returns:
            True if course is full, False otherwise
        """
        return len(self.enrolled_students) >= self.max_students

    def get_available_seats(self) -> int:
        """
        Get the number of available seats in the course.

        Returns:
            Number of available seats
        """
        return self.max_students - len(self.enrolled_students)

    def get_enrollment_count(self) -> int:
        """
        Get the number of students enrolled in the course.

        Returns:
            Number of enrolled students
        """
        return len(self.enrolled_students)

    def is_student_enrolled(self, student_id: str) -> bool:
        """
        Check if a specific student is enrolled in the course.

        Args:
            student_id: ID of the student to check

        Returns:
            True if enrolled, False otherwise
        """
        return student_id in self.enrolled_students

    def has_schedule_conflict(self, other_course: 'Course') -> bool:
        """
        Check if this course has a scheduling conflict with another course.

        Args:
            other_course: Another course to check for conflicts

        Returns:
            True if there is a time conflict, False otherwise
        """
        # If either course doesn't have schedule info, no conflict
        if not self.days or not self.time or not other_course.days or not other_course.time:
            return False

        # Check if courses share any common days
        if not self._has_common_days(other_course.days):
            return False

        # If they share days, check if times overlap
        return self._times_overlap(self.time, other_course.time)

    def _has_common_days(self, other_days: str) -> bool:
        """
        Check if this course shares any days with another course.

        Args:
            other_days: Days string from another course (e.g., "MWF")

        Returns:
            True if courses share at least one day
        """
        self_days = set(self.days)
        other_days_set = set(other_days)
        return len(self_days.intersection(other_days_set)) > 0

    def _times_overlap(self, time1: str, time2: str) -> bool:
        """
        Check if two time ranges overlap.

        Args:
            time1: First time range (e.g., "9:00-10:15")
            time2: Second time range (e.g., "10:30-11:45")

        Returns:
            True if times overlap, False otherwise
        """
        try:
            # Parse time ranges
            start1, end1 = self._parse_time_range(time1)
            start2, end2 = self._parse_time_range(time2)

            # Check if ranges overlap: start1 < end2 and start2 < end1
            return start1 < end2 and start2 < end1
        except:
            # If parsing fails, assume no conflict
            return False

    def _parse_time_range(self, time_range: str) -> tuple:
        """
        Parse a time range string into start and end minutes.

        Args:
            time_range: Time range string (e.g., "9:00-10:15")

        Returns:
            Tuple of (start_minutes, end_minutes) from midnight
        """
        start_str, end_str = time_range.split('-')
        start_minutes = self._time_to_minutes(start_str.strip())
        end_minutes = self._time_to_minutes(end_str.strip())
        return start_minutes, end_minutes

    def _time_to_minutes(self, time_str: str) -> int:
        """
        Convert a time string to minutes from midnight.

        Args:
            time_str: Time string (e.g., "9:00" or "10:15")

        Returns:
            Number of minutes from midnight
        """
        hour, minute = map(int, time_str.split(':'))
        return hour * 60 + minute

    def __str__(self) -> str:
        """String representation of the course."""
        return (f"Course ID: {self.course_id}, Name: {self.name}, "
                f"Instructor: {self.instructor}, "
                f"Enrolled: {len(self.enrolled_students)}/{self.max_students}")

    def __repr__(self) -> str:
        """Developer-friendly representation of the course."""
        return (f"Course(course_id='{self.course_id}', name='{self.name}', "
                f"instructor='{self.instructor}', enrolled={len(self.enrolled_students)}/{self.max_students})")
