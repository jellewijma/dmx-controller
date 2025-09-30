
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSpinBox, QDialogButtonBox, QFormLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class AddFixtureForm(QWidget):
    fixture_added = pyqtSignal(object, int, int, int) # fixture, universe, address, id
    cancelled = pyqtSignal()

    def __init__(self, fixture_library, patch_manager, parent=None): # Added patch_manager
        super().__init__(parent)
        self.fixture_library = fixture_library
        self.patch_manager = patch_manager # Stored patch_manager

        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.manufacturer_combo = QComboBox()
        self.model_combo = QComboBox()
        self.universe_spinbox = QSpinBox()
        self.universe_spinbox.setMinimum(1)
        self.address_spinbox = QSpinBox()
        self.address_spinbox.setMinimum(1)
        self.address_spinbox.setMaximum(512)
        self.id_spinbox = QSpinBox() # New ID spinbox
        self.id_spinbox.setMinimum(1)
        self.id_spinbox.setMaximum(999) # Arbitrary max ID
        self.id_spinbox.setValue(self.patch_manager._next_fixture_id) # Set initial ID

        self.form_layout.addRow("Manufacturer:", self.manufacturer_combo)
        self.form_layout.addRow("Model:", self.model_combo)
        self.form_layout.addRow("Universe:", self.universe_spinbox)
        self.form_layout.addRow("Address:", self.address_spinbox)
        self.form_layout.addRow("ID:", self.id_spinbox) # Add ID to form

        self.layout.addLayout(self.form_layout)

        self.add_button = QPushButton("Add Fixture")
        self.add_button.clicked.connect(self._add_fixture)
        self.layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancelled.emit)
        self.layout.addWidget(self.cancel_button)

        self.populate_manufacturers()
        self.manufacturer_combo.currentTextChanged.connect(self.populate_models)
        self.model_combo.currentTextChanged.connect(self._update_suggested_address) # Connect model change
        self.universe_spinbox.valueChanged.connect(self._update_suggested_address) # Connect universe change
        self.populate_models(self.manufacturer_combo.currentText()) # Initial population
        self._update_suggested_address() # Set initial suggested address

    def _find_next_free_address(self, universe, num_channels):
        if universe not in self.patch_manager.patched_fixtures:
            return 1 # If universe is empty, address 1 is free

        occupied_ranges = []
        for patch_info in self.patch_manager.patched_fixtures[universe]:
            existing_fixture = patch_info['fixture']
            existing_address = patch_info['address']
            existing_mode = existing_fixture['modes'][0] # Assuming first mode
            existing_num_channels = len(existing_mode['channels'])
            occupied_ranges.append((existing_address, existing_address + existing_num_channels - 1))

        occupied_ranges.sort()

        # Find the first gap
        current_address = 1
        for start, end in occupied_ranges:
            if current_address + num_channels - 1 < start:
                return current_address
            current_address = end + 1
        
        return current_address # If no gap, return the next address after all existing fixtures

    def _update_suggested_address(self):
        manufacturer = self.manufacturer_combo.currentText()
        model = self.model_combo.currentText()
        universe = self.universe_spinbox.value()

        fixture = self.fixture_library.get_fixture(manufacturer, model)
        if fixture:
            mode = fixture['modes'][0]
            num_channels = len(mode['channels'])
            next_free_address = self._find_next_free_address(universe, num_channels)
            self.address_spinbox.setValue(next_free_address)
        else:
            self.address_spinbox.setValue(1) # Default to 1 if fixture not found

    def populate_manufacturers(self):
        manufacturers = sorted(list(set(f['manufacturer'] for f in self.fixture_library.fixtures)))
        self.manufacturer_combo.addItems(manufacturers)

    def populate_models(self, manufacturer):
        self.model_combo.clear()
        models = sorted([f['model'] for f in self.fixture_library.fixtures if f['manufacturer'] == manufacturer])
        self.model_combo.addItems(models)

    def _add_fixture(self):
        manufacturer = self.manufacturer_combo.currentText()
        model = self.model_combo.currentText()
        universe = self.universe_spinbox.value()
        address = self.address_spinbox.value()
        fixture_id = self.id_spinbox.value() # Get ID

        fixture = self.fixture_library.get_fixture(manufacturer, model)
        if fixture:
            self.fixture_added.emit(fixture, universe, address, fixture_id) # Emit ID
            self.id_spinbox.setValue(self.patch_manager._next_fixture_id) # Update ID spinbox
        else:
            print(f"Error: Fixture {manufacturer} {model} not found in library.")
