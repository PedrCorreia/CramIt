"""Activity data model."""
import uuid
from datetime import datetime


class Activity:
    """Represents a planned activity with time tracking."""
    
    def __init__(self, name="", activity_type="work", 
                 start=None, end=None, executed=False, activity_id=None,
                 category="general", subcategory=""):
        self.id = activity_id or str(uuid.uuid4())
        self.name = name
        self.type = activity_type  # work, school, hobbies
        self.start = start or datetime.now()
        self.end = end or datetime.now()
        self.executed = executed  # Boolean: was this activity completed?
        self.category = category
        self.subcategory = subcategory

    @property
    def planned_hours(self):
        """Calculate planned hours from start and end times."""
        if isinstance(self.start, datetime) and isinstance(self.end, datetime):
            duration = self.end - self.start
            return duration.total_seconds() / 3600.0
        return 0.0
    
    def to_dict(self):
        """Convert to dict for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "start": self.start.isoformat() if isinstance(self.start, datetime) else self.start,
            "end": self.end.isoformat() if isinstance(self.end, datetime) else self.end,
            "executed": self.executed,
            "category": self.category,
            "subcategory": self.subcategory,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Activity from dict."""
        act = cls(
            name=data.get("name", ""),
            activity_type=data.get("type", "work"),
            executed=data.get("executed", False),
            activity_id=data.get("id"),
            category=data.get("category", "general"),
            subcategory=data.get("subcategory", ""),
        )
        # Parse ISO datetime strings
        start = data.get("start")
        if isinstance(start, str):
            act.start = datetime.fromisoformat(start)
        end = data.get("end")
        if isinstance(end, str):
            act.end = datetime.fromisoformat(end)
        return act
