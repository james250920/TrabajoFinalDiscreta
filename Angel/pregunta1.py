from grafo import crear_grafo as grafo
from collections import deque


def bfs(grafo, nodo, visitados):
    cola = deque([nodo])
    while cola:
        aux = cola.popleft()
        if aux not in visitados:
            visitados.add(aux)
            for neighbor in grafo[aux]:
                if neighbor not in visitados:
                    cola.append(neighbor)

def find_friend_groups(grafo):
    visitados = set()
    grupos = 0
    
    for nodo in grafo:
        if nodo not in visitados:
            bfs(grafo, nodo, visitados)
            grupos += 1
    
    return grupos