import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Graph, Use Case: Emergency Supply Robot

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}
# Heuristic
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Path reconstruction
def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path

# GBFS


def gbfs(start, goal):

    # priority = h(n); queue entries: (h(n), node, parent)
    frontier = [(heuristic(start, goal), start, None)]
    came_from = {}
    explored = set()

    while frontier:

        h, current, parent = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)
        came_from[current] = parent

        if current == goal:
            path = reconstruct_path(came_from, current)
            cost = sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))
            return path, cost

        for neighbor in hospital_graph[current]:
            if neighbor not in explored:
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), neighbor, current)
                )

    return None, None

# A*
def a_star(start, goal):

    # priority = f(n) = g(n) + h(n); queue entries: (f(n), g(n), node)
    g_cost = {start: 0}
    came_from = {start: None}
    frontier = [(heuristic(start, goal), 0, start)]

    while frontier:

        f, g, current = heapq.heappop(frontier)

        if g > g_cost[current]:      # outdated entry, a cheaper route was found
            continue

        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current]

        for neighbor, cost in hospital_graph[current].items():

            tentative_g = g_cost[current] + cost

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor)
                )

    return None, None
