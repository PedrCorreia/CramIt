"""CramIt Application - Main Entry Point

A modular planner application for tracking activities with calendar and analytics.

Project Structure:
- models.py: Data models (Activity class)
- storage.py: Data persistence layer
- dialogs.py: UI dialogs for creating/editing activities
- controllers/: Business logic layer
  - activity_controller.py: Activity management logic
- ui/: User interface layer
  - main_window.py: Main application window
- widgets/: Reusable UI components
  - list_panel.py: Activity list view
  - calendar_panel.py: Calendar and hub views
  - analytics_panel.py: Analytics display

Architecture:
Follows MVC (Model-View-Controller) pattern for clean separation of concerns:
- Model: Activity, Storage
- View: MainWindow, Widgets
- Controller: ActivityController
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow


def main():
    """Run the CramIt application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()