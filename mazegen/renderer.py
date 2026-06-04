import sys
from typing import Any
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver


class TerminalRenderer:
    def __init__(self, config: dict[str, Any], initial_gen: MazeGenerator, initial_path: str) -> None:
        self.config = config
        self.generator = initial_gen
        self.show_path = False
        self.color_idx = 0
        self.colors = ['\033[40m', '\033[43m', '\033[45m', '\033[46m']
        self.reset = '\033[0m'
        self.empty_c = '\033[47m  \033[0m'
        self.path_c = '\033[44m  \033[0m'
        self.start_c = '\033[42m  \033[0m'
        self.end_c = '\033[41m  \033[0m'
        self.c42 = '\033[40m  \033[0m'

        self._carve_center()
        ex, ey = self.config["ENTRY"]
        ox, oy = self.config["EXIT"]
        path = MazeSolver.solve(self.generator.grid, (ex, ey), (ox, oy))
        self.path = path if path else ""

    def _carve_center(self) -> None:
        w = self.generator.width
        h = self.generator.height
        if w < 6 or h < 6:
            return
        
        mid_x = w // 2
        mid_y = h // 2
        
        xs = [mid_x - 1, mid_x, mid_x + 1]
        ys = [mid_y - 1, mid_y]
        
        px_min, px_max = mid_x - 2, mid_x + 2
        py_min, py_max = mid_y - 2, mid_y + 1
        
        for y in range(py_min, py_max + 1):
            for x in range(px_min, px_max + 1):
                if y in (py_min, py_max) and x < px_max:
                    self.generator.grid[y][x] &= ~2
                    self.generator.grid[y][x+1] &= ~8
                if x in (px_min, px_max) and y < py_max:
                    self.generator.grid[y][x] &= ~4
                    self.generator.grid[y+1][x] &= ~1
                    
        for y in ys:
            for x in xs:
                self.generator.grid[y][x] = 15
                if y == ys[0]: self.generator.grid[py_min][x] |= 4
                if y == ys[-1]: self.generator.grid[py_max][x] |= 1
                if x == xs[0]: self.generator.grid[y][px_min] |= 2
                if x == xs[-1]: self.generator.grid[y][px_max] |= 8

    def generate_new(self) -> None:
        self.generator = MazeGenerator(self.config["WIDTH"], self.config["HEIGHT"])
        self.generator.generate()
        self._carve_center()
        ex, ey = self.config["ENTRY"]
        ox, oy = self.config["EXIT"]
        path = MazeSolver.solve(self.generator.grid, (ex, ey), (ox, oy))
        self.path = path if path else ""

    def draw(self) -> None:
        w = self.generator.width
        h = self.generator.height
        grid = self.generator.grid
        ex, ey = self.config["ENTRY"]
        ox, oy = self.config["EXIT"]

        out = [[self.empty_c for _ in range(w * 2 + 1)] for _ in range(h * 2 + 1)]
        wall = f"{self.colors[self.color_idx]}  {self.reset}"

        for y in range(h):
            for x in range(w):
                cx, cy = x * 2 + 1, y * 2 + 1
                cell = grid[y][x]
                
                out[cy - 1][cx - 1] = wall
                out[cy - 1][cx + 1] = wall
                out[cy + 1][cx - 1] = wall
                out[cy + 1][cx + 1] = wall
                
                if cell & 1: out[cy - 1][cx] = wall
                if cell & 2: out[cy][cx + 1] = wall
                if cell & 4: out[cy + 1][cx] = wall
                if cell & 8: out[cy][cx - 1] = wall

        if self.show_path and self.path:
            px, py = ex, ey
            out[py * 2 + 1][px * 2 + 1] = self.path_c
            for move in self.path:
                if move == 'N':
                    out[py * 2][px * 2 + 1] = self.path_c
                    py -= 1
                elif move == 'S':
                    out[py * 2 + 2][px * 2 + 1] = self.path_c
                    py += 1
                elif move == 'E':
                    out[py * 2 + 1][px * 2 + 2] = self.path_c
                    px += 1
                elif move == 'W':
                    out[py * 2 + 1][px * 2] = self.path_c
                    px -= 1
                out[py * 2 + 1][px * 2 + 1] = self.path_c

        out[ey * 2 + 1][ex * 2 + 1] = self.start_c
        out[oy * 2 + 1][ox * 2 + 1] = self.end_c

        if w >= 6 and h >= 6:
            mid_x = w // 2
            mid_y = h // 2
            start_x = mid_x * 2 - 2
            start_y = mid_y * 2 - 2
            
            p42 = [
                [1, 0, 1, 0, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1]
            ]
            
            for r in range(5):
                for c in range(7):
                    if p42[r][c]:
                        out[start_y + r][start_x + c] = self.c42
                    else:
                        out[start_y + r][start_x + c] = self.empty_c

        print("\033[H\033[J", end="") 
        print("====== A-Maze-ing ======\n")
        for row in out:
            print("".join(row))

    def loop(self) -> None:
        while True:
            self.draw()
            print("\n1. Generar nuevo laberinto")
            print("2. Mostrar/Ocultar ruta")
            print("3. Cambiar color de pared")
            print("4. Salir")
            try:
                choice = input("\nOpción (1-4): ").strip()
            except (KeyboardInterrupt, EOFError):
                sys.exit(0)
            
            if choice == '1':
                self.generate_new()
            elif choice == '2':
                self.show_path = not self.show_path
            elif choice == '3':
                self.color_idx = (self.color_idx + 1) % len(self.colors)
            elif choice == '4':
                sys.exit(0)