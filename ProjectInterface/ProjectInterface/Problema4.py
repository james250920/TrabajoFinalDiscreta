
from Problema1 import *

def shortest_path(graph, person1, person2):
    from collections import deque

    queue = deque([(person1, [person1])])
    visited = set([person1])

    while queue:
        current, path = queue.popleft()

        if current == person2:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return

camino_corto = shortest_path(grafo, 1, 11)
print(f"Camino más corto: {camino_corto}")