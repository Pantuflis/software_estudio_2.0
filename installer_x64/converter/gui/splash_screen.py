import time
from gui.main_window import MainWindow
from .elements import Label, ImageLabel, SplashProgressBar
from PyQt6.QtWidgets import  QWidget
from PyQt6 import QtCore, QtGui

MESSAGES = ['Burning books', 'Shredding documents', 'Hidding employees']
counter = 0

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setFixedSize(600, 400)
        self.setWindowFlags(QtCore.Qt.WindowType.SplashScreen)
        # self.setWindowIcon(QtGui.QIcon('gui/icons/program_icon.png'))
        self.setStyleSheet(
            'background: #212121;' 
        )
        
        # Data label
        self.label_data = Label('DATA', '#ffffff', '50', 'bold', self)
        self.label_data.move(85, 30)


        # Converter label
        self.label_converter = Label('CONVERTER', '#ffffff', '50', 'normal',  self)
        self.label_converter.move(235, 80)

        # Pipe label
        self.label_pipe = Label('|', '#ffffff', '90', 'normal', self)
        self.label_pipe.move(215, 20)

        
        # Messages label
        self.label_message = Label('WELCOME HOPLESS SOUL', '#ffffff', '17', 'normal', self)
        self.label_message.setFixedSize(600, 50)
        self.label_message.move(0, 140)
        self.label_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Logo label
        self.logo = ImageLabel('gui/icons/convert_white.png', self)
        self.logo.setFixedSize(172, 95)
        self.logo.move(214, 190)


        # Loading label
        self.label_loading = Label('Loading...', '#ffffff', '15', 'normal', self)
        self.label_loading.setFixedSize(600, 30)
        self.label_loading.move(0, 340)
        self.label_loading.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        # Change messages label
        QtCore.QTimer.singleShot(1500, lambda: self.label_message.setText(MESSAGES[0]))
        QtCore.QTimer.singleShot(3000, lambda: self.label_message.setText(MESSAGES[1]))
        QtCore.QTimer.singleShot(4500, lambda: self.label_message.setText(MESSAGES[2]))

        # Progressbar
        self.progressbar = SplashProgressBar(self)
        self.progressbar.setFixedSize(550, 25)
        self.progressbar.move(25, 310)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(50)

    # Functions
    def progress(self):
        global counter
        self.progressbar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            time.sleep(0.5)
            self.close()
            time.sleep(0.5)
            self.open_main_window()
        counter += 1

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()

    


