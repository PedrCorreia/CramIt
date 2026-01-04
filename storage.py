"""Storage functions for activities."""
import json
from pathlib import Path
from models import Activity


STORAGE_DIR = Path.home() / ".cramit"
ACTIVITIES_FILE = STORAGE_DIR / "activities.json"


def ensure_storage():
    """Create storage directory if it doesn't exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_activities():
    """Load activities from JSON file."""
    ensure_storage()
    if not ACTIVITIES_FILE.exists():
        return []
    
    try:
        with open(ACTIVITIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Activity.from_dict(item) for item in data]
    except Exception as e:
        print(f"Error loading activities: {e}")
        return []


def save_activities(activities):
    """Save activities to JSON file."""
    ensure_storage()
    try:
        data = [act.to_dict() for act in activities]
        with open(ACTIVITIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving activities: {e}")
