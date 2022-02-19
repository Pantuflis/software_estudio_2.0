from PyQt6 import QtGui, QtCore
from functions import operations
from PyQt6.QtWidgets import QWidget, QFrame
from .elements import BarButton, Label, ImageLabel, Options, BrowseBar, Button, OptionsBox, ProgressBar

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 350)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet('background: #212121;')
        self.setWindowIcon(QtGui.QIcon('gui/icons/icon.png'))

        # Title bar
        self.title_bar = QFrame(self)
        self.title_bar.setGeometry(0, 0, 500, 30)
        self.title_bar.setStyleSheet('background: #000000')

        # Title bar logo
        self.logo = ImageLabel('gui/icons/convert_white_icon.png', self.title_bar)
        self.logo.setFixedSize(46, 25)
        self.logo.move(5, 1)

        # Title bar header
        self.name = Label('Data Converter', 'white', '20', 'normal', self.title_bar)
        self.name.move(55, 0)

        # Title bar buttons
        self.minimize_button = BarButton('gui/icons/minimize.png', self)
        self.minimize_button.move(415, 1)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.maximize_button = BarButton('gui/icons/maximize.png', self)
        self.maximize_button.move(443, 1)
        self.maximize_button.clicked.connect(self.maximize_window)
        self.close_button = BarButton('gui/icons/close.png', self)
        self.close_button.move(471, 1)
        self.close_button.clicked.connect(self.close_window)

        # Options box
        self.options_box = OptionsBox(self)
        self.options_box.move(10, 50)

        # Options
        self.option_1 = Options('Archivo Grupos Integrados')
        self.options_box.grid.addWidget(self.option_1, 0, 0 )
        self.option_4 = Options('Agente de Recaudacion Misiones')
        self.options_box.grid.addWidget(self.option_4, 1, 0)
        self.option_2 = Options('SIFERE - Retenciones AGIP')
        self.options_box.grid.addWidget(self.option_2, 0, 1)
        self.option_3 = Options('SIFERE - Percepciones AGIP')
        self.options_box.grid.addWidget(self.option_3, 1, 1)

        #Browser bar
        self.browser_bar = BrowseBar(self)
        self.browser_bar.move(10, 180)

        # Progress bar
        self.progress_bar = ProgressBar(self)
        self.progress_bar.move(10, 295)

        # Browse button
        self.browse_button = Button(text='Browse', width=100, height=30, font_size='18', parent=self)
        self.browse_button.move(390, 180)
        self.browse_button.clicked.connect(self.filter_file)

        # Convert button
        self.convert_button = Button(text='Convert', width=480, height=50, font_size='25', parent=self)
        self.convert_button.move(10, 230)
        self.convert_button.clicked.connect(self.click_convert_file)




    # Functions
    # Minimize, maximize, close window
    def minimize_window(self):
        self.showMinimized()

    def maximize_window(self):
        self.showNormal()

    def close_window(self):
        self.close()

    # Drag window
    def mousePressEvent(self, event):
        self.old_position = event.globalPosition()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPosition() - self.old_position
        self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
        self.old_position = event.globalPosition()

    # Buttons
    def click_browse_file(self, filter):
        operations.browse_file(filter, self.browser_bar, self.progress_bar)

    def click_convert_file(self):
        self.convert_process(self.browser_bar.text())

    def filter_file(self):
        options_list = [self.option_1, self.option_2, self.option_3, self.option_4]
        operations.filter(options_list, self.click_browse_file)

    def convert_process(self, file_name):
        options_list = [self.option_1, self.option_2, self.option_3, self.option_4]
        operations.convert_process(file_name, options_list, self.progress_bar)



