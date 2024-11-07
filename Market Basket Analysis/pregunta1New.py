from collections import deque

def bfs(graph, node, visited):
    queue = deque([node])
    visited.add(node)
    
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def find_friend_groups(graph):
    visited = set()
    groups = 0
    for node in graph:
        if node not in visited:
            groups += 1
            bfs(graph, node, visited)
    return groups

graph, _ = obtener_grafo()
num_grupos = find_friend_groups(graph)
print(f"Número de grupos de amigos: {num_grupos}")
