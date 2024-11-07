import networkx as nx
import matplotlib.pyplot as plt
from conexion import obtener_amistades, obtener_nombres_usuarios, conectar, cerrar_conexion


def crear_grafo(amistades, conexion):
    # Obtener los nombres de los usuarios desde la base de datos
    usuarios = obtener_nombres_usuarios(conexion)

    G = nx.Graph()

    # Recorrer las amistades y agregar las relaciones al grafo
    for usuario1, usuario2 in amistades:
        nombre_usuario1 = usuarios.get(usuario1)
        nombre_usuario2 = usuarios.get(usuario2)

        if nombre_usuario1 and nombre_usuario2:
            G.add_edge(nombre_usuario1, nombre_usuario2)

    # Visualizar el grafo con Matplotlib
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G)  # Layout de los nodos
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold',
            edge_color='gray')
    plt.title("Grafo de Usuarios y Amistades")
    plt.show()

    return G


def main():
    # Conectar a la base de datos
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Crear el grafo a partir de las amistades obtenidas
            crear_grafo(amistades, conexion)

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()
