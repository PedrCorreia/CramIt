from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QTabWidget
from PyQt6.QtCore import Qt
from widgets.hub_view import HubWidget


class CalendarPanel(QWidget):
    """Center panel: Calendar and Hub modes with tab switching.
    
    Calendar tab: traditional calendar views
    Hub tab: week/month/year with circular progress graphs
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Create tab widget for Calendar vs Hub modes
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        # Calendar tab (traditional calendar)
        self.calendar_widget = QCalendarWidget()
        self.tabs.addTab(self.calendar_widget, "Calendar")
        
        # Hub tab (week/month/year with graphs)
        self.hub_widget = HubWidget()
        self.tabs.addTab(self.hub_widget, "Hub")
        
        layout.addWidget(self.tabs)
    
    def update_activities(self, activities):
        """Update the hub views with activity data."""
        self.hub_widget.update_activities(activities)
