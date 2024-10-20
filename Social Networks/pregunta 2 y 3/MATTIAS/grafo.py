import networkx as nx
import matplotlib.pyplot as plt
from pregunta1 import *

def crear_grafo(usuarios):
    G = nx.Graph()
    
    for usuario in usuarios:
        nombre_usuario = usuario[0].strip() 
        amigos = usuario[1].split(',')
        
        for amigo in amigos:
            amigo = amigo.strip() 
            if amigo: 
                G.add_edge(nombre_usuario, amigo)
    return G

def mostrar_grafo(G):
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold', edge_color='gray')
    plt.title("Grafo de Usuarios y Amistades")
    plt.show()

# Pregunta 2: Función para recomendar nuevos amigos
def recommend_friends(graph):
    recomendaciones = {}
    for node in graph.nodes:
        amigos = set(graph.neighbors(node))  # Obtener amigos directos
        recomendados = set()
        for amigo in amigos:
            amigos_del_amigo = set(graph.neighbors(amigo)) - amigos - {node}  # Amigos del amigo, excluyendo los amigos directos
            recomendados.update(amigos_del_amigo)
        
        if recomendados:
            recomendaciones[node] = list(recomendados)
    return recomendaciones

# Pregunta 3: Función para encontrar al individuo con más amigos
def most_popular_friend(graph):
    popular_node = max(graph.nodes, key=lambda n: graph.degree(n))  # Encontrar el nodo con el mayor grado
    num_amigos = graph.degree(popular_node)
    return popular_node, num_amigos

# Ejemplo de usuarios
usuarios = [
    ("Juan", "María, Pedro"),
    ("María", "Ana"),
    ("Pedro", "Ana, Luis, Carlos")
]

# Crear grafo
G = crear_grafo(usuarios)

# Buscar grupos de amigos (importado de pregunta1.py)
#buscarGruposAmigos(G)

# Mostrar el grafo
mostrar_grafo(G)

# Llamada a la función de recomendaciones de amigos
recomendaciones = recommend_friends(G)
print("Recomendaciones de nuevos amigos:", recomendaciones)

# Llamada a la función para encontrar el amigo más popular
popular_friend, num_amigos = most_popular_friend(G)
print(f"El amigo más popular es {popular_friend} con {num_amigos} amigos.")
