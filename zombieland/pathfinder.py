from collections import deque
from zombieland.settings import MAP_COL, MAP_ROW

class Node:
    def __init__(self, x, y, walkable, neighbors):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.neighbors = neighbors
        self.parent = None
        self.g_cost = float("inf")
        self.h_cost = float("inf")

    def __str__(self):
        return f'Node ({self.x}, {self.y})'

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost

class PathFinder:
    def __init__(self, map_layout, wall_coors):
        self.map = map_layout
        self.walls = wall_coors
        self.mode = 'bfs'
        self.directions = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]
        self.nodes: dict[tuple[int, int]:Node] = {}
        self.graph = self.get_graph()

    def set_search_mode(self, mode):
        self.mode = mode

    def get_path(self, start, goal):
        path: list[tuple[int, int]] = []
        if self.mode == 'bfs':
            path = self._get_path_by_bfs(start, goal)
        elif self.mode == 'a*':
            path = self._get_path_by_a_star(start, goal)
        return path

    def _get_path_by_bfs(self, start, goal):
        visited = self.breadth_first_search(start, goal)
        path = [goal]
        step = visited.get(goal, start)
        while step and step != start:
            path.append(step)
            step = visited[step]
        return path

    def breadth_first_search(self, start, goal):
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            next_nodes = self.graph.get(current, [])
            for node in next_nodes:
                if node not in visited:
                    queue.append(node)
                    visited[node] = current
        return visited

    def get_neighbors(self, x, y):
        return [(x+dx, y+dy) for dx, dy in self.directions if (x+dx, y+dy) not in self.walls]

    def get_graph(self):
        graph = {}
        for y, row in enumerate(self.map):
            for x, val in enumerate(row):
                if val == '-1':
                    graph[(x, y)] = self.get_neighbors(x, y)
        return graph

    def _get_path_by_a_star(self, start, end):
        self.a_star_search(start, end)
        path = []
        current = self.graph[end]
        while current != self.graph[start]:
            path.append((current.x, current.y))
            current = current.parent
        return path

    def a_star_search(self, start, end):
        self.nodes = self.get_nodes()
        open_set: list[Node] = []
        closed_set = []
        open_set.append(self.graph[start])

        while len(open_set) > 0:
            current = open_set[0]
            for i in range(1, len(open_set)):
                if open_set[i].f_cost < current.f_cost or (open_set[i].f_cost == current.f_cost and open_set[i].h_cost < current.h_cost):
                    current = open_set[i]
            open_set.remove(current)
            closed_set.append(current)

            if (current.x, current.y) == end:
                return

            for neighbor in current.neighbors:
                if not self.nodes[neighbor].walkable or self.nodes[neighbor] in closed_set:
                    continue

                new_move_cost = current.g_cost + self.get_dist(current, self.nodes[neighbor])
                if new_move_cost < self.nodes[neighbor].g_cost or self.nodes[neighbor] not in open_set:
                    self.nodes[neighbor].g_cost = new_move_cost
                    self.nodes[neighbor].h_cost = self.get_dist(self.nodes[neighbor], self.nodes[end])
                    self.nodes[neighbor].parent = current
                    if self.nodes[neighbor] not in open_set:
                        open_set.append(self.nodes[neighbor])

    def get_neighbor_nodes(self, x, y):
        return [(x+dx, y+dy) for dx, dy in self.directions if 0 < x+dx < MAP_COL and 0 < y+dy < MAP_ROW]

    @staticmethod
    def get_dist(a, b):
        x_dist = abs(a.x - b.x)
        y_dist = abs(a.y - b.y)
        if x_dist > y_dist:
            return 14*y_dist + 10*(x_dist-y_dist)
        else:
            return 14*x_dist + 10*(y_dist-x_dist)

    def get_nodes(self):
        nodes = {}
        for y, row in enumerate(self.map):
            for x, val in enumerate(row):
                walkable = True if val == '-1' else False
                neighbors = self.get_neighbor_nodes(x, y)
                nodes[(x, y)] = Node(x, y, walkable, neighbors)
        return nodes


