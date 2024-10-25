from grafo import *
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


def find_friend_groups(graph):
    visited = set()
    groups = 0

    for node in graph:
        if node not in visited:
            groups += 1
            dfs(graph, node, visited)

    return groups

grafo, _ = obtener_grafo()
num_grupos = find_friend_groups(grafo)
print(f"Número de grupos de amigos: {num_grupos}")