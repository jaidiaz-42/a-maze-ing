import random
from typing import Optional

class MazeGenerator:
    DIRECTIONS = {
        'N': (0, -1, 1, 4),
        'E': (1, 0, 2, 8),
        'S': (0, 1, 4, 1),
        'W': (-1, 0, 8, 2)
    }

    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        # Inicializa la matriz con 15 (1111 en binario, todas las paredes cerradas)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        if seed is not None:
            random.seed(seed)

    def generate(self) -> None:
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        visited = {(start_x, start_y)}
        stack = [(start_x, start_y)]

        while stack:
            cx, cy = stack[-1]
            neighbors = []

            for direction, (dx, dy, wall, opp_wall) in self.DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    neighbors.append((nx, ny, wall, opp_wall))

            if neighbors:
                nx, ny, wall, opp_wall = random.choice(neighbors)
                # Derriba la pared de la celda actual y la pared opuesta de la celda vecina
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp_wall
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
