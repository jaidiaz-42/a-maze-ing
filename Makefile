# Variables
POETRY = poetry
CONFIG = config.txt

.PHONY: all install run debug clean lint

all: install lint

install:
	@echo "Instalando entorno y dependencias con Poetry..."
	$(POETRY) install
	@echo "Compilando el proyecto..."
	$(POETRY) build
	@echo "Colocando el archivo .whl en la raíz del repositorio..."
	@cp dist/*.whl .
	@echo "Entorno listo y empaquetado completado."

run:
	@if [ ! -f $(CONFIG) ]; then \
		echo " Error: No se encuentra el archivo $(CONFIG)."; \
		exit 1; \
	fi
	$(POETRY) run python3 a_maze_ing.py $(CONFIG)

debug:
	$(POETRY) run python3 -m pdb a_maze_ing.py $(CONFIG)

clean:
	@echo " Limpiando residuos de compilación..."
	rm -rf dist build *.egg-info .mypy_cache
	rm -f *.whl
	@echo " Directorio limpio."

lint:
	@echo " Pasando Flake8 (Estilo)..."
	$(POETRY) run flake8 a_maze_ing.py src/
	@echo " Pasando Mypy (Tipado)..."
	$(POETRY) run mypy --disallow-untyped-defs --check-untyped-defs a_maze_ing.py src/