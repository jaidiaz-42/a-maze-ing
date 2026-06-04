# A-Maze-ing

## Descripción
Nuestro proyecto es un generador y resolutor de laberintos implementado en Python. Los desarrolladores hemos creado una herramienta matemática que genera cuadrículas de dimensiones personalizadas y encuentra la ruta de salida utilizando un algoritmo de búsqueda de rutas (BFS). El resultado se renderiza de forma interactiva directamente en la terminal utilizando secuencias de escape ANSI, prescindiendo de librerías gráficas externas problemáticas en entornos de subsistema.

## Características
- Generación procedimental de laberintos garantizando la ausencia de bucles y celdas aisladas.
- Resolución automática del camino desde el punto de entrada hasta la salida.
- Interfaz gráfica fluida basada en terminal.
- Controles interactivos en tiempo real para regenerar, alternar la visibilidad de la ruta y modificar la paleta de colores.
- Configuración parametrizada mediante archivo `config.txt`.
- Exportación automática del trazado y la solución a archivo de texto plano (`maze.txt`).

## Requisitos
- Python 3.12 o superior.
- Utilidad `make` instalada en el sistema.

## Instalación
Prepara el entorno virtual y las dependencias necesarias ejecutando:
```bash
make install
```

## Ejecución
Para iniciar el renderizador interactivo, ejecuta:
```bash
make run
```

## Controles
Una vez iniciado el programa, introduce la opción numérica y presiona Enter:
- **1**: Generar nueva estructura matemática.
- **2**: Mostrar/Ocultar la ruta de solución.
- **3**: Cambiar el color de las paredes.
- **4**: Salir de la aplicación de forma segura.

## Team Management
- Roles: Arquitectura, lógica de generación y testing a cargo conjunto de **jaidiaz-** y **jotriano**.

La arquitectura, lógica de generación y renderizado de este proyecto han sido ideadas y programadas íntegramente de forma conjunta por los estudiantes de 42: **jaidiaz-** y **jotriano**. Todas las fases de pruebas, depuración de errores y validación matemática de la resolución de los laberintos han sido ejecutadas y verificadas en conjunto por ambos desarrolladores. No se han utilizado aportaciones externas ni individuales en el código fuente.