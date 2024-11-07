# ProjectInterface.py

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget, QPushButton, QLineEdit, QTextEdit, QHBoxLayout
from socialNetworks import SocialNetworks  # Import the new interface
from marketBasketAnalysis import  MarketBasketAnalysis


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto Final")
        self.setGeometry(100, 100, 1100, 600)
        self.setWindowIcon(QIcon('Icono/redes.png'))
        self.setStyleSheet("background-color: #1f1f1f;")


        self.setFixedSize(1100, 600)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.center()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setGeometry(450, 20, 200, 200)
        self.label.setPixmap(QIcon('Icono/ICON.png').pixmap(200, 200))

        self.Izquierda = QPushButton("Social Networks", self)
        self.Izquierda.setGeometry(260, 200, 200, 200)
        self.Izquierda.setStyleSheet("background-color: #ac99ea; border-radius: 5px; text-family: Arial; font-size: 20px;")
        self.Izquierda.setCursor(Qt.PointingHandCursor)
        self.Izquierda.clicked.connect(self.openSocialNetworks)  # Connect to the new method

        self.Derecha = QPushButton("Market Basket \n Analysis", self)
        self.Derecha.setGeometry(640, 200, 200, 200)
        self.Derecha.setStyleSheet("background-color: #ac99ea; border-radius: 5px; text-family: Arial; font-size: 20px;")
        self.Derecha.setCursor(Qt.PointingHandCursor)
        self.Derecha.clicked.connect(self.openmarketBasketAnalysis)

        # Create layout for text boxes
        self.layout = QHBoxLayout(self)

        self.textbox1 = QLineEdit(self)
        self.textbox1.setPlaceholderText("Enter text for box 1")
        self.layout.addWidget(self.textbox1)

        self.textbox2 = QLineEdit(self)
        self.textbox2.setPlaceholderText("Enter text for box 2")
        self.layout.addWidget(self.textbox2)

        self.largeTextbox = QTextEdit(self)
        self.largeTextbox.setPlaceholderText("This is a larger text box.")
        self.layout.addWidget(self.largeTextbox)

        # Set layout on the main window
        self.setLayout(self.layout)

        # Hide text boxes initially
        self.textbox1.hide()
        self.textbox2.hide()
        self.largeTextbox.hide()



    def openSocialNetworks(self):
        self.hide()  # Hide the main window
        self.social_window = SocialNetworks()  # Create the social networks window
        self.social_window.show()  # Show the social networks window
        self.social_window.closeEvent = self.closeEventHandler  # Override close event

    def openmarketBasketAnalysis(self):
        self.hide()  # Hide the main window
        self.social_window = MarketBasketAnalysis()  # Create the social networks window
        self.social_window.show()  # Show the social networks window
        self.social_window.closeEvent = self.closeEventHandler  # Override close event

    def closeEventHandler(self, event):
        self.show()  # Show the main window again when the social window is closed
        event.accept()  # Accept the close event

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# Create the application
app = QApplication(sys.argv)
window = Interface()
window.show()
sys.exit(app.exec_())
