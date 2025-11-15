"""
Main GUI module for the University Course Registration System.

CS 236: Data Structures and Algorithms - Final Lab Assignment #5

This module provides a modern, card-based user interface for students to:
- View enrolled courses
- Browse available courses
- Enroll in new courses
- Drop existing courses

Features a clean two-tab interface with automatic refresh and inline actions.

Author: Lleyton
Date: 10/24/2025
"""

import tkinter as tk
from tkinter import messagebox
from enrollment_system import EnrollmentSystem


class RegistrationSystemGUI:
    """Beautiful modern GUI with polished design."""

    def __init__(self, root, auth_system, current_user, data_directory: str = "."):
        self.root = root
        self.auth_system = auth_system
        self.current_user = current_user
        self.data_directory = data_directory

        self.setup_window()
        self.system = EnrollmentSystem(data_directory)

        if not self.system.courses:
            self._initialize_sample_data()

        self.current_tab_btn = None
        self.create_widgets()

    def setup_window(self):
        """Configure window."""
        self.root.title(f"Course Registration - {self.current_user.username}")
        self.root.geometry("1150x850")
        self.root.resizable(True, True)
        self.root.minsize(1000, 750)

        # Beautiful color scheme
        self.bg_color = "#f5f7fa"
        self.primary_color = "#4f46e5"  # Indigo
        self.primary_hover = "#4338ca"
        self.success_color = "#10b981"
        self.success_hover = "#059669"
        self.danger_color = "#ef4444"
        self.danger_hover = "#dc2626"
        self.card_bg = "#ffffff"
        self.text_color = "#1e293b"
        self.text_muted = "#64748b"
        self.border_color = "#e2e8f0"

        self.root.configure(bg=self.bg_color)

    def _initialize_sample_data(self):
        """Initialize sample courses."""
        courses = [
            ("CS101", "Introduction to Programming", "Dr. Smith", 30),
            ("CS236", "Data Structures and Algorithms", "Dr. Johnson", 30),
            ("MATH201", "Calculus I", "Prof. Williams", 30),
            ("ENG101", "English Composition", "Dr. Brown", 25),
            ("PHY101", "Physics I", "Prof. Davis", 30),
            ("CS301", "Database Systems", "Dr. Garcia", 25),
            ("MATH301", "Linear Algebra", "Prof. Martinez", 30),
        ]
        for cid, name, instructor, max_s in courses:
            self.system.add_course(cid, name, instructor, max_s)

    def create_widgets(self):
        """Create all widgets."""
        self.create_header()

        # Main content
        main = tk.Frame(self.root, bg=self.bg_color)
        main.pack(fill='both', expand=True, padx=40, pady=30)

        # Navigation
        nav = tk.Frame(main, bg=self.bg_color)
        nav.pack(fill='x', pady=(0, 30))

        self.tab_buttons = {}

        # Tab 1: My Courses
        btn1 = self.create_tab_button(nav, "📚 My Courses", "my_courses")
        btn1.pack(side='left', padx=(0, 15))

        # Tab 2: Browse Courses
        btn2 = self.create_tab_button(nav, "🔍 Browse Courses", "browse")
        btn2.pack(side='left')

        # Content area (create BEFORE switching tabs)
        self.content = tk.Frame(main, bg=self.bg_color)
        self.content.pack(fill='both', expand=True)

        # Activate first tab
        self.switch_tab("my_courses")

    def create_tab_button(self, parent, text, tab_id):
        """Create a styled tab button."""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 11, 'bold'),
            bg=self.card_bg,
            fg=self.text_muted,
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=12,
            bd=0,
            command=lambda: self.switch_tab(tab_id)
        )
        self.tab_buttons[tab_id] = btn
        return btn

    def switch_tab(self, tab_name):
        """Switch between tabs."""
        # Reset all tabs
        for btn in self.tab_buttons.values():
            btn.configure(
                fg=self.text_muted,
                bg=self.card_bg
            )

        # Highlight active
        active_btn = self.tab_buttons[tab_name]
        active_btn.configure(
            fg=self.primary_color,
            bg='#eef2ff'  # Light indigo background
        )

        # Show content
        if tab_name == "my_courses":
            self.show_my_courses()
        else:
            self.show_browse()

    def create_header(self):
        """Create beautiful header."""
        header = tk.Frame(self.root, bg=self.primary_color, height=85)
        header.pack(fill='x')
        header.pack_propagate(False)

        # Title
        tk.Label(
            header,
            text="🎓 Banner Web",
            font=('Segoe UI', 20, 'bold'),
            bg=self.primary_color,
            fg='white'
        ).pack(side='left', padx=40, pady=25)

        # User info
        right = tk.Frame(header, bg=self.primary_color)
        right.pack(side='right', padx=40, pady=25)

        tk.Label(
            right,
            text=f"👤 {self.current_user.username}",
            font=('Segoe UI', 11),
            bg=self.primary_color,
            fg='white'
        ).pack(side='left', padx=(0, 20))

        logout_btn = tk.Button(
            right,
            text="Logout",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.primary_color,
            activebackground='#f1f5f9',
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.logout
        )
        logout_btn.pack()

    def clear_content(self):
        """Clear content area."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_my_courses(self):
        """Show enrolled courses."""
        self.clear_content()

        # Title bar
        title_bar = tk.Frame(self.content, bg=self.bg_color)
        title_bar.pack(fill='x', pady=(0, 25))

        tk.Label(
            title_bar,
            text="My Enrolled Courses",
            font=('Segoe UI', 26, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side='left')

        tk.Label(
            title_bar,
            text=f"Student ID: {self.current_user.student_id}",
            font=('Segoe UI', 12),
            bg=self.bg_color,
            fg=self.text_muted
        ).pack(side='left', padx=20)

        # Print Schedule button
        print_btn = tk.Button(
            title_bar,
            text="🖨️ Print Schedule",
            font=('Segoe UI', 11, 'bold'),
            bg=self.primary_color,
            fg='white',
            activebackground=self.primary_hover,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.show_print_schedule
        )
        print_btn.pack(side='right')

        # Scrollable container
        canvas = tk.Canvas(self.content, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview)

        self.my_container = tk.Frame(canvas, bg=self.bg_color)
        self.my_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.my_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.my_container.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        self.my_container.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_my_courses()

    def refresh_my_courses(self):
        """Refresh enrolled courses."""
        for widget in self.my_container.winfo_children():
            widget.destroy()

        student_id = self.current_user.student_id

        if student_id not in self.system.students:
            self.system.register_student(student_id, self.current_user.username)

        student = self.system.students.get(student_id)

        if not student or not student.registered_courses:
            # Empty state
            empty = tk.Frame(self.my_container, bg=self.card_bg, relief=tk.FLAT)
            empty.pack(fill='x', pady=15)

            tk.Label(
                empty,
                text="📚 No courses enrolled yet",
                font=('Segoe UI', 18, 'bold'),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(pady=40)

            tk.Label(
                empty,
                text="Go to 'Browse Courses' tab to start adding courses",
                font=('Segoe UI', 12),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(pady=(0, 40))
        else:
            # Course cards
            for course_id in student.registered_courses:
                if course_id in self.system.courses:
                    course = self.system.courses[course_id]
                    self.create_my_course_card(course)

    def create_my_course_card(self, course):
        """Create enrolled course card with smaller drop button."""
        # Card with shadow effect
        card_outer = tk.Frame(self.my_container, bg=self.bg_color)
        card_outer.pack(fill='x', pady=12)

        card = tk.Frame(card_outer, bg=self.card_bg, relief=tk.SOLID, bd=1, highlightthickness=0, highlightbackground=self.border_color)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(fill='x', padx=30, pady=25)

        # Left - Course info
        left = tk.Frame(inner, bg=self.card_bg)
        left.pack(side='left', fill='x', expand=True)

        # Top row
        top = tk.Frame(left, bg=self.card_bg)
        top.pack(fill='x', pady=(0, 12))

        tk.Label(
            top,
            text=course.course_id,
            font=('Segoe UI', 10, 'bold'),
            bg=self.primary_color,
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', padx=(0, 12))

        tk.Label(
            top,
            text=course.name,
            font=('Segoe UI', 17, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack(side='left')

        # Details
        details_frame = tk.Frame(left, bg=self.card_bg)
        details_frame.pack(fill='x', pady=(5, 0))

        tk.Label(
            details_frame,
            text=f"👨‍🏫 {course.instructor}",
            font=('Segoe UI', 11),
            bg=self.card_bg,
            fg=self.text_muted
        ).pack(side='left', padx=(0, 20))

        # Show schedule if available
        if course.days and course.time:
            tk.Label(
                details_frame,
                text=f"📅 {course.days}",
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(side='left', padx=(0, 15))

            tk.Label(
                details_frame,
                text=f"🕐 {course.time}",
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(side='left', padx=(0, 15))

            # Show location if available
            if course.location:
                tk.Label(
                    details_frame,
                    text=f"📍 {course.location}",
                    font=('Segoe UI', 11),
                    bg=self.card_bg,
                    fg=self.text_muted
                ).pack(side='left')

        # Right - Smaller Drop button
        drop_btn = tk.Button(
            inner,
            text="Drop",
            font=('Segoe UI', 10, 'bold'),
            bg=self.danger_color,
            fg='white',
            activebackground=self.danger_hover,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda c=course: self.drop_course(c.course_id)
        )
        drop_btn.pack(side='right')

    def show_browse(self):
        """Show browse & enroll."""
        self.clear_content()

        # Title bar
        title_bar = tk.Frame(self.content, bg=self.bg_color)
        title_bar.pack(fill='x', pady=(0, 25))

        tk.Label(
            title_bar,
            text="Browse Courses",
            font=('Segoe UI', 26, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side='left')

        # Scrollable
        canvas = tk.Canvas(self.content, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview)

        self.browse_container = tk.Frame(canvas, bg=self.bg_color)
        self.browse_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.browse_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.browse_container.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        self.browse_container.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_browse()

    def refresh_browse(self):
        """Refresh browse."""
        for widget in self.browse_container.winfo_children():
            widget.destroy()

        student_id = self.current_user.student_id
        enrolled_courses = set()

        if student_id in self.system.students:
            enrolled_courses = self.system.students[student_id].registered_courses

        for course in self.system.courses.values():
            is_enrolled = course.course_id in enrolled_courses
            self.create_browse_card(course, is_enrolled)

    def create_browse_card(self, course, is_enrolled):
        """Create browse course card."""
        # Card
        card_outer = tk.Frame(self.browse_container, bg=self.bg_color)
        card_outer.pack(fill='x', pady=12)

        card = tk.Frame(card_outer, bg=self.card_bg, relief=tk.SOLID, bd=1, highlightthickness=0, highlightbackground=self.border_color)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=self.card_bg)
        inner.pack(fill='x', padx=30, pady=25)

        # Right side - Badges and button
        right = tk.Frame(inner, bg=self.card_bg)
        right.pack(side='right', padx=(15, 0))

        # Status in right frame
        if is_enrolled:
            # Enrolled badge
            tk.Label(
                right,
                text="✓ Enrolled",
                font=('Segoe UI', 9, 'bold'),
                bg=self.success_color,
                fg='white',
                padx=10,
                pady=5
            ).pack(side='top', anchor='e')
        elif not course.is_full():
            # Enroll button (if not enrolled and not full)
            enroll_btn = tk.Button(
                right,
                text="Enroll",
                font=('Segoe UI', 10, 'bold'),
                bg=self.success_color,
                fg='white',
                activebackground=self.success_hover,
                relief=tk.FLAT,
                cursor="hand2",
                padx=20,
                pady=10,
                command=lambda c=course: self.enroll_course(c.course_id)
            )
            enroll_btn.pack(side='top', anchor='e')

        # Left - Course info
        left = tk.Frame(inner, bg=self.card_bg)
        left.pack(side='left', fill='x', expand=True)

        # Top row
        top = tk.Frame(left, bg=self.card_bg)
        top.pack(fill='x', pady=(0, 12))

        tk.Label(
            top,
            text=course.course_id,
            font=('Segoe UI', 10, 'bold'),
            bg=self.primary_color,
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', padx=(0, 12))

        tk.Label(
            top,
            text=course.name,
            font=('Segoe UI', 17, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack(side='left')

        # Details
        details = tk.Frame(left, bg=self.card_bg)
        details.pack(fill='x')

        tk.Label(
            details,
            text=f"👨‍🏫 {course.instructor}",
            font=('Segoe UI', 11),
            bg=self.card_bg,
            fg=self.text_muted
        ).pack(side='left', padx=(0, 25))

        tk.Label(
            details,
            text=f"📊 {len(course.enrolled_students)}/{course.max_students}",
            font=('Segoe UI', 11),
            bg=self.card_bg,
            fg=self.text_muted
        ).pack(side='left', padx=(0, 25))

        # Show schedule if available
        if course.days and course.time:
            tk.Label(
                details,
                text=f"📅 {course.days}",
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(side='left', padx=(0, 15))

            tk.Label(
                details,
                text=f"🕐 {course.time}",
                font=('Segoe UI', 11),
                bg=self.card_bg,
                fg=self.text_muted
            ).pack(side='left', padx=(0, 15))

            # Show location if available
            if course.location:
                tk.Label(
                    details,
                    text=f"📍 {course.location}",
                    font=('Segoe UI', 11),
                    bg=self.card_bg,
                    fg=self.text_muted
                ).pack(side='left')

    def enroll_course(self, course_id):
        """Enroll in course."""
        student_id = self.current_user.student_id

        if student_id not in self.system.students:
            messagebox.showerror("Error", "Student not found in system")
            return

        # Check if student has reached the course limit
        student = self.system.students.get(student_id)
        if student and len(student.registered_courses) >= 6:
            messagebox.showwarning(
                "Course Limit Reached",
                "You cannot enroll in more than 6 courses per semester."
            )
            return

        success, message = self.system.enroll_student(student_id, course_id)

        if success:
            messagebox.showinfo("Success", f"Enrolled in {course_id}")
            self.refresh_my_courses()
            self.refresh_browse()
        else:
            messagebox.showerror("Error", message)

    def drop_course(self, course_id):
        """Drop course."""
        if not messagebox.askyesno("Confirm Drop", f"Drop course {course_id}?"):
            return

        student_id = self.current_user.student_id
        success, message = self.system.drop_course(student_id, course_id)

        if success:
            messagebox.showinfo("✅ Success", message)
            # Auto-refresh to show updated state
            self.show_my_courses()
        else:
            messagebox.showerror("❌ Error", message)

    def show_print_schedule(self):
        """Display printable schedule in a new window."""
        student_id = self.current_user.student_id

        # Get formatted schedule
        schedule_text = self.system.get_formatted_schedule(student_id)

        # Create new window
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Print Schedule")
        schedule_window.geometry("900x700")
        schedule_window.configure(bg='white')

        # Header frame
        header = tk.Frame(schedule_window, bg=self.primary_color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📅 Student Course Schedule",
            font=('Segoe UI', 16, 'bold'),
            bg=self.primary_color,
            fg='white'
        ).pack(side='left', padx=30, pady=15)

        # Button frame
        btn_frame = tk.Frame(header, bg=self.primary_color)
        btn_frame.pack(side='right', padx=30)

        # Print button
        print_btn = tk.Button(
            btn_frame,
            text="🖨️ Print",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.primary_color,
            activebackground='#f1f5f9',
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.print_schedule_dialog(schedule_text)
        )
        print_btn.pack(side='left', padx=(0, 10))

        # Close button
        close_btn = tk.Button(
            btn_frame,
            text="Close",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.primary_color,
            activebackground='#f1f5f9',
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=schedule_window.destroy
        )
        close_btn.pack(side='left')

        # Schedule content with scrollbar
        text_frame = tk.Frame(schedule_window, bg='white')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')

        text_widget = tk.Text(
            text_frame,
            font=('Courier New', 10),
            bg='white',
            fg='#1e293b',
            wrap=tk.NONE,
            yscrollcommand=scrollbar.set,
            padx=15,
            pady=15
        )
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)

        # Enable mouse wheel scrolling for Text widget
        def on_text_mousewheel(event):
            text_widget.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"

        text_widget.bind("<MouseWheel>", on_text_mousewheel)

        # Insert schedule text
        text_widget.insert('1.0', schedule_text)
        text_widget.config(state='disabled')  # Make read-only

    def print_schedule_dialog(self, schedule_text):
        """Handle printing of schedule."""
        try:
            # Try to open print dialog (Windows)
            import tempfile
            import os

            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(schedule_text)
                temp_path = f.name

            # Open with default text editor for printing
            os.startfile(temp_path, 'print')
            messagebox.showinfo("Print", "Schedule sent to printer.\nA print dialog should open shortly.")
        except Exception as e:
            # Fallback: just show message
            messagebox.showinfo(
                "Print Schedule",
                "To print:\n1. Select all text (Ctrl+A)\n2. Copy (Ctrl+C)\n3. Paste into a text editor\n4. Print from there"
            )

    def logout(self):
        """Logout and return to login screen."""
        from login_ui import LoginWindow

        # Logout from auth system
        self.auth_system.logout()

        # Destroy all current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Show login window again
        def on_login_success(auth_system, user):
            """Callback when user logs in again."""
            # Clear the login window
            for widget in self.root.winfo_children():
                widget.destroy()
            # Create new registration GUI
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            RegistrationSystemGUI(self.root, auth_system, user, data_directory=script_dir)

        LoginWindow(self.root, on_login_success)
