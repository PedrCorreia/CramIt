"""Centralized color scheme for CramIT application."""
from PyQt6.QtGui import QColor


# Activity type colors - planned (soft) versions
ACTIVITY_COLORS = {
    "work": QColor("#e8b4a0"),      # Soft salmon
    "school": QColor("#90ee90"),    # Soft green (light green)
    "hobbies": QColor("#dda0dd"),   # Soft plum
}

# Activity type colors - executed (harder) versions
EXECUTED_COLORS = {
    "work": QColor("#c0503b"),      # Reddish (harder red)
    "school": QColor("#2d5016"),    # Harder green (dark green)
    "hobbies": QColor("#8b008b"),   # Darker magenta
}

# UI colors
BACKGROUND_DARK = QColor("#2d2d2d")
BACKGROUND_DARKER = QColor("#1e1e1e")
BORDER_COLOR = QColor("#3a3a3a")
TEXT_COLOR = QColor("#ffffff")
TEXT_SECONDARY = QColor("#888888")


def get_activity_color(activity):
    """Get the appropriate color for an activity.
    
    Args:
        activity: Activity object with 'type' and 'executed' attributes
        
    Returns:
        QColor: The color to use for this activity (executed or planned)
    """
    if activity.executed:
        return EXECUTED_COLORS.get(activity.type, EXECUTED_COLORS["work"])
    return ACTIVITY_COLORS.get(activity.type, ACTIVITY_COLORS["work"])
