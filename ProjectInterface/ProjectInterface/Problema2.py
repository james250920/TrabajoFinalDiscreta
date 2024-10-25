from grafo import *
from Problema1 import *
def recommend_friends(graph):
    recommendations = {}

    for person in graph:
        friends = set(graph[person])
        mutual_friends = set()

        for friend in friends:
            for mutual in graph[friend]:
                if mutual != person and mutual not in friends:
                    mutual_friends.add(mutual)

        recommendations[person] = list(mutual_friends)

    return recommendations

recomendaciones = recommend_friends(grafo)
print(f"Recomendaciones de amistad: {recomendaciones}")