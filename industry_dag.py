import matplotlib.pyplot as plt
import networkx as nx


G = nx.DiGraph() 
G.add_nodes_from([
    "HYBE Corporation", "SM Entertainment", "YG Entertainment", "JYP Entertainment",
    "WakeOne Entertainment", "Grandline Group", "KQ Entertainment", "High Up Entertainment",
    "Cube Entertainment", "Big Hit Music", "Belift Music", "Source Music", "KOZ Entertainment",
    "ADOR", "Mystic Story", "APop", "The Black Label", "Squ4d"
])

# Add directed edges
G.add_edges_from([
    ("HYBE Corporation", "Big Hit Music"),
    ("HYBE Corporation", "Belift Music"),
    ("HYBE Corporation", "Source Music"),
    ("HYBE Corporation", "KOZ Entertainment"),
    ("HYBE Corporation", "ADOR"),
    ("SM Entertainment","Mystic Story"),
    ("Mystic Story","APop"),
    ("YG Entertainment","The Black Label"),
    ("JYP Entertainment","Squ4d")])

   
large_nodes = {"HYBE Corporation", "SM Entertainment", "YG Entertainment", "JYP Entertainment"}

# Set node sizes: larger for key labels, smaller for others
node_sizes = [5000 if node in large_nodes else 1000 for node in G.nodes()]
color=['pink' if node in large_nodes else 'lightblue' for node in G.nodes()]

# Visualize the DAG 
plt.figure(figsize=(20, 15))
pos = nx.kamada_kawai_layout(G)
nx.draw_networkx(G, pos, with_labels=True,node_size=node_sizes, node_color=color, font_size=10, font_weight='bold', arrows=True)
plt.title("K-pop Industry")
plt.axis('off')
plt.show()
