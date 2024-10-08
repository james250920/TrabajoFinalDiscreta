from grafo import crear_grafo as grafo

def cicloGrafo(grafo):
    def DFS(nodo, visitado, padre):
        visitado[nodo] = True
        
        for vecino in grafo[nodo]:
            if not visitado[vecino]:
                if DFS(vecino, visitado, nodo):
                    return True
            elif vecino != padre:
                return True
        
        return False

    visitado = [False] * len(grafo)
    
    for i in range(len(grafo)):
        if not visitado[i]:
            if DFS(i, visitado, -1):
                return True
                
    return False
