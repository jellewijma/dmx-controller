
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QDialog
from src.add_fixture_dialog import AddFixtureDialog

class PatchWindow(QWidget):
    def __init__(self, patch_manager, fixture_library):
        super().__init__()
        self.patch_manager = patch_manager
        self.fixture_library = fixture_library

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Manufacturer", "Model", "Universe", "Address", "Mode"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Add Fixture")
        self.add_button.clicked.connect(self.open_add_fixture_dialog)
        self.layout.addWidget(self.add_button)

        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(0)
        for universe, fixtures in self.patch_manager.patched_fixtures.items():
            for patch_info in fixtures:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(patch_info['fixture']['manufacturer']))
                self.table.setItem(row_position, 1, QTableWidgetItem(patch_info['fixture']['model']))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(universe)))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(patch_info['address'])))
                self.table.setItem(row_position, 4, QTableWidgetItem(patch_info['fixture']['modes'][0]['name']))

    def open_add_fixture_dialog(self):
        dialog = AddFixtureDialog(self.fixture_library, self)
        if dialog.exec_() == QDialog.Accepted:
            fixture, universe, address = dialog.get_selection()
            if fixture:
                self.patch_manager.add_fixture(fixture, universe, address)
                self.populate_table()
