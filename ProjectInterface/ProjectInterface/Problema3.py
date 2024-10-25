
from Problema2 import *
from TrabajoFinalDiscreta.ProjectInterface.ProjectInterface.conexion import usuarios



def most_popular_friend(graph, usuarios):
    most_popular = None
    max_friends = -1
    popular_name = None

    for person in graph:
        num_friends = len(graph[person])
        if num_friends > max_friends:
            most_popular = person
            max_friends = num_friends

    for usuario in usuarios:
        if usuario[0] == most_popular:
            popular_name = usuario[1]
            break

    return popular_name, max_friends

persona_popular, num_amigos = most_popular_friend(grafo, usuarios)
print(f"Persona más popular: {persona_popular}, con {num_amigos} amigos")