"""Main window for CramIt application."""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QSplitter, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from widgets.list_panel import ListPanel
from widgets.calendar_panel import CalendarPanel
from widgets.analytics_panel import AnalyticsPanel
from controllers.activity_controller import ActivityController
from utils.dialogs import TaskDialog


class MainWindow(QMainWindow):
    """Main application window for CramIt planner.
    
    Follows MVC pattern:
    - View: This class and widget panels
    - Controller: ActivityController
    - Model: Activity class and storage
    """
    
    def __init__(self):
        """Initialize the main window and its components."""
        super().__init__()
        
        self.setWindowTitle("CramIt - Planner")
        self.resize(1400, 900)
        
        # Initialize controller
        self.controller = ActivityController()
        self.controller.add_observer(self.refresh_ui)
        
        # Setup UI
        self._setup_ui()
        
        # Initial refresh
        self.refresh_ui()
    
    def _setup_ui(self):
        """Set up the user interface layout and components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        
        # Create panels 
        self.list_panel = ListPanel()
        self.calendar_panel = CalendarPanel()
        self.analytics_panel = AnalyticsPanel()
        
        # Add to splitter
        splitter.addWidget(self.list_panel)
        splitter.addWidget(self.calendar_panel)
        splitter.addWidget(self.analytics_panel)
        splitter.setSizes([200, 600, 200])
        
        layout.addWidget(splitter)
        
        # Connect signals to slots
        self._connect_signals()
    
    def _connect_signals(self):
        """Connect widget signals to handler methods."""
        self.list_panel.btn_add.clicked.connect(self.on_add_activity)
        self.list_panel.btn_edit.clicked.connect(self.on_edit_activity)
        self.list_panel.btn_delete.clicked.connect(self.on_delete_activity)
        self.list_panel.list.itemDoubleClicked.connect(self.on_toggle_executed)
    
    def on_add_activity(self):
        """Handle add activity button click."""
        dialog = TaskDialog(parent=self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.add_activity(
                name=data["name"],
                activity_type=data["type"],
                start=data["start"],
                end=data["end"],
                executed=data["executed"]
            )
    
    def on_edit_activity(self):
        """Handle edit activity button click."""
        selected_id = self.list_panel.get_selected_id()
        if not selected_id:
            return
        
        # Find activity
        activity = next((a for a in self.controller.get_activities() 
                        if a.id == selected_id), None)
        if not activity:
            return
        
        dialog = TaskDialog(activity=activity, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.update_activity(
                activity_id=selected_id,
                name=data["name"],
                activity_type=data["type"],
                start=data["start"],
                end=data["end"],
                executed=data["executed"]
            )
    
    def on_delete_activity(self):
        """Handle delete activity button click."""
        selected_id = self.list_panel.get_selected_id()
        if not selected_id:
            return
        
        reply = QMessageBox.question(
            self, 
            'Confirm Delete', 
            'Delete this activity?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_activity(selected_id)
    
    def on_toggle_executed(self):
        """Handle double-click on activity to toggle executed status."""
        selected_id = self.list_panel.get_selected_id()
        if not selected_id:
            return
        
        self.controller.toggle_executed(selected_id)
    
    def refresh_ui(self):
        """Refresh all UI panels with current data from controller."""
        activities = self.controller.get_activities()
        
        # Update list panel - show calculated hours and executed status
        items = []
        for a in activities:
            status = "✓" if a.executed else "○"
            items.append(f"{status} {a.name} ({a.planned_hours:.1f}h, {a.type})")
        
        ids = [a.id for a in activities]
        self.list_panel.set_items(items, ids)
        
        # Update calendar panel with activities
        self.calendar_panel.update_activities(activities)
        
        # Update analytics
        self.analytics_panel.update_from(activities)
        self.analytics_panel.update_from(activities)
