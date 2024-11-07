from collections import defaultdict
import networkx as nx

def build_cooccurrence_graph(transactions, k):

    cooccurrence_counts = defaultdict(int)

    for transaction in transactions:
        items = list(transaction)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair = tuple(sorted([items[i], items[j]])) 
                cooccurrence_counts[pair] += 1


    G = nx.Graph()


    for pair, count in cooccurrence_counts.items():
        if count >= k:
            G.add_edge(pair[0], pair[1])

    return G