from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AnalyticsPanel(QWidget):
    """Right-side analytics placeholder. Call update_from(activities) to refresh."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.title = QLabel("Analytics")
        self.summary = QLabel("No data")
        layout.addWidget(self.title)
        layout.addWidget(self.summary)

    def update_from(self, activities):
        self.summary.setText(f"Total activities: {len(activities)}")
