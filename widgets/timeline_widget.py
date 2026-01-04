"""Week timeline widget for displaying activities in a timeline view."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QBrush
from datetime import datetime, timedelta
from utils.colors import get_activity_color, BACKGROUND_DARKER, BORDER_COLOR, TEXT_COLOR, TEXT_SECONDARY


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
            
            print(f"\n=== Day {day_idx}: {day_date.date()} ===")
            print(f"Day range: {day_date} to {day_end}")
            
            # Draw day label
            day_name = day_date.strftime("%A, %b %d")
            painter.setPen(QPen(TEXT_COLOR))
            painter.drawText(10, y_pos + 25, day_name)
            
            # Draw timeline bar
            timeline_y = y_pos + 10
            timeline_height = day_height - 20
            
            # Background timeline
            painter.setBrush(QBrush(BACKGROUND_DARKER))
            painter.setPen(QPen(BORDER_COLOR, 1))
            painter.drawRoundedRect(int(timeline_x), int(timeline_y), 
                                   int(timeline_width), int(timeline_height), 8, 8)
            
            # Draw hour markers (every hour)
            painter.setPen(QPen(BORDER_COLOR, 1))
            for hour in range(0, 25):
                x = int(timeline_x + hour * hour_width)
                # Draw small tick marks
                if hour < 24:
                    painter.drawLine(x, int(timeline_y), x, int(timeline_y + 5))
                    # Draw hour labels every 3 hours
                    if hour % 3 == 0:
                        painter.setPen(QPen(TEXT_SECONDARY))
                        painter.drawText(x + 2, int(timeline_y - 8), f"{hour:02d}")
                        painter.setPen(QPen(BORDER_COLOR, 1))
            
            # Draw activities for this day
            day_activities = [a for a in self.activities 
                            if a.start < day_end and a.end > day_date]
            
            print(f"Found {len(day_activities)} activities for this day")
            
            for activity in day_activities:
                # Calculate which portion of the activity falls within this day
                # Use the activity's actual start/end times, but clamp to day boundaries
                
                # Debug: print activity info
                print(f"\n--- Activity: {activity.name} ---")
                print(f"Full activity: {activity.start} to {activity.end}")
                print(f"Current day: {day_date.date()}")
                
                # If activity starts before this day, draw from beginning (hour 0)
                if activity.start.date() < day_date.date():
                    start_hour = 0.0
                    print(f"Activity starts before this day, using start_hour=0")
                else:
                    # Activity starts on this day, use actual hour
                    start_hour = activity.start.hour + activity.start.minute / 60.0
                    print(f"Activity starts on this day at {activity.start.hour}:{activity.start.minute}, start_hour={start_hour:.2f}")
                
                # If activity ends after this day, draw to end (hour 24)
                if activity.end.date() > day_date.date():
                    end_hour = 24.0
                    print(f"Activity ends after this day, using end_hour=24")
                else:
                    # Activity ends on this day, use actual hour
                    end_hour = activity.end.hour + activity.end.minute / 60.0
                    print(f"Activity ends on this day at {activity.end.hour}:{activity.end.minute}, end_hour={end_hour:.2f}")
                
                duration_hours = end_hour - start_hour
                print(f"Drawing from hour {start_hour:.2f} to {end_hour:.2f} (duration: {duration_hours:.2f}h)")
                
                # Calculate pixel position
                act_x = timeline_x + start_hour * hour_width
                act_width = (end_hour - start_hour) * hour_width
                act_y = timeline_y + 4
                act_height = timeline_height - 8
                
                # Get color from centralized color scheme
                color = get_activity_color(activity)
                
                # Draw activity block
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(color.lighter(120), 2))
                painter.drawRoundedRect(int(act_x), int(act_y), int(act_width), int(act_height), 5, 5)
                
                # Draw activity name (if width allows)
                if act_width > 40:
                    painter.setPen(QPen(TEXT_COLOR))
                    text_rect = QRectF(act_x + 5, act_y, act_width - 10, act_height)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                                   activity.name[:15])
