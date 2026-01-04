"""Activity controller - handles business logic for activity management."""
from PyQt6.QtWidgets import QMessageBox
from utils.models import Activity
from utils.storage import load_activities, save_activities


class ActivityController:
    """Controller for managing activity operations.
    
    Separates business logic from UI concerns following MVC pattern.
    """
    
    def __init__(self):
        """Initialize controller and load activities from storage."""
        self.activities = load_activities()
        self._observers = []
    
    def add_observer(self, callback):
        """Register a callback to be notified when activities change."""
        self._observers.append(callback)
    
    def _notify_observers(self):
        """Notify all observers that activities have changed."""
        for callback in self._observers:
            callback()
    
    def get_activities(self):
        """Get all activities."""
        return self.activities
    
    def add_activity(self, name, activity_type, start, end, executed=False):
        """Add a new activity.
        
        Args:
            name: Activity name
            activity_type: Type of activity (work, school, hobbies)
            start: Start datetime
            end: End datetime
            executed: Whether the activity is completed
            
        Returns:
            The created Activity object
        """
        activity = Activity(
            name=name,
            activity_type=activity_type,
            start=start,
            end=end,
            executed=executed
        )
        self.activities.append(activity)
        self._save_and_notify()
        return activity
    
    def update_activity(self, activity_id, name, activity_type, start, end, executed):
        """Update an existing activity.
        
        Args:
            activity_id: ID of activity to update
            name: New activity name
            activity_type: New activity type
            start: New start datetime
            end: New end datetime
            executed: New executed status
            
        Returns:
            True if activity was found and updated, False otherwise
        """
        activity = self._find_activity(activity_id)
        if not activity:
            return False
        
        activity.name = name
        activity.type = activity_type
        activity.start = start
        activity.end = end
        activity.executed = executed
        
        self._save_and_notify()
        return True
    
    def delete_activity(self, activity_id):
        """Delete an activity.
        
        Args:
            activity_id: ID of activity to delete
            
        Returns:
            True if activity was found and deleted, False otherwise
        """
        initial_count = len(self.activities)
        self.activities = [a for a in self.activities if a.id != activity_id]
        
        if len(self.activities) < initial_count:
            self._save_and_notify()
            return True
        return False
    
    def toggle_executed(self, activity_id):
        """Toggle the executed status of an activity.
        
        Args:
            activity_id: ID of activity to toggle
            
        Returns:
            True if activity was found and toggled, False otherwise
        """
        activity = self._find_activity(activity_id)
        if not activity:
            return False
        
        activity.executed = not activity.executed
        self._save_and_notify()
        return True
    
    def _find_activity(self, activity_id):
        """Find activity by ID."""
        return next((a for a in self.activities if a.id == activity_id), None)
    
    def _save_and_notify(self):
        """Save activities to storage and notify observers."""
        save_activities(self.activities)
        self._notify_observers()
