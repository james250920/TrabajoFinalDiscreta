import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QDesktopWidget, QApplication
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MarketBasketAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Market Basket Analysis ")
        self.setWindowIcon(QIcon('Icono/redes.png'))
        self.setStyleSheet("background-color: #1f1f1f;")
        self.setFixedSize(1100, 600)  # Tamaño fijo de la ventana

        # Desactivar maximizar y limitar a cerrar y minimizar
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.center()  # Centrar la ventana en pantalla
        self.initUI()  # Inicializar elementos de la interfaz

    def initUI(self):
        layout = QVBoxLayout()  # Usamos un layout vertical

        '''
        label = QLabel("Welcome to the Social Networks Interface", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        '''

        # Botón para volver
        back_button = QPushButton("Back", self)
        back_button.setStyleSheet(
            "background-color: #1f1f1f; font-size: 16px;border-radius: 5px; text-align: center;color: #ac99ea;border: 2px solid #ac99ea;")
        back_button.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a mano al pasar
        back_button.clicked.connect(self.close)  # Cerrar la ventana al hacer clic
        back_button.setGeometry(20, 10, 60, 30)

        '''# Imagen en la parte superior
        self.image_label = QLabel(self)
        self.image_label.setGeometry(450, 20, 200, 200)
        self.image_label.setPixmap(QIcon('Icono/ICON.png').pixmap(200, 200))
        '''

        # Espacio para el gráfico de Matplotlib
        self.figure = Figure()  # Crear una figura de Matplotlib
        self.canvas = FigureCanvas(self.figure)  # Crear un canvas con la figura

        # Contenedor para el canvas
        canvas_container = QWidget(self)  # Contenedor del gráfico
        canvas_container.setGeometry(295, 10, 790, 580)  # Posición y tamaño del contenedor
        canvas_container.setStyleSheet("background-color: white; border: 1px solid black;")

        # Crear la figura de Matplotlib y el canvas
        self.figure = Figure()  # Crear la figura
        self.canvas = FigureCanvas(self.figure)  # Crear el canvas con la figura

        # Layout del contenedor
        canvas_layout = QVBoxLayout(canvas_container)  # Layout vertical para el gráfico
        canvas_layout.addWidget(self.canvas)  # Agregar el canvas al layout del contenedor

        # Dibujar un gráfico de ejemplo
        self.plot_example()

        self.setLayout(layout)  # Establecer el layout

    def plot_example(self):
        """Función para dibujar un gráfico simple."""
        ax = self.figure.add_subplot(111)  # Agregar un subplot a la figura
        ax.plot([0, 1, 2, 3], [5, 1, 20, 5])  # Gráfico de ejemplo
        ax.set_title("Sample Plot")  # Título del gráfico
        self.canvas.draw()  # Renderizar el gráfico en el canvas

    def center(self):
        """Centrar la ventana en la pantalla."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
# Main execution code to test this new interface
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketBasketAnalysis()
    window.show()
    sys.exit(app.exec_())