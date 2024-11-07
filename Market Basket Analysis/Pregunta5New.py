def tiene_ciclo(grafo, nodo_inicio):
    visitados = set()
    pila = [(nodo_inicio, [nodo_inicio])]

    while pila:
        nodo, ruta = pila.pop()
        if nodo in visitados:
            if len(ruta) >= 3 and ruta[0] == ruta[-1]:
                return True
        else:
            visitados.add(nodo)
            for vecino in grafo[nodo]:
                pila.append((vecino, ruta + [vecino]))

    return False

grafo, _ = obtener_grafo()
for nodo in grafo:
    if tiene_ciclo(grafo, nodo):
        print(f"Se encontró un ciclo que comienza y termina en el nodo: {nodo}")
        break
else:
    print("No se encontraron ciclos")
