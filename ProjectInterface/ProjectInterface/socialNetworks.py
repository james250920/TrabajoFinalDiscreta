import sys
import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QDesktopWidget, QApplication, QTableWidgetItem, QTableWidget
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx  # Para generar el grafo
import matplotlib.pyplot as plt  # Para dibujar el grafo
from matplotlib.backend_bases import MouseButton  # Para manejar clicks en el grafo


# Conexión a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sistemas",
            database="finaldiscreta"
        )
        print("Connected to the database successfully")
        return conexion
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")
        return None


# Clase principal para la ventana de la interfaz
class SocialNetworks(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Networks")
        self.setWindowIcon(QIcon('Icono/redes.png'))
        self.setStyleSheet("background-color: #1f1f1f;")
        self.setFixedSize(1100, 600)  # Tamaño fijo de la ventana
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.center()  # Centrar la ventana en pantalla
        self.initUI()  # Inicializar elementos de la interfaz

    def initUI(self):
        layout = QVBoxLayout()  # Usamos un layout vertical
        back_button = QPushButton("Back", self)
        back_button.setStyleSheet(
            "background-color: #1f1f1f; font-size: 16px;border-radius: 5px; text-align: center;color: #ac99ea;border: 2px solid #ac99ea;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.close)
        back_button.setGeometry(20, 10, 60, 30)

        # Espacio para el gráfico de Matplotlib
        self.figure = Figure()  # Crear una figura de Matplotlib
        self.canvas = FigureCanvas(self.figure)  # Crear un canvas con la figura

        # Contenedor para el canvas
        canvas_container = QWidget(self)
        canvas_container.setGeometry(295, 10, 790, 580)
        canvas_container.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 5px ")
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.addWidget(self.canvas)

        self.setLayout(layout)

        # Crear tabla para mostrar usuarios
        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(2)  # ID y Nombre
        self.user_table.setHorizontalHeaderLabels(["ID", "Usuarios"])
        self.user_table.setGeometry(20, 50, 110, 500)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.cellClicked.connect(self.on_user_selected)

        # Cargar el grafo completo al iniciar
        self.load_complete_graph()  # Esta línea llama a la nueva función


        # Cargar usuarios en la tabla
        self.load_users()

        # Etiqueta para mostrar el ID del usuario seleccionado
        self.selected_user_id_label = QLabel("Selected User ID: None", self)
        self.selected_user_id_label.setGeometry(20, 570, 100, 30)

    def load_users(self):
        """Cargar usuarios desde la base de datos en la tabla."""
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT id, nombre FROM Usuarios"
                cursor.execute(query)
                usuarios = cursor.fetchall()

                self.user_table.setRowCount(len(usuarios))
                self.user_table.setStyleSheet("background-color: #8264ee; color: #190649;")
                self.user_table.setColumnWidth(0, 0)
                self.user_table.setColumnWidth(1, 70)
                for row in range(len(usuarios)):
                    self.user_table.setRowHeight(row, 25)

                for row, usuario in enumerate(usuarios):
                    self.user_table.setItem(row, 0, QTableWidgetItem(str(usuario[0])))
                    self.user_table.setItem(row, 1, QTableWidgetItem(usuario[1]))

            except mysql.connector.Error as err:
                print(f"Error fetching users: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            print("Failed to load users due to connection issue.")

    def on_user_selected(self, row, column):
        """Actualizar la etiqueta con el ID del usuario seleccionado y generar el gráfico."""
        user_id = int(self.user_table.item(row, 0).text())  # Obtener el ID de la celda seleccionada
        self.selected_user_id_label.setText(f"Selected User ID: {user_id}")

        # Lógica para generar el grafo y mostrar las amistades
        self.generate_graph_for_user(user_id)

    def generate_graph_for_user(self, user_id):
        """Generar el grafo de amistades completo para el usuario seleccionado, incluyendo amigos de amigos y sus amistades, sin bucles."""
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()

                # Obtener el nombre del usuario principal
                query_usuario = "SELECT nombre FROM Usuarios WHERE id = %s"
                cursor.execute(query_usuario, (user_id,))
                nombre_usuario = cursor.fetchone()[0]

                # Obtener todas las amistades del usuario seleccionado
                query_amigos = """
                SELECT 
                    CASE 
                        WHEN A.id_usuario1 = %s THEN U2.id
                        ELSE U1.id
                    END AS amigo_id,
                    CASE 
                        WHEN A.id_usuario1 = %s THEN U2.nombre
                        ELSE U1.nombre
                    END AS nombre_amigo
                FROM Amistades A
                JOIN Usuarios U1 ON A.id_usuario1 = U1.id
                JOIN Usuarios U2 ON A.id_usuario2 = U2.id
                WHERE A.id_usuario1 = %s OR A.id_usuario2 = %s
                """
                cursor.execute(query_amigos, (user_id, user_id, user_id, user_id))
                amistades = cursor.fetchall()

                # Crear el grafo con NetworkX
                self.figure.clear()  # Limpiar la figura actual
                G = nx.Graph()

                # Añadir nodo del usuario principal con su nombre
                G.add_node(user_id, label=f"{nombre_usuario} ({user_id})")

                # Añadir amigos directos y sus amistades
                amigos_visitados = set()  # Conjunto para evitar duplicados

                for amigo_id, nombre_amigo in amistades:
                    if amigo_id not in amigos_visitados:
                        amigos_visitados.add(amigo_id)

                        # Añadir amigo directo al grafo
                        G.add_node(amigo_id, label=f"{nombre_amigo} ({amigo_id})")
                        G.add_edge(user_id, amigo_id)  # Conectar al usuario con sus amigos directos

                        # Obtener todas las amistades del amigo (amigos de amigos)
                        query_amigos_amigo = """
                        SELECT 
                            CASE 
                                WHEN A.id_usuario1 = %s THEN U2.id
                                ELSE U1.id
                            END AS amigo_de_amigo_id,
                            CASE 
                                WHEN A.id_usuario1 = %s THEN U2.nombre
                                ELSE U1.nombre
                            END AS nombre_amigo_de_amigo
                        FROM Amistades A
                        JOIN Usuarios U1 ON A.id_usuario1 = U1.id
                        JOIN Usuarios U2 ON A.id_usuario2 = U2.id
                        WHERE A.id_usuario1 = %s OR A.id_usuario2 = %s
                        """
                        cursor.execute(query_amigos_amigo, (amigo_id, amigo_id, amigo_id, amigo_id))
                        amigos_de_amigo = cursor.fetchall()

                        for amigo_de_amigo_id, nombre_amigo_de_amigo in amigos_de_amigo:
                            if amigo_de_amigo_id not in amigos_visitados:
                                # Añadir amigos de amigos al grafo
                                amigos_visitados.add(amigo_de_amigo_id)
                                G.add_node(amigo_de_amigo_id, label=f"{nombre_amigo_de_amigo} ({amigo_de_amigo_id})")
                                G.add_edge(amigo_id, amigo_de_amigo_id)  # Conectar el amigo con sus amigos

                # Dibujar el grafo
                ax = self.figure.add_subplot(111)
                pos = nx.spring_layout(G)
                labels = nx.get_node_attributes(G, 'label')
                node_colors = ['lightblue' if node != user_id else 'green' for node in G.nodes]
                nx.draw(G, pos, with_labels=True, labels=labels, ax=ax, node_color=node_colors, edge_color='gray',
                        node_size=2000, font_size=10)

                # Manejar eventos de clic en nodos
                def on_click(event):
                    if event.inaxes == ax:  # Si el clic es dentro del gráfico
                        for node in G.nodes:
                            xy = pos[node]
                            if (xy[0] - event.xdata) ** 2 + (xy[1] - event.ydata) ** 2 < 0.01:  # Si clic en el nodo
                                nombre = labels[node]
                                self.selected_user_id_label.setText(f"Clicked on: {nombre}")

                                # Cambiar color del nodo seleccionado y actualizar el grafo
                                node_colors = ['blue' if n == node else 'lightblue' for n in G.nodes]
                                nx.draw(G, pos, with_labels=True, labels=labels, ax=ax, node_color=node_colors,
                                        edge_color='gray',
                                        node_size=2000, font_size=10)
                                self.canvas.draw()  # Redibujar el grafo
                                break

                self.canvas.mpl_connect('button_press_event', on_click)
                self.canvas.draw()  # Actualizar el gráfico

            except mysql.connector.Error as err:
                print(f"Error fetching friends: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            print("Failed to load friends due to connection issue.")

    def center(self):
        """Centrar la ventana en la pantalla."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_complete_graph(self):
        """Cargar todos los usuarios y amistades desde la base de datos y generar el grafo completo."""
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()

                # Obtener todos los usuarios
                query_usuarios = "SELECT id, nombre FROM Usuarios"
                cursor.execute(query_usuarios)
                usuarios = cursor.fetchall()

                # Obtener todas las amistades
                query_amistades = "SELECT id_usuario1, id_usuario2 FROM Amistades"
                cursor.execute(query_amistades)
                amistades = cursor.fetchall()

                # Crear el grafo con NetworkX
                self.figure.clear()  # Limpiar la figura actual
                G = nx.Graph()

                # Añadir todos los nodos (usuarios)
                for usuario in usuarios:
                    G.add_node(usuario[0], label=usuario[1])

                # Añadir todas las relaciones de amistad (aristas)
                for amistad in amistades:
                    G.add_edge(amistad[0], amistad[1])

                # Dibujar el grafo
                ax = self.figure.add_subplot(111)
                pos = nx.spring_layout(G)
                labels = nx.get_node_attributes(G, 'label')
                node_colors = ['lightblue' for node in G.nodes]  # Todos los nodos en azul claro
                nx.draw(G, pos, with_labels=True, labels=labels, ax=ax, node_color=node_colors, edge_color='gray',
                        node_size=2000, font_size=10)

                self.canvas.draw()  # Redibujar el gráfico

            except mysql.connector.Error as err:
                print(f"Error fetching data: {err}")
            finally:
                cursor.close()
                conexion.close()
        else:
            print("Failed to load graph due to connection issue.")


# Código principal para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialNetworks()
    window.show()
    sys.exit(app.exec_())
