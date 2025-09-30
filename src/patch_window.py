
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QStackedWidget, QFormLayout, QComboBox, QSpinBox, QLabel
from PyQt5.QtCore import Qt
from src.add_fixture_form import AddFixtureForm

class PatchWindow(QWidget):
    def __init__(self, patch_manager, fixture_library):
        super().__init__()
        self.patch_manager = patch_manager
        self.fixture_library = fixture_library

        self.main_layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Page 1: Patched Fixtures Table
        self.table_page = QWidget()
        self.table_page_layout = QVBoxLayout(self.table_page)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Manufacturer", "Model", "Universe", "Address", "Mode"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_page_layout.addWidget(self.table)

        self.add_button = QPushButton("Add Fixture")
        self.add_button.clicked.connect(self.show_add_fixture_form)
        self.table_page_layout.addWidget(self.add_button)

        # Search functionality
        self.search_layout = QHBoxLayout()
        self.search_input = QSpinBox()
        self.search_input.setMinimum(1)
        self.search_input.setMaximum(999)
        self.search_button = QPushButton("Search by ID")
        self.search_button.clicked.connect(self.search_fixture_by_id)
        self.search_layout.addWidget(QLabel("Search ID:"))
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.table_page_layout.addLayout(self.search_layout)

        self.stacked_widget.addWidget(self.table_page)

        # Page 2: Add Fixture Form
        self.add_fixture_form = AddFixtureForm(self.fixture_library, self.patch_manager)
        self.add_fixture_form.fixture_added.connect(self.handle_fixture_added)
        self.add_fixture_form.cancelled.connect(self.show_table_page)
        self.stacked_widget.addWidget(self.add_fixture_form)

        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(0)
        for universe, fixtures in self.patch_manager.patched_fixtures.items():
            for patch_info in fixtures:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(patch_info['id'])))
                self.table.setItem(row_position, 1, QTableWidgetItem(patch_info['fixture']['manufacturer']))
                self.table.setItem(row_position, 2, QTableWidgetItem(patch_info['fixture']['model']))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(universe)))
                self.table.setItem(row_position, 4, QTableWidgetItem(str(patch_info['address'])))
                self.table.setItem(row_position, 5, QTableWidgetItem(patch_info['fixture']['modes'][0]['name']))

    def show_add_fixture_form(self):
        self.add_fixture_form._update_suggested_address() # Update suggested address when showing the form
        self.stacked_widget.setCurrentWidget(self.add_fixture_form)

    def show_table_page(self):
        self.stacked_widget.setCurrentWidget(self.table_page)

    def handle_fixture_added(self, fixture, universe, address, fixture_id):
        self.patch_manager.add_fixture(fixture, universe, address, fixture_id)
        self.populate_table()
        print(f"Added fixture: {fixture['manufacturer']} {fixture['model']} (ID: {fixture_id}) at U{universe} A{address}")
        self.show_table_page()

    def search_fixture_by_id(self):
        search_id = self.search_input.value()
        found_fixture = self.patch_manager.get_fixture_by_id(search_id)

        if found_fixture:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0) # ID is in the first column
                if item and int(item.text()) == search_id:
                    self.table.selectRow(row)
                    return
            # This case should ideally not be reached if populate_table is consistent
            # with patch_manager's state.
            print(f"Warning: Fixture with ID {search_id} found in manager but not visually in table.")
        else:
            self.table.clearSelection()
