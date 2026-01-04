"""Date and time utility functions."""
from datetime import datetime, timedelta


def get_current_week_range():
    """Get the start and end datetime of the current week (Monday to Sunday)."""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)
    return week_start, week_end


def filter_activities_by_week(activities, week_start=None, week_end=None):
    """Filter activities that fall within the given week range."""
    if week_start is None or week_end is None:
        week_start, week_end = get_current_week_range()
    
    return [a for a in activities if week_start <= a.start < week_end]


def calculate_activity_stats(activities):
    """Calculate total, completed, and pending hours from activities.
    
    Returns:
        tuple: (total_hours, completed_hours, pending_hours)
    """
    total_hours = sum(a.planned_hours for a in activities)
    completed_hours = sum(a.planned_hours for a in activities if a.executed)
    pending_hours = total_hours - completed_hours
    return total_hours, completed_hours, pending_hours


def calculate_stats_by_type(activities, activity_type):
    """Calculate total and completed hours for a specific activity type.
    
    Args:
        activities: List of Activity objects
        activity_type: Type string ('work', 'school', 'hobbies')
    
    Returns:
        tuple: (completed_hours, total_hours)
    """
    type_activities = [a for a in activities if a.type == activity_type]
    total = sum(a.planned_hours for a in type_activities)
    completed = sum(a.planned_hours for a in type_activities if a.executed)
    return completed, total
