# archivo: grafo.py

import networkx as nx
from conexion import obtener_amistades, obtener_nombres_usuarios, conectar, cerrar_conexion


def most_popular_friend(graph):
    # Inicializamos las variables para almacenar el usuario más popular
    max_friends = -1
    most_popular = None

    # Recorremos todos los nodos en el grafo
    for node in graph.nodes:
        # Obtenemos el grado del nodo (número de amigos)
        num_friends = graph.degree(node)

        # Si este nodo tiene más amigos que el actual más popular, lo actualizamos
        if num_friends > max_friends:
            max_friends = num_friends
            most_popular = node

    return most_popular, max_friends


def crear_grafo(amistades, conexion):
    usuarios = obtener_nombres_usuarios(conexion)
    G = nx.Graph()

    # Recorrer las amistades y agregar las relaciones al grafo
    for usuario1, usuario2 in amistades:
        nombre_usuario1 = usuarios.get(usuario1)
        nombre_usuario2 = usuarios.get(usuario2)

        if nombre_usuario1 and nombre_usuario2:
            G.add_edge(nombre_usuario1, nombre_usuario2)

    return G


def main():
    # Conectar a la base de datos
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Crear el grafo a partir de las amistades obtenidas
            grafo = crear_grafo(amistades, conexion)

            # Encontrar el usuario más popular
            user, friends_count = most_popular_friend(grafo)
            print(f"El usuario más popular es {user} con {friends_count} amigos.")

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()
