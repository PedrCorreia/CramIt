"""Donut graph widget for displaying completion statistics."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


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
