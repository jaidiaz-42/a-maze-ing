import sys
import os
from typing import Dict, Any, Tuple, List

# Importamos nuestros módulos internos desde el paquete src
from src.config import ConfigParser
from src.matrix import MazeMatrix
from src.generator import MazeGenerator
from src.solver import MazeSolver
from src.display import MazeDisplay


def get_key() -> str:
    # added type ignores to work with windows and check lints
    if os.name == 'nt':
        import msvcrt  # type: ignore
        try:
            ch = msvcrt.getch().decode('utf-8').lower()  # type: ignore
            return ch
        except Exception:
            return ""
    else:
        # linux / macOS
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)  # type: ignore[attr-defined]
        try:
            tty.setraw(sys.stdin.fileno())  # type: ignore[attr-defined]
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,  # type: ignore[attr-defined]
                              termios.TCSADRAIN,  # type: ignore[attr-defined]
                              old_settings)
        return ch.lower()


def run_maze_pipeline(config: Dict[str, Any]) -> Tuple[
     MazeMatrix, List[Tuple[int, int]]]:
    # 1. Create the maze with the specified dimensions and apply the "42"
    matrix = MazeMatrix(config["WIDTH"], config["HEIGHT"])

    # 2. Generate walls using the DFS algorithm, starting from the ENTRY point
    generator = MazeGenerator(matrix)
    generator.generate(start_x=config["ENTRY"][0], start_y=config["ENTRY"][1])

    # 3. Solve using DFS to find the shortest path from ENTRY to EXIT
    solver = MazeSolver(matrix)
    path = solver.solve(config["ENTRY"], config["EXIT"])

    # 4. Save to file the generated maze and the solution path
    solver.save_to_file(config["OUTPUT_FILE"],
                        config["ENTRY"],
                        config["EXIT"],
                        path)

    return matrix, path


def main() -> None:
    # Validación estricta de argumentos (Capítulo IV.2: Usage)
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py <archivo_de_configuracion>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # Parsear y validar el archivo de configuración
        parser = ConfigParser(config_file)
        config = parser.parse()
    except Exception as e:
        print(f"Error al cargar la configuración: {e}", file=sys.stderr)
        sys.exit(1)

    # Generación inicial del laberinto
    matrix, path = run_maze_pipeline(config)

    # Inicializar el visualizador interactivo
    display = MazeDisplay(matrix, config["ENTRY"], config["EXIT"], path)

    # Bucle de interacción principal (Capítulo V del Subject)
    while True:
        display.render()

        # Quedarse escuchando la siguiente tecla del usuario
        key = get_key()

        if key == 'q':
            # Salir limpiamente del programa
            print("\n¡Gracias por usar 42 A-Maze-ing! Saliendo...\n")
            break

        elif key == 'h':
            # Mostrar / Ocultar la solución (Toggle)
            display.toggle_path()

        elif key == 'c':
            # Cambiar paleta de colores de las paredes dinámicamente
            display.change_color()

        elif key == 'r':
            # Generate ramdon maze
            matrix, path = run_maze_pipeline(config)
            # Actualizamos las referencias internas del visualizador
            display.matrix = matrix
            display.path = path


if __name__ == "__main__":
    main()
