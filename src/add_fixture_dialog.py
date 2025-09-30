
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QSpinBox, QDialogButtonBox, QFormLayout

class AddFixtureDialog(QDialog):
    def __init__(self, fixture_library, parent=None):
        super().__init__(parent)
        self.fixture_library = fixture_library

        self.setWindowTitle("Add Fixture")
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

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.populate_manufacturers()
        self.manufacturer_combo.currentTextChanged.connect(self.populate_models)

    def populate_manufacturers(self):
        manufacturers = sorted(list(set(f['manufacturer'] for f in self.fixture_library.fixtures)))
        self.manufacturer_combo.addItems(manufacturers)

    def populate_models(self, manufacturer):
        self.model_combo.clear()
        models = sorted([f['model'] for f in self.fixture_library.fixtures if f['manufacturer'] == manufacturer])
        self.model_combo.addItems(models)

    def get_selection(self):
        manufacturer = self.manufacturer_combo.currentText()
        model = self.model_combo.currentText()
        fixture = self.fixture_library.get_fixture(manufacturer, model)
        universe = self.universe_spinbox.value()
        address = self.address_spinbox.value()
        return fixture, universe, address
