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

    # fast filter: keep only activities that overlap [start, end)


def map_act_to_dates(activities, start=None, end=None):
    # normalize defaults: require datetimes
    if start is None and end is None:
        start = datetime.now()
        end = start + timedelta(days=1)
    elif start is None:
        start = end - timedelta(days=1)
    elif end is None:
        end = start + timedelta(days=1)

    # optional safety: ensure start <= end
    if start > end:
        start, end = end, start
    def overlaps(a):
        return (a.end > start) and (a.start < end)
    candidates = [a for a in activities if overlaps(a)]
    result = defaultdict(list)
    for activity in candidates:
        act_start = max(activity.start, start)
        act_end = min(activity.end, end)
        if act_end <= act_start:
            continue  # no overlap
    current_date = act_start.date()
    last_date = (act_end - timedelta(microseconds=1)).date()
    while current_date <= last_date:
        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = day_start + timedelta(days=1)
        clip_start = max(act_start, day_start)
        clip_end = min(act_end, day_end)
        if clip_end > clip_start:
            duration = (clip_end - clip_start).total_seconds() / 3600.0
            record = {
                "activity_id":activity.id,
                "name":activity.name,
                "type":activity.type,
                "executed":activity.executed,
                "clipped_start":clip_start,
                "clipped_end":clip_end,
                "duration_hours":duration,
                "all_day": clip_start.time() == datetime.min.time() and clip_end == day_end,
            }
            result[current_date].append(record)
        current_date += timedelta(days=1)
    return dict(result)