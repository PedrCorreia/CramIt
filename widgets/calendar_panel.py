from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QCalendarWidget, QLabel, QPushButton, QHBoxLayout, QTabWidget


class CalendarPanel(QWidget):
    """Center panel: Calendar and Hub modes with tab switching.
    
    Calendar tab: traditional calendar views
    Hub tab: week/month/year with circular progress graphs
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget for Calendar vs Hub modes
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        # Calendar tab (traditional calendar)
        self.calendar_widget = QCalendarWidget()
        self.tabs.addTab(self.calendar_widget, "Calendar")
        
        # Hub tab (week/month/year with graphs)
        self.hub_widget = self._create_hub_widget()
        self.tabs.addTab(self.hub_widget, "Hub")
        
        layout.addWidget(self.tabs)

    def _create_hub_widget(self):
        """Create the Hub view with week/month/year switcher and graph placeholders."""
        hub = QWidget()
        hub_layout = QVBoxLayout(hub)
        
        # View switcher buttons
        btn_layout = QHBoxLayout()
        self.btn_week = QPushButton("Week")
        self.btn_month = QPushButton("Month")
        self.btn_year = QPushButton("Year")
        
        btn_layout.addWidget(self.btn_week)
        btn_layout.addWidget(self.btn_month)
        btn_layout.addWidget(self.btn_year)
        btn_layout.addStretch()
        
        hub_layout.addLayout(btn_layout)
        
        # Stacked widget for different time period views
        self.hub_stack = QStackedWidget()
        self.week_view = QLabel("Week Hub:\n7 circular graphs (planned vs executed per day)\n+ weekly total")
        self.month_view = QLabel("Month Hub:\nMonthly circular graph\n(planned vs executed for the month)")
        self.year_view = QLabel("Year Hub:\n12 circular graphs (one per month)\n+ yearly total")
        
        self.hub_stack.addWidget(self.week_view)
        self.hub_stack.addWidget(self.month_view)
        self.hub_stack.addWidget(self.year_view)
        
        hub_layout.addWidget(self.hub_stack)
        
        # Connect buttons
        self.btn_week.clicked.connect(self.show_week)
        self.btn_month.clicked.connect(self.show_month)
        self.btn_year.clicked.connect(self.show_year)
        
        # Default to month view
        self.show_month()
        
        return hub

    def show_week(self):
        self.hub_stack.setCurrentWidget(self.week_view)

    def show_month(self):
        self.hub_stack.setCurrentWidget(self.month_view)

    def show_year(self):
        self.hub_stack.setCurrentWidget(self.year_view)
