"""Add/Edit activity dialog."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDoubleSpinBox, QComboBox, QDateTimeEdit, 
                             QPushButton, QHBoxLayout, QCheckBox)
from PyQt6.QtCore import QDateTime
from datetime import datetime


class TaskDialog(QDialog):
    """Dialog for creating or editing an activity.
    
    Fields:
    - Name
    - Type (work, school, hobbies)
    - Start datetime
    - End datetime
    - Executed checkbox (mark if completed)
    """
    
    def __init__(self, activity=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Activity" if activity is None else "Edit Activity")
        self.activity = activity
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # Name field
        self.name_input = QLineEdit()
        form.addRow("Name:", self.name_input)
        
        # Type dropdown
        self.type_input = QComboBox()
        self.type_input.addItems(["work", "school", "hobbies"])
        self.type_input.setEditable(True)  # Allow custom types
        form.addRow("Type:", self.type_input)
        
        # Start datetime
        self.start_input = QDateTimeEdit()
        self.start_input.setCalendarPopup(True)
        self.start_input.setDateTime(QDateTime.currentDateTime())
        form.addRow("Start:", self.start_input)
        
        # End datetime
        self.end_input = QDateTimeEdit()
        self.end_input.setCalendarPopup(True)
        self.end_input.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # +1 hour default
        form.addRow("End:", self.end_input)
        
        # Executed checkbox
        self.executed_input = QCheckBox()
        form.addRow("Executed:", self.executed_input)
        
        layout.addLayout(form)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        
        # Connect buttons
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        # Populate if editing
        if activity:
            self._populate_fields(activity)
    
    def _populate_fields(self, activity):
        """Fill form with existing activity data."""
        self.name_input.setText(activity.name)
        self.type_input.setCurrentText(activity.type)
        self.executed_input.setChecked(activity.executed)
        
        if isinstance(activity.start, datetime):
            self.start_input.setDateTime(QDateTime(activity.start))
        if isinstance(activity.end, datetime):
            self.end_input.setDateTime(QDateTime(activity.end))
    
    def get_data(self):
        """Return dict with form data."""
        return {
            "name": self.name_input.text(),
            "type": self.type_input.currentText(),
            "start": self.start_input.dateTime().toPyDateTime(),
            "end": self.end_input.dateTime().toPyDateTime(),
            "executed": self.executed_input.isChecked()
        }
