from itertools import combinations
from collections import defaultdict
from datos import transacciones

k = int(input("¿En cuántas transacciones desea que se muestren los conjuntos de productos? "))

def frequent_itemsets(transacciones, k):
    itemTrans = defaultdict(int)
    
    for t in transacciones:
        for r in range(2, 7):  
            for s in combinations(t, r):
                itemTrans[frozenset(s)] += 1
    
    agrupado = defaultdict(list)

    for itemset, cant in itemTrans.items():
        if cant >= k:  
            agrupado[len(itemset)].append(set(itemset))
    
    return agrupado

agrupados = frequent_itemsets(transacciones, k)
print(f"Subconjuntos frecuentes agrupados por tamaño de conjunto (al menos {k} apariciones):")
for tamaño, s in sorted(agrupados.items()):
    print(f"\nConjuntos de tamaño {tamaño}:")
    for sub in s:
        print(sub)