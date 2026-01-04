"""Week timeline widget for displaying activities in a timeline view."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from datetime import datetime, timedelta


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
