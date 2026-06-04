import sys
from typing import Any
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver
from mazegen.renderer import TerminalRenderer


def parse_config(filepath: str) -> dict[str, Any]:
    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    config: dict[str, Any] = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    raise ValueError(f"Sintaxis inválida en línea {line_num}")
                key, value = [part.strip() for part in line.split('=', 1)]
                
                if key in ["WIDTH", "HEIGHT"]:
                    config[key] = int(value)
                elif key in ["ENTRY", "EXIT"]:
                    config[key] = tuple(map(int, value.split(',')))
                elif key == "PERFECT":
                    config[key] = value.lower() in ('true', '1', 'yes', 't')
                else:
                    config[key] = value
                    
        if missing := mandatory_keys - config.keys():
            raise ValueError(f"Faltan claves: {', '.join(missing)}")
    except Exception as e:
        sys.exit(f"Error al analizar configuración: {e}")
    return config


def write_maze_file(filename: str, grid: list[list[int]], start: tuple[int, int], end: tuple[int, int], path: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for row in grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")
            f.write("\n")
            f.write(f"{start[0]},{start[1]}\n")
            f.write(f"{end[0]},{end[1]}\n")
            f.write(f"{path}\n")
    except Exception as e:
        sys.exit(f"Error al escribir el archivo: {e}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 a_maze_ing.py <config.txt>")

    config = parse_config(sys.argv[1])
    width, height = config["WIDTH"], config["HEIGHT"]
    ex, ey = config["ENTRY"]
    ox, oy = config["EXIT"]

    if not (0 <= ex < width and 0 <= ey < height):
        sys.exit(f"Error: ENTRY {ex},{ey} fuera de rango. Max permitido: {width-1},{height-1}")
    if not (0 <= ox < width and 0 <= oy < height):
        sys.exit(f"Error: EXIT {ox},{oy} fuera de rango. Max permitido: {width-1},{height-1}")

    generator = MazeGenerator(width, height)
    generator.generate()
    
    path = MazeSolver.solve(generator.grid, (ex, ey), (ox, oy))
    if path is None:
        sys.exit(f"Error crítico: Resolutor no encontró ruta válida desde {ex},{ey} hasta {ox},{oy}.")
        
    write_maze_file(config["OUTPUT_FILE"], generator.grid, (ex, ey), (ox, oy), path)
    
    renderer = TerminalRenderer(config, generator, path)
    renderer.loop()


if __name__ == "__main__":
    main()
