from collections import deque
from typing import Optional

class MazeSolver:
    DIRECTIONS = {
        'N': (0, -1, 1),
        'E': (1, 0, 2),
        'S': (0, 1, 4),
        'W': (-1, 0, 8)
    }

    @staticmethod
    def solve(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> Optional[str]:
        width = len(grid[0])
        height = len(grid)
        queue = deque([(start[0], start[1], "")])
        visited = {start}

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == end:
                return path

            cell_walls = grid[y][x]

            for dir_name, (dx, dy, wall_bit) in MazeSolver.DIRECTIONS.items():
                if not (cell_walls & wall_bit):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + dir_name))

        return None
