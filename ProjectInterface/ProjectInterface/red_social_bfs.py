
import mysql.connector
from mysql.connector import Error
from collections import deque

# Conectar a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sistemas",
            database="fdiscreta"
        )

        if conexion.is_connected():
            print("Connected to the database successfully")
            return conexion

    except Error as err:
        print(f"Failed to connect to the database: {err}")
        return None

# Cerrar la conexión a la base de datos
def cerrar_conexion(conexion):
    if conexion and conexion.is_connected():
        conexion.close()
        print("Connection closed successfully")

# Obtener las amistades desde la base de datos
def obtener_amistades(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario1, id_usuario2 FROM amistades")
        amistades = cursor.fetchall()
        return amistades
    except Error as err:
        print(f"Error fetching amistades: {err}")
        return []
    finally:
        cursor.close()

# Función para obtener los nombres de los usuarios desde la base de datos
def obtener_nombres_usuarios(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Usuarios")
        usuarios = cursor.fetchall()
        # Crear un diccionario con id como clave y nombre como valor
        return {usuario[0]: usuario[1] for usuario in usuarios}
    except Error as err:
        print(f"Error fetching user names: {err}")
        return {}
    finally:
        cursor.close()

# Crear el grafo a partir de las amistades obtenidas
def crear_grafo(amistades, conexion):
    G = {}
    # Obtener los nombres de los usuarios desde la base de datos
    usuarios = obtener_nombres_usuarios(conexion)

    for usuario1, usuario2 in amistades:
        # Obtener los nombres de los usuarios
        nombre_usuario1 = usuarios.get(usuario1)
        nombre_usuario2 = usuarios.get(usuario2)

        if nombre_usuario1 and nombre_usuario2:
            if nombre_usuario1 not in G:
                G[nombre_usuario1] = []
            if nombre_usuario2 not in G:
                G[nombre_usuario2] = []
            G[nombre_usuario1].append(nombre_usuario2)
            G[nombre_usuario2].append(nombre_usuario1)

    return G

# Función para encontrar el camino más corto entre dos personas usando BFS
def shortest_path(graph, person1, person2):
    if person1 not in graph or person2 not in graph:
        return None  # Si alguna de las personas no está en el grafo, no hay camino

    # Usamos una cola para implementar BFS
    queue = deque([(person1, [person1])])  # Cada elemento es una tupla (nodo_actual, camino_hasta_aquí)
    visited = set()  # Para llevar un seguimiento de los nodos visitados

    while queue:
        current_node, path = queue.popleft()

        # Si encontramos la persona2, devolvemos el camino encontrado
        if current_node == person2:
            return path

        # Marcamos el nodo como visitado
        visited.add(current_node)

        # Exploramos los vecinos del nodo actual
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Añadimos el vecino y el camino actualizado a la cola

    # Si agotamos todos los caminos y no encontramos person2, devolvemos None
    return None

def main():
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Crear el grafo a partir de las amistades obtenidas
            grafo = crear_grafo(amistades, conexion)

            # Pedimos los nombres de las personas entre las que queremos encontrar el camino más corto
            person1 = input("Introduce el nombre de la primera persona: ")
            person2 = input("Introduce el nombre de la segunda persona: ")

            # Encontrar el camino más corto entre person1 y person2 usando BFS
            camino = shortest_path(grafo, person1, person2)

            if camino:
                print(f"El camino más corto entre {person1} y {person2} es: {' -> '.join(camino)}")
            else:
                print(f"No hay camino entre {person1} y {person2}.")

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")

if __name__ == "__main__":
    main()
