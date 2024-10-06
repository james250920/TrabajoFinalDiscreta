import networkx as nx
import matplotlib.pyplot as plt
from usuarios import usuarios as u

def crear_grafo(u):
    G = nx.Graph()
    
    for usuario in u:
        nombre_usuario = usuario[0].strip() 
        amigos = usuario[1].split(',')
        
        for amigo in amigos:
            amigo = amigo.strip() 
            if amigo: 
                G.add_edge(nombre_usuario, amigo)
    
    def mostrar_grafo(G):
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G) 
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold', edge_color='gray')
        plt.title("Grafo de Usuarios y Amistades")
        plt.show()

    mostrar_grafo(G)
    return G



