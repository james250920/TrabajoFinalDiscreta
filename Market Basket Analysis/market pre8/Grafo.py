from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from ConDB import mysql, conectar


db = conectar()
cursor = db.cursor()

query = """
    SELECT transaction_id, item_name
    FROM Transaction_Items
    ORDER BY transaction_id;
"""

cursor.execute(query)
transactions_data = cursor.fetchall()

# Cerrar la conexión
cursor.close()
db.close()


transactions = defaultdict(list)
for transaction_id, item_name in transactions_data:
    transactions[transaction_id].append(item_name)


transactions_list = list(transactions.values())
cooccurrence_counts = defaultdict(int)


for transaction in transactions_list:
    items = list(transaction)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            pair = tuple(sorted([items[i], items[j]]))
            cooccurrence_counts[pair] += 1


G = nx.Graph()

for pair, count in cooccurrence_counts.items():
    if count >= 2:  # Umbral k = 2
        G.add_edge(pair[0], pair[1], weight=count)


plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2500, font_size=10)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo de Co-ocurrencia de Artículos Comprados Juntos")
plt.show()
