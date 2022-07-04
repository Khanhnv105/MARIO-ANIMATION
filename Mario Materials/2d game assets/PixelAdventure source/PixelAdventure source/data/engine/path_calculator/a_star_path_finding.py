from queue import PriorityQueue

NOT_COLLIDER = 0
COLLIDER = 3


def h(p1, p2):
    """
    L distance: No es la tipica distancia euclidieana,
    sino que es la suma de delta_x y delta_y entre los puntos
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Node:
    def __init__(self, row, col, state=NOT_COLLIDER):
        self.row = row
        self.col = col
        self.state = state
        self.neighbors = []

    def is_state(self, state: int):
        return self.state == state

    def set_state(self, state: int):
        self.state = state

    def get_pos(self) -> tuple:
        return self.row, self.col

    def update_neighbors(self, grid, total_columns, total_rows):
        self.neighbors.clear()

        # Checking down
        if self.row < total_rows - 1 and not grid[self.row + 1][self.col].is_state(COLLIDER):
            self.neighbors.append(grid[self.row + 1][self.col])

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_state(COLLIDER):
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right
        if self.col < total_columns - 1 and not grid[self.row][self.col + 1].is_state(COLLIDER):
            self.neighbors.append(grid[self.row][self.col + 1])

        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_state(COLLIDER):
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

    def __repr__(self):
        return f"({self.row}, {self.col}, {self.state})"


class AStarPathFinding:
    def __init__(self, binary_grid):
        self.binary_grid = binary_grid

        self.rows = len(self.binary_grid)
        self.columns = len(self.binary_grid[0])
        self.grid = []
        self._make_grid()

    def get_path(self, start_grid_pos: tuple, end_grid_pos: tuple):
        
        """
        Retorna el conjunto de puntos que une la posicion inicial
        con la posicion final. En el caso de que sea imposible llegar
        al punto final o que los puntos de START o END no esten en el
        array se retorna None
        
        """
        
        start_pos = int(start_grid_pos[0]), int(start_grid_pos[1])
        end_pos = int(end_grid_pos[0]), int(end_grid_pos[1])

        if self._is_in_grid(start_pos) and self._is_in_grid(end_pos):
            start_node = self.grid[start_pos[1]][start_pos[0]]
            end_node = self.grid[end_pos[1]][end_pos[0]]

            return self._algorithm(start_node, end_node)

    def _is_in_grid(self, point: tuple):
        return point[0] < len(self.grid[0]) and point[1] < len(self.grid)

    def _make_grid(self):
        self.grid.clear()

        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.columns):
                node = Node(
                    row=row,
                    col=col,
                    state=COLLIDER if self.binary_grid[row][col] else NOT_COLLIDER
                )
                self.grid[row].append(node)

        for row in self.grid:
            for node in row:
                node.update_neighbors(
                    self.grid,
                    self.columns,
                    self.rows
                )

    def _reconstruct_path(self, came_from: dict, current: Node):
        points = []
        while current in came_from:
            current = came_from[current]
            points.append(current.get_pos())
        return points

    def _algorithm(self, start: Node, end: Node):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))

        came_from = {}

        # Guarda la distancia de cada uno de los nodos desde si mismos hacia el start_node
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[start] = 0

        # Guarda la distancia de cada uno de los nodos desde si mismos hacia el start_end
        f_score = {node: float("inf") for row in self.grid for node in row}
        f_score[start] = h(start.get_pos(), end.get_pos())

        # Lista en la cual guardamos todos los nodos abiertos
        open_set_hash = {start}

        while not open_set.empty():
            # Obtenemos el primer nodo
            current_node = open_set.get()[2]
            open_set_hash.remove(current_node)

            # Si es que llego al final retorno
            # la lista de posiciones del path
            if current_node == end:
                return self._reconstruct_path(came_from, end)

            # Buscamos en todos los neighbors
            for neighbor in current_node.neighbors:
                temp_g_score = g_score[current_node] + 1

                # Si es que el g_score es menor que el actual
                # actualizo el g_score dado a que es un mejor path
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)


""""import time
size = 100
binary_grid = [[0 for _ in range(size)] for _ in range(size)]

calculator = AStarPathFinding(binary_grid)

i = time.time()
points = calculator.get_path((0, 0), (99, 99))
print(time.time() - i)

for point in points:
    binary_grid[point[0]][point[1]] = 3


def good_print(l):
    for row in l:
        print(row)


good_print(binary_grid)"""
