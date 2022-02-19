import sys
from PyQt6.QtWidgets import QApplication
from gui.splash_screen import SplashScreen
from gui.main_window import MainWindow
from functions import options, operations


app = QApplication(sys.argv)

splash_screen = SplashScreen()
# main_window = MainWindow()

if __name__ == "__main__":
    splash_screen.show()
    # main_window.show()
    sys.exit(app.exec())