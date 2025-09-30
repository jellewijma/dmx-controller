import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DMXControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DMX Controller')
        
        main_layout = QHBoxLayout()
        
        for i in range(8):
            slider_layout = QVBoxLayout()
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setTickInterval(10)
            slider.setTickPosition(QSlider.TicksRight)
            slider.valueChanged.connect(self.slider_moved)
            
            label = QLabel(f'Ch {i+1}')
            
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            
            main_layout.addLayout(slider_layout)
            
        self.setLayout(main_layout)

    def slider_moved(self):
        slider = self.sender()
        # A bit of a hack to find the channel number from the layout
        for i in range(self.layout().count()):
            layout_item = self.layout().itemAt(i)
            if layout_item and layout_item.layout():
                # Check if the slider is in this layout
                for j in range(layout_item.layout().count()):
                    widget_item = layout_item.layout().itemAt(j)
                    if widget_item and widget_item.widget() == slider:
                        print(f'Channel {i+1}: {slider.value()}')
                        return

def create_gui():
    app = QApplication(sys.argv)
    ex = DMXControl()
    ex.show()
    sys.exit(app.exec_())