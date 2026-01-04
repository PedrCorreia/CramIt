from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton


class ListPanel(QWidget):
    """Left-side panel: shows a list and Add/Edit/Delete buttons.

    Methods:
    - set_items(list_of_strings)
    - get_selected_text()
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.list = QListWidget()
        layout.addWidget(self.list)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_edit)
        btn_row.addWidget(self.btn_delete)

        layout.addLayout(btn_row)

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

        self.list.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        has = bool(self.list.selectedItems())
        self.btn_edit.setEnabled(has)
        self.btn_delete.setEnabled(has)

    def set_items(self, items, ids=None):
        """Set list items and attach activity IDs as user data."""
        self.list.clear()
        for i, it in enumerate(items):
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(it)
            if ids and i < len(ids):
                item.setData(1, ids[i])  # Store activity ID
            self.list.addItem(item)

    def get_selected_text(self):
        items = self.list.selectedItems()
        if not items:
            return None
        return items[0].text()
    
    def get_selected_id(self):
        """Get the activity ID of the selected item."""
        items = self.list.selectedItems()
        if not items:
            return None
        return items[0].data(1)
