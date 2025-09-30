
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QAction, QFileDialog, QTabWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from src.dmx_output import send_dmx
from src.show_file import save_show, load_show
from src.patch_window import PatchWindow

class DMXControl(QMainWindow):
    def __init__(self, patch_manager, fixture_library):
        super().__init__()
        self.patch_manager = patch_manager
        self.fixture_library = fixture_library
        self.dmx_frame = [0] * 512
        self.patch_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DMX Controller')

        # Create menu bar
        menubar = self.menuBar()
        # Removed File menu, as save/load will be in a tab
        patch_menu = menubar.addMenu('Patch')

        manage_patch_action = QAction('Manage Patch', self)
        manage_patch_action.triggered.connect(self.open_patch_window)
        patch_menu.addAction(manage_patch_action)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create DMX Control tab (sliders)
        dmx_control_widget = QWidget()
        dmx_control_layout = QHBoxLayout(dmx_control_widget)
        
        self.sliders = []
        
        for i in range(8):
            slider_layout = QVBoxLayout()
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setTickInterval(10)
            slider.setTickPosition(QSlider.TicksRight)
            slider.valueChanged.connect(self.slider_moved)
            self.sliders.append(slider)
            
            label = QLabel(f'Ch {i+1}')
            
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            
            dmx_control_layout.addLayout(slider_layout)
        
        self.tab_widget.addTab(dmx_control_widget, "DMX Control")

        # Create Session tab
        session_widget = QWidget()
        session_layout = QVBoxLayout(session_widget)

        save_button = QPushButton("Save Show")
        save_button.clicked.connect(self.save_action)
        session_layout.addWidget(save_button)

        load_button = QPushButton("Load Show")
        load_button.clicked.connect(self.load_action)
        session_layout.addWidget(load_button)

        self.tab_widget.addTab(session_widget, "Session")

        # Open Patch Manager tab by default
        self.patch_window = PatchWindow(self.patch_manager, self.fixture_library)
        self.tab_widget.addTab(self.patch_window, "Patch Manager")
        self.tab_widget.setCurrentWidget(self.patch_window)

    def slider_moved(self):
        slider = self.sender()
        channel = self.sliders.index(slider)
        value = slider.value()
        
        print(f'Channel {channel + 1}: {value}')

        self.dmx_frame[channel] = value
        send_dmx(self.dmx_frame)

    def save_action(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Show File","","JSON Files (*.json);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith(".json"):
                fileName += ".json"
            save_show(fileName, self.dmx_frame, self.patch_manager)
            print(f"Show saved to {fileName}")

    def load_action(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load Show File","","JSON Files (*.json);;All Files (*)", options=options)
        if fileName:
            loaded_dmx_frame, loaded_patched_fixtures_data = load_show(fileName, self.fixture_library)
            
            self.dmx_frame = loaded_dmx_frame
            self.patch_manager.clear_patch()
            for universe, fixtures_data in loaded_patched_fixtures_data.items():
                for patch_info in fixtures_data:
                    # Directly use the fixture object from patch_info
                    fixture = patch_info['fixture']
                    if fixture:
                        self.patch_manager.add_fixture(fixture, int(universe), patch_info['address'])

            self.update_sliders()
            send_dmx(self.dmx_frame)
            if self.patch_window:
                self.patch_window.populate_table()
            print(f"Show loaded from {fileName}")

    def update_sliders(self):
        for i, slider in enumerate(self.sliders):
            slider.setValue(self.dmx_frame[i])

    def open_patch_window(self):
        # Patch window is now always created and added as a tab
        self.tab_widget.setCurrentWidget(self.patch_window)

def create_gui(patch_manager, fixture_library):
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    ex = DMXControl(patch_manager, fixture_library)
    ex.show()
    sys.exit(app.exec_())
