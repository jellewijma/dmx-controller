
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QAction, QFileDialog
from PyQt5.QtCore import Qt
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
        file_menu = menubar.addMenu('File')
        patch_menu = menubar.addMenu('Patch')

        save_action = QAction('Save Show', self)
        save_action.triggered.connect(self.save_action)
        file_menu.addAction(save_action)

        load_action = QAction('Load Show', self)
        load_action.triggered.connect(self.load_action)
        file_menu.addAction(load_action)

        manage_patch_action = QAction('Manage Patch', self)
        manage_patch_action.triggered.connect(self.open_patch_window)
        patch_menu.addAction(manage_patch_action)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
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
            
            main_layout.addLayout(slider_layout)

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
                    fixture = self.fixture_library.get_fixture(patch_info['manufacturer'], patch_info['model'])
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
        if not self.patch_window:
            self.patch_window = PatchWindow(self.patch_manager, self.fixture_library)
        self.patch_window.show()

def create_gui(patch_manager, fixture_library):
    app = QApplication(sys.argv)
    ex = DMXControl(patch_manager, fixture_library)
    ex.show()
    sys.exit(app.exec_())

