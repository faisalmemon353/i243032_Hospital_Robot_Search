import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# import the necessary functions and variables from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

st.set_page_config(page_title="Hospital Robot Search Visualizer", page_icon="🏥", layout="wide")

st.title("🏥 Hospital Emergency Supply Robot - Search Visualizer")
st.write(
    "Pick a start node, a goal node and a search algorithm (**GBFS** or **A\\***). "
    "The app runs the search on the hospital corridor graph, highlights the solution path "
    "on the NetworkX graph, and shows the path and its total cost."
)

nodes = list(hospital_graph.keys())

col1, col2, col3 = st.columns(3)
with col1:
    start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
with col2:
    goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
with col3:
    algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal, hospital_graph)
    else:
        path, cost, expansion_order = a_star(start, goal, hospital_graph)

    if path is None:
        st.error(f"No path found from {start} to {goal}. (Corridors are one-way; try a different pair.)")

    else:
        # Visualize NetworkX graph
        G = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        pos = locations

        path_edges = list(zip(path, path[1:]))
        colors = ["lightgreen" if n == start else "gold" if n == goal
                  else "salmon" if n in path else "lightblue" for n in G.nodes]

        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2200, edgecolors="black", ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, arrowsize=20, node_size=2200, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=4,
                               arrows=True, arrowsize=25, node_size=2200, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"),
                                     font_size=9, ax=ax)
        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)

        # Display result
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Expansion Order:** {' → '.join(expansion_order)}")
