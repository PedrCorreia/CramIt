"""Hub view for displaying week/month/year activity timelines and statistics."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QHBoxLayout, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from widgets.donut_widget import DonutWidget
from widgets.timeline_widget import WeekTimelineWidget
from utils.date_helpers import (
    filter_activities_by_week,
    calculate_activity_stats,
    calculate_stats_by_type
)
from utils.colors import ACTIVITY_COLORS


class HubWidget(QWidget):
    """Hub widget with week/month/year views and timeline visualization."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # View switcher buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_week = QPushButton("Week")
        self.btn_month = QPushButton("Month")
        self.btn_year = QPushButton("Year")
        
        btn_layout.addWidget(self.btn_week)
        btn_layout.addWidget(self.btn_month)
        btn_layout.addWidget(self.btn_year)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Stacked widget for different time period views
        self.hub_stack = QStackedWidget()
        self.week_view = self._create_week_view()
        self.month_view = QLabel("Month Hub:\nMonthly circular graph\n(planned vs executed for the month)")
        self.year_view = QLabel("Year Hub:\n12 circular graphs (one per month)\n+ yearly total")
        
        self.hub_stack.addWidget(self.week_view)
        self.hub_stack.addWidget(self.month_view)
        self.hub_stack.addWidget(self.year_view)
        
        layout.addWidget(self.hub_stack)
        
        # Connect buttons
        self.btn_week.clicked.connect(self.show_week)
        self.btn_month.clicked.connect(self.show_month)
        self.btn_year.clicked.connect(self.show_year)
        
        # Default to week view
        self.show_week()
    
    def _create_week_view(self):
        """Create the week view with dashboard and timeline."""
        week_widget = QWidget()
        week_layout = QVBoxLayout(week_widget)
        week_layout.setContentsMargins(0, 0, 0, 0)
        week_layout.setSpacing(15)
        
        # Dashboard section at top
        dashboard = self._create_dashboard()
        week_layout.addWidget(dashboard)
        
        # Donut graphs section
        donut_section = self._create_donut_section()
        week_layout.addWidget(donut_section)
        
        # Timeline widget (no scroll, fixed size)
        self.timeline_widget = WeekTimelineWidget()
        week_layout.addWidget(self.timeline_widget)
        
        return week_widget
    
    def _create_donut_section(self):
        """Create section with donut graphs for each activity type."""
        donut_frame = QFrame()
        donut_frame.setFrameShape(QFrame.Shape.StyledPanel)
        donut_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(donut_frame)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create donut widgets for each type (using centralized colors)
        self.work_donut = DonutWidget("Work", ACTIVITY_COLORS["work"])
        self.school_donut = DonutWidget("School", ACTIVITY_COLORS["school"])
        self.hobbies_donut = DonutWidget("Hobbies", ACTIVITY_COLORS["hobbies"])
        
        layout.addWidget(self.work_donut)
        layout.addWidget(self.school_donut)
        layout.addWidget(self.hobbies_donut)
        
        return donut_frame
    
    def _create_dashboard(self):
        """Create dashboard with week statistics."""
        dashboard = QFrame()
        dashboard.setFrameShape(QFrame.Shape.StyledPanel)
        dashboard.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QGridLayout(dashboard)
        layout.setSpacing(15)
        
        # Statistics labels
        self.week_total_label = QLabel("Total: 0h")
        self.week_completed_label = QLabel("Completed: 0h")
        self.week_pending_label = QLabel("Pending: 0h")
        self.week_activities_label = QLabel("Activities: 0")
        
        # Style labels
        for label in [self.week_total_label, self.week_completed_label, 
                     self.week_pending_label, self.week_activities_label]:
            label.setStyleSheet("font-size: 12px; color: #ffffff;")
        
        layout.addWidget(self.week_total_label, 0, 0)
        layout.addWidget(self.week_completed_label, 0, 1)
        layout.addWidget(self.week_pending_label, 0, 2)
        layout.addWidget(self.week_activities_label, 0, 3)
        layout.setColumnStretch(4, 1)
        
        return dashboard
    
    def show_week(self):
        """Switch to week view."""
        self.hub_stack.setCurrentWidget(self.week_view)
    
    def show_month(self):
        """Switch to month view."""
        self.hub_stack.setCurrentWidget(self.month_view)
    
    def show_year(self):
        """Switch to year view."""
        self.hub_stack.setCurrentWidget(self.year_view)
    
    def update_activities(self, activities):
        """Update the hub views with activity data."""
        self.timeline_widget.set_activities(activities)
        self._update_dashboard(activities)
        self._update_donuts(activities)
    
    def _update_donuts(self, activities):
        """Update donut graphs with activity data."""
        week_activities = filter_activities_by_week(activities)
        
        # Calculate totals by type using helper function
        work_completed, work_total = calculate_stats_by_type(week_activities, "work")
        school_completed, school_total = calculate_stats_by_type(week_activities, "school")
        hobbies_completed, hobbies_total = calculate_stats_by_type(week_activities, "hobbies")
        
        # Update donut colors based on completion
        from utils.colors import EXECUTED_COLORS
        self.work_donut.color = EXECUTED_COLORS["work"] if work_completed > 0 else ACTIVITY_COLORS["work"]
        self.school_donut.color = EXECUTED_COLORS["school"] if school_completed > 0 else ACTIVITY_COLORS["school"]
        self.hobbies_donut.color = EXECUTED_COLORS["hobbies"] if hobbies_completed > 0 else ACTIVITY_COLORS["hobbies"]
        
        self.work_donut.set_values(work_completed, work_total)
        self.school_donut.set_values(school_completed, school_total)
        self.hobbies_donut.set_values(hobbies_completed, hobbies_total)
    
    def _update_dashboard(self, activities):
        """Update dashboard statistics for current week."""
        week_activities = filter_activities_by_week(activities)
        total_hours, completed_hours, pending_hours = calculate_activity_stats(week_activities)
        
        self.week_total_label.setText(f"Total: {total_hours:.1f}h")
        self.week_completed_label.setText(f"Completed: {completed_hours:.1f}h")
        self.week_pending_label.setText(f"Pending: {pending_hours:.1f}h")
        self.week_activities_label.setText(f"Activities: {len(week_activities)}")
