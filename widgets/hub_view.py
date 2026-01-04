"""Hub view for displaying week/month/year activity timelines and statistics."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QHBoxLayout, QFrame, QGridLayout
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
from widgets.donut_widget import DonutWidget
from widgets.timeline_widget import WeekTimelineWidget


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
        
        # Create donut widgets for each type
        self.work_donut = DonutWidget("Work", QColor("#4a5568"))
        self.school_donut = DonutWidget("School", QColor("#2563eb"))
        self.hobbies_donut = DonutWidget("Hobbies", QColor("#7c3aed"))
        
        layout.addWidget(self.work_donut)
        layout.addWidget(self.school_donut)
        layout.addWidget(self.hobbies_donut)
        layout.addStretch()
        
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
        # Get current week
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        
        # Filter activities for this week
        week_activities = [a for a in activities 
                          if week_start <= a.start < week_end]
        
        # Calculate totals by type
        work_total = sum(a.planned_hours for a in week_activities if a.type == "work")
        work_completed = sum(a.planned_hours for a in week_activities if a.type == "work" and a.executed)
        
        school_total = sum(a.planned_hours for a in week_activities if a.type == "school")
        school_completed = sum(a.planned_hours for a in week_activities if a.type == "school" and a.executed)
        
        hobbies_total = sum(a.planned_hours for a in week_activities if a.type == "hobbies")
        hobbies_completed = sum(a.planned_hours for a in week_activities if a.type == "hobbies" and a.executed)
        
        self.work_donut.set_values(work_completed, work_total)
        self.school_donut.set_values(school_completed, school_total)
        self.hobbies_donut.set_values(hobbies_completed, hobbies_total)
    
    def _update_dashboard(self, activities):
        """Update dashboard statistics for current week."""
        # Get current week
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        
        # Filter activities for this week
        week_activities = [a for a in activities 
                          if week_start <= a.start < week_end]
        
        total_hours = sum(a.planned_hours for a in week_activities)
        completed_hours = sum(a.planned_hours for a in week_activities if a.executed)
        pending_hours = total_hours - completed_hours
        
        self.week_total_label.setText(f"Total: {total_hours:.1f}h")
        self.week_completed_label.setText(f"Completed: {completed_hours:.1f}h")
        self.week_pending_label.setText(f"Pending: {pending_hours:.1f}h")
        self.week_activities_label.setText(f"Activities: {len(week_activities)}")


class WeekTimelineWidget(QWidget):
    """Custom widget for displaying week timeline with activities."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activities = []
        self.setMinimumHeight(500)
        self.setMaximumHeight(500)
        
    def set_activities(self, activities):
        """Set activities to display on timeline."""
        self.activities = activities
        self.update()
    
    def paintEvent(self, event):
        """Paint the timeline and activities."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get current week
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        # Dimensions - calculate based on available width
        width = self.width()
        day_height = 65  # More spaced
        header_height = 50
        day_label_width = 150
        timeline_x = day_label_width
        timeline_width = width - day_label_width - 20
        hour_width = timeline_width / 24
        
        # Draw day rows
        for day_idx in range(7):
            day_date = week_start + timedelta(days=day_idx)
            day_end = day_date + timedelta(days=1)
            y_pos = header_height + day_idx * day_height
            
            # Draw day label
            day_name = day_date.strftime("%A, %b %d")
            painter.setPen(QPen(QColor("#ffffff")))
            painter.drawText(10, y_pos + 25, day_name)
            
            # Draw timeline bar
            timeline_y = y_pos + 10
            timeline_height = day_height - 20
            
            # Background timeline
            painter.setBrush(QBrush(QColor("#1e1e1e")))
            painter.setPen(QPen(QColor("#3a3a3a"), 1))
            painter.drawRoundedRect(int(timeline_x), int(timeline_y), 
                                   int(timeline_width), int(timeline_height), 8, 8)
            
            # Draw hour markers (every hour)
            painter.setPen(QPen(QColor("#3a3a3a"), 1))
            for hour in range(0, 25):
                x = int(timeline_x + hour * hour_width)
                # Draw small tick marks
                if hour < 24:
                    painter.drawLine(x, int(timeline_y), x, int(timeline_y + 5))
                    # Draw hour labels every 3 hours
                    if hour % 3 == 0:
                        painter.setPen(QPen(QColor("#888888")))
                        painter.drawText(x + 2, int(timeline_y - 8), f"{hour:02d}")
                        painter.setPen(QPen(QColor("#3a3a3a"), 1))
            
            # Draw activities for this day
            day_activities = [a for a in self.activities 
                            if a.start < day_end and a.end > day_date]
            
            for activity in day_activities:
                # Clip activity to current day boundaries
                act_start = max(activity.start, day_date)
                act_end = min(activity.end, day_end)
                
                # Calculate position
                start_hour = act_start.hour + act_start.minute / 60
                end_hour = act_end.hour + act_end.minute / 60
                
                # Handle midnight crossing
                if act_start.date() != day_date.date():
                    start_hour = 0
                if act_end.date() != day_date.date():
                    end_hour = 24
                
                duration_hours = end_hour - start_hour
                
                act_x = timeline_x + start_hour * hour_width
                act_width = duration_hours * hour_width
                act_y = timeline_y + 4
                act_height = timeline_height - 8
                
                # Choose color based on type and executed status
                if activity.executed:
                    color = QColor("#2d5016")  # Green for completed
                elif activity.type == "work":
                    color = QColor("#4a5568")
                elif activity.type == "school":
                    color = QColor("#2563eb")
                else:
                    color = QColor("#7c3aed")
                
                # Draw activity block
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(color.lighter(120), 2))
                painter.drawRoundedRect(int(act_x), int(act_y), int(act_width), int(act_height), 5, 5)
                
                # Draw activity name (if width allows)
                if act_width > 40:
                    painter.setPen(QPen(QColor("#ffffff")))
                    text_rect = QRectF(act_x + 5, act_y, act_width - 10, act_height)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                                   activity.name[:15])


class DonutWidget(QWidget):
    """Circular donut graph showing completed vs total hours."""
    
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.completed = 0
        self.total = 0
        self.setMinimumSize(120, 120)
        self.setMaximumSize(120, 120)
    
    def set_values(self, completed, total):
        """Update the donut values."""
        self.completed = completed
        self.total = total
        self.update()
    
    def paintEvent(self, event):
        """Paint the donut graph."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Center and radius
        center_x = self.width() // 2
        center_y = 45
        outer_radius = 35
        inner_radius = 25
        
        # Draw background circle
        painter.setPen(QPen(QColor("#3a3a3a"), 10))
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        painter.drawEllipse(center_x - outer_radius, center_y - outer_radius, 
                          outer_radius * 2, outer_radius * 2)
        
        # Draw progress arc
        if self.total > 0:
            percentage = self.completed / self.total
            span_angle = int(360 * 16 * percentage)  # Qt uses 1/16th degree units
            
            painter.setPen(QPen(self.color, 10))
            painter.drawArc(center_x - outer_radius, center_y - outer_radius,
                          outer_radius * 2, outer_radius * 2,
                          90 * 16, -span_angle)  # Start from top, go clockwise
        
        # Draw center text
        painter.setPen(QPen(QColor("#ffffff")))
        if self.total > 0:
            text = f"{self.completed:.0f}/{self.total:.0f}h"
        else:
            text = "0h"
        painter.drawText(center_x - 30, center_y - 5, 60, 20, 
                        Qt.AlignmentFlag.AlignCenter, text)
        
        # Draw title
        painter.drawText(0, 95, self.width(), 20, 
                        Qt.AlignmentFlag.AlignCenter, self.title)
