import streamlit as st
import math
import heapq
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

# Set Page Config
st.set_page_config(
    page_title="Hospital Robot Route Planner",
    page_icon="🏥",
    layout="wide"
)

# write meaningful title and description for the app
st.title("🏥 Emergency Supply Robot: Informed Search Visualizer")

st.write(
    "An autonomous robot delivers emergency medical supplies inside a hospital. "
    "Choose a start location, a goal location and a search algorithm "
    "(**Greedy Best-First Search** or **A\\***). The app finds a route on the "
    "hospital graph using the Euclidean distance heuristic and highlights the "
    "solution path."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)

if st.button("Run Search"):

    if algorithm == "GBFS":

        # run the GBFS algorithm with the selected start and goal nodes
        path, cost = gbfs(start, goal)
    else:

        # run the A* algorithm with the selected start and goal nodes
        path, cost = a_star(start, goal)

    if path is None:

       # display a error message indicating that no path was found
       st.error(f"No path found from {start} to {goal}.")

    else:

        # Display result
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )



        # Visualize NetworkX graph

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

               G.add_edge(node, neighbor, weight=weight)
        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        path_edges = list(zip(path, path[1:]))

        node_colors = []
        for node in G.nodes():
            if node == start:
                node_colors.append("#4CAF50")      # start = green
            elif node == goal:
                node_colors.append("#FFC107")      # goal = amber
            elif node in path:
                node_colors.append("#FF8A80")      # on the path = light red
            else:
                node_colors.append("#90CAF9")      # others = light blue

        # all nodes
        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=2600, ax=ax
        )

        # all edges (grey)
        nx.draw_networkx_edges(
            G, pos, edge_color="gray", width=1.5, arrows=True,
            arrowsize=18, node_size=2600, ax=ax
        )

        # solution path edges (red, thick)
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=4,
            arrows=True, arrowsize=22, node_size=2600, ax=ax
        )

        nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_size=9, ax=ax
        )

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)
