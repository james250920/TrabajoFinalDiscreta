from collections import defaultdict
import networkx as nx

def build_cooccurrence_graph(transactions, k):
    cooccurrence_counts = defaultdict(int)

    # Contar las co-ocurrencias de cada par de artículos
    for transaction in transactions:
        items = list(transaction)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair = tuple(sorted([items[i], items[j]]))
                cooccurrence_counts[pair] += 1

    # Construir el grafo
    G = nx.Graph()
    for pair, count in cooccurrence_counts.items():
        if count >= k:
            G.add_edge(pair[0], pair[1])

    return G

def dfs(graph, start, visited):
    stack = [start]
    component = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            component.add(node)
            # Agregar nodos adyacentes a la pila si no han sido visitados
            stack.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)
    
    return component

def find_communities_dfs(graph):
    visited = set()
    communities = []

    for node in graph.nodes():
        if node not in visited:
            component = dfs(graph, node, visited)
            communities.append(component)

    return communities

# Ejemplo de uso
transactions = [
    ['bread', 'milk', 'butter'],
    ['bread', 'milk'],
    ['milk', 'butter'],
    ['apple', 'banana'],
    ['apple', 'orange']
]

k = 2  # Umbral de co-ocurrencia mínimo
graph = build_cooccurrence_graph(transactions, k)
communities = find_communities_dfs(graph)

print("Comunidades de artículos que suelen comprarse juntos:")
for i, community in enumerate(communities, start=1):
    print(f"Comunidad {i}: {community}")
