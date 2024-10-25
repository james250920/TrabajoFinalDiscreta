from Problema1 import *
def has_cycle(graph):
    def dfs(node, visited, parent):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, visited, node):
                    return True
            elif neighbor != parent:
                return True

        return False

    visited = set()

    for node in graph:
        if node not in visited:
            if dfs(node, visited, None):
                return True

    return False

tiene_ciclo = has_cycle(grafo)
print(f"¿La red tiene ciclos?: {tiene_ciclo}")