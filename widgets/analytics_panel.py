from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AnalyticsPanel(QWidget):
    """Right-side analytics placeholder. Call update_from(activities) to refresh."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        self.title = QLabel("Analytics")
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.summary = QLabel("No data")
        
        layout.addWidget(self.title)
        layout.addWidget(self.summary)
        layout.addStretch()

    def update_from(self, activities):
        self.summary.setText(f"Total activities: {len(activities)}")
