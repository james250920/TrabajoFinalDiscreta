from Problema1 import *
def dfs_cycle(graph, node, visited, parent):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_cycle(graph, neighbor, visited, node):
                return True
        elif neighbor != parent:
            return True
    return False


# Función para detectar ciclos en el grafo
def has_cycle(graph):
    visited = set()

    # Recorremos cada nodo en el grafo
    for node in graph:
        if node not in visited:
            if dfs_cycle(graph, node, visited, None):
                return True
    return False
def main():
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Crear el grafo a partir de las amistades obtenidas
            grafo = crear_grafo(amistades, conexion)
            # Detectar si hay ciclos en la red social
            tiene_ciclo = has_cycle(grafo)
            print(f"¿La red tiene ciclos?: {tiene_ciclo}")

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()