from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QPushButton, QRadioButton, QLineEdit, QGroupBox, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout


class Label(QLabel):
    def __init__(self, text, color, size, weight, parent):
        super().__init__()
        self.setStyleSheet(
            f"""
            color: {color};
            font-size: {size}px;
            font-weight: {weight};
            """
        )
        self.setText(text)
        self.setParent(parent)


class ImageLabel(QLabel):
    def __init__(self, image, parent):
        super().__init__()
        self.setFixedSize(28, 28)
        self.setPixmap(QtGui.QPixmap(image))
        self.setParent(parent)


class SplashProgressBar(QProgressBar):
    def __init__(self, parent):
        super().__init__()
        self.setStyleSheet(
            """
            SplashProgressBar{
                background-color: '#484848';
                color: '#ffffff';
                border-style: none;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
            }
            *::chunk{
                border-radius: 10px;
                background-color: '#005bb2';
            }
            """
        )
        self.setValue(0)
        self.setParent(parent)


class BarButton(QPushButton):
    def __init__(self, icon, parent):
        super().__init__()
        self.setFixedSize(28, 28)
        self.setStyleSheet(
            "*{border: 1px solid '#000000';" +
            "background: '#000000';" +
            "padding: 5px 5px;}" +
            "*:hover{background: '#484848'}" +
            "*:hover{border: '#484848'}" +
            "*:pressed{background: '#212121'}"
            "*:pressed{border: '#212121'}"
        )
        self.setIcon(QtGui.QIcon(icon))
        self.setParent(parent)

class OptionsBox(QGroupBox):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(480, 100)
        self.setTitle('Options')
        self.setStyleSheet(
            """*{
                color: 'white';
                font-size: 15px;
                margin: 7px 0 0 0;
            }
            *::title {
                top: -11.5px;
                left: 10px;
            }
            """
        )
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(5)
        self.setParent(parent)

class Options(QRadioButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(
            """
            border: 0;
            color: 'white';
            font-size: 15px;
            """
        )

class BrowseBar(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.place_holder = ''
        self.setFixedSize(375, 30)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setPlaceholderText('Drop or select your files')
        self.setStyleSheet(
            """
                border: 2px solid '#0e1111';
                background-color: '#484848';
                border-radius: 7px;
                color: 'white';
                font-size: 15px;
                margin: 0;
            """
        )
        self.setParent(parent)
        
    # Drop files
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.DropAction(1))
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.DropAction(1))
            event.accept()
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = str(url.toLocalFile())
            else:
                path = str(url.toString())
            self.setText(path)
        else:
            event.ignore()

class Button(QPushButton):
    def __init__(self, text="", width=100, height=100, radius='10', font_size='10', parent=None):
        super().__init__()
        self.setText(text)
        self.setFixedSize(width, height)
        self.setStyleSheet(
            "*{border: 3px solid '#1e88e5';" +
            f"border-radius: {radius}px;" +
            "background: '#1e88e5';" +
            "font-weight: bold;" +
            "font-family: 'Arial';" +
            "color: '#000000';" +
            f"font-size: {font_size}px;" +
            "padding: 5px 5px;}" +
            "*:hover{background: '#6ab7ff'}" +
            "*:hover{border: '#6ab7ff'}" +
            "*:hover{color: '#000000'}" +
            "*:pressed{background: '#005cb2'}" +
            "*:pressed{border: '#005cb2'}"
            "*:pressed{color: '#ffffff'}"
        )
        self.setParent(parent)


class ProgressBar(QProgressBar):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(480, 30)
        self.setStyleSheet(
            """ProgressBar{border: 2px solid '#0e1111';
            background-color: '#484848';
            border-radius: 7px;
            color: 'white';
            font-size: 15px;
            font-weight: bold;
            text-align: center;}
            *::chunk{
                background-color: '#005cb2';
                border-radius: 4px;
                }"""
        )
        self.setValue(0)
        self.setParent(parent)


class PopUp(QWidget):
    def __init__(self, text='', title='', icon='', parent=None):
        super().__init__()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(
            "background: #212121;"
        )

        # Title bar
        self.title_bar = QFrame(self)
        self.title_bar.setGeometry(0, 0, 500, 30)
        self.title_bar.setStyleSheet('background: #000000')

        # Title bar header
        self.name = Label(title, 'white', '15', 'normal', self.title_bar)
        self.name.move(5, 5)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.message_layout = QHBoxLayout()
        self.btn_layout = QGridLayout()
        self.setLayout(self.main_layout)

        # Content
        self.error = Label(text, '#ffffff', 15, 'normal', self)
        self.ok_button = Button(text='OK', width=100,
                                height=40, font_size='15', parent=self)
        self.icon = ImageLabel(icon, self)
        self.icon.setFixedSize(50, 50)
        self.main_layout.addLayout(self.message_layout)
        self.message_layout.addWidget(self.icon)
        self.message_layout.addWidget(self.error)     
        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.setContentsMargins(10, 35, 10, 10)    
        self.btn_layout.addWidget(self.ok_button)
        self.btn_layout.setContentsMargins(10, 20, 10, 10)                
        self.error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ok_button.clicked.connect(lambda: self.close())


    # Drag window
    def mousePressEvent(self, event):
        self.old_position = event.globalPosition()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPosition() - self.old_position
        self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
        self.old_position = event.globalPosition()

    # Move to center of parent
    def center_window(self):
        geo = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        self.move((int(geo.x() - self.frameSize().width() / 2)) , int((geo.y() - self.frameSize().height() / 2)))

class InfoWindow(PopUp):
    def __init__(
        self, 
        text='', 
        title='Information', 
        icon='gui/icons/info_icon.png',
    ):
        super().__init__(text, title, icon)
        
    def move_center(self): 
        self.center_window()

class ErrorWindow(PopUp):
    def __init__(
        self, 
        text='', 
        title='Something went wrong', 
        icon='gui/icons/error_icon.png'
    ):
        super().__init__(text, title, icon)

    def move_center(self): 
        self.center_window()

class SuccessWindow(PopUp):
    def __init__(
        self, 
        text='', 
        title='Success!', 
        icon='gui/icons/success_icon.png'
    ):
        super().__init__(text, title, icon)

    def move_center(self): 
        self.center_window()


