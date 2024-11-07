from collections import deque
import matplotlib.pyplot as plt
from conexion import obtener_amistades, obtener_nombres_usuarios, conectar, cerrar_conexion
import networkx as nx

# Función que implementa BFS para encontrar el camino más corto
def shortest_path(graph, person1, person2):
    # Verificar si las dos personas están en el grafo
    if person1 not in graph or person2 not in graph:
        return None

    # Utilizar una cola para realizar BFS
    queue = deque([(person1, [person1])])  # Cada elemento es (nodo_actual, camino)

    # Conjunto para rastrear los nodos visitados
    visited = set()

    while queue:
        current_person, path = queue.popleft()

        # Marcar como visitado el nodo actual
        if current_person in visited:
            continue
        visited.add(current_person)

        # Verificar si llegamos a la persona objetivo
        if current_person == person2:
            return path  # Retorna el camino encontrado

        # Añadir los vecinos no visitados a la cola
        for neighbor in graph.neighbors(current_person):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None  # Retorna None si no existe un camino entre person1 y person2



# Crear el grafo de amistades
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

# Probar la búsqueda del camino más corto entre dos usuarios
def probar_camino_mas_corto(graph, person1, person2):
    camino = shortest_path(graph, person1, person2)
    if camino:
        print(f"Camino más corto entre {person1} y {person2}: {' -> '.join(camino)}")
    else:
        print(f"No existe un camino entre {person1} y {person2}")

# Función principal
def main():
    # Conectar a la base de datos
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Crear el grafo a partir de las amistades obtenidas
            G = crear_grafo(amistades, conexion)

            # Probar la búsqueda del camino más corto entre dos personas
            # Cambia los valores de person1 y person2 para probar con usuarios específicos
            person1 = "nombre_usuario1"  # Reemplaza con un nombre de usuario válido
            person2 = "nombre_usuario2"  # Reemplaza con un nombre de usuario válido
            probar_camino_mas_corto(G, person1, person2)

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")

if __name__ == "__main__":
    main()
