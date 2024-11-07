from conexion import obtener_amistades, obtener_nombres_usuarios, conectar, cerrar_conexion


# DFS para recorrer los nodos de forma recursiva
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


# Encontrar los grupos de amigos (componentes conexos)
def find_friend_groups(graph):
    visited = set()
    groups = 0

    # Recorremos cada nodo en el grafo
    for node in graph:
        if node not in visited:
            groups += 1
            dfs(graph, node, visited)

    return groups


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


# DFS para detectar ciclos
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

            # Encontrar los grupos de amigos (componentes conexos)
            grupos = find_friend_groups(grafo)
            print(f"Número de grupos de amigos: {grupos}")

            # Detectar si hay ciclos en la red social
            tiene_ciclo = has_cycle(grafo)
            print(f"¿La red tiene ciclos?: {tiene_ciclo}")

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()
