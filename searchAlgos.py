"""Search algorithms and hospital graph shared by the notebook (Task 3) and the Streamlit GUI."""
import math
import heapq

# Hospital coordinates (Task 3)
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

# Hospital weighted (directed) graph (Task 3)
hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current, goal, coords=locations):
    """Euclidean distance between two nodes."""
    (x1, y1), (x2, y2) = coords[current], coords[goal]
    return math.hypot(x1 - x2, y1 - y2)


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def path_cost(path, graph):
    return sum(graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal, graph=hospital_graph, coords=locations):
    """Greedy Best-First Search, f(n) = h(n). Returns (path, cost, expansion_order)."""
    frontier = [(heuristic(start, goal, coords), start)]
    came_from, visited, expansion_order = {}, set(), []
    in_frontier = {start}
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, path_cost(path, graph), expansion_order
        for nb in graph[current]:
            if nb not in visited and nb not in in_frontier:
                came_from[nb] = current
                in_frontier.add(nb)
                heapq.heappush(frontier, (heuristic(nb, goal, coords), nb))
    return None, None, expansion_order


def weighted_a_star(start, goal, graph=hospital_graph, weight=1.0, coords=locations):
    """f(n) = g(n) + w*h(n). Returns (path, cost, expansion_order, g_cost)."""
    frontier = [(weight * heuristic(start, goal, coords), start)]
    g_cost, came_from = {start: 0.0}, {}
    closed, expansion_order = set(), []
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.add(current)
        expansion_order.append(current)
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_cost[current], expansion_order, g_cost
        for nb, c in graph[current].items():
            new_g = g_cost[current] + c
            if nb not in g_cost or new_g < g_cost[nb]:
                g_cost[nb] = new_g
                came_from[nb] = current
                heapq.heappush(frontier, (new_g + weight * heuristic(nb, goal, coords), nb))
    return None, None, expansion_order, g_cost


def a_star(start, goal, graph=hospital_graph, coords=locations):
    """A* Search, f(n) = g(n) + h(n). Returns (path, cost, expansion_order)."""
    path, cost, order, _ = weighted_a_star(start, goal, graph, 1.0, coords)
    return path, cost, order
