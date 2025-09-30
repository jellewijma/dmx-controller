
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSpinBox, QDialogButtonBox, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class AddFixtureForm(QWidget):
    fixture_added = pyqtSignal(object, int, int) # fixture, universe, address
    cancelled = pyqtSignal()

    def __init__(self, fixture_library, parent=None):
        super().__init__(parent)
        self.fixture_library = fixture_library

        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.manufacturer_combo = QComboBox()
        self.model_combo = QComboBox()
        self.universe_spinbox = QSpinBox()
        self.universe_spinbox.setMinimum(1)
        self.address_spinbox = QSpinBox()
        self.address_spinbox.setMinimum(1)
        self.address_spinbox.setMaximum(512)

        self.form_layout.addRow("Manufacturer:", self.manufacturer_combo)
        self.form_layout.addRow("Model:", self.model_combo)
        self.form_layout.addRow("Universe:", self.universe_spinbox)
        self.form_layout.addRow("Address:", self.address_spinbox)

        self.layout.addLayout(self.form_layout)

        self.add_button = QPushButton("Add Fixture")
        self.add_button.clicked.connect(self._add_fixture)
        self.layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancelled.emit)
        self.layout.addWidget(self.cancel_button)

        self.populate_manufacturers()
        self.manufacturer_combo.currentTextChanged.connect(self.populate_models)
        self.populate_models(self.manufacturer_combo.currentText()) # Initial population

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

        fixture = self.fixture_library.get_fixture(manufacturer, model)
        if fixture:
            self.fixture_added.emit(fixture, universe, address)
        else:
            print(f"Error: Fixture {manufacturer} {model} not found in library.")
