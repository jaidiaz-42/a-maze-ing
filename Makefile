VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: help install run debug clean lint lint-strict build

help:
	@echo "Comandos disponibles:"
	@echo "  make help        - Muestra este mensaje de ayuda"
	@echo "  make install     - Crea el entorno virtual e instala dependencias"
	@echo "  make run         - Ejecuta el generador de laberintos con config.txt"
	@echo "  make debug       - Ejecuta el script en modo depuración (pdb)"
	@echo "  make clean       - Elimina archivos temporales y cachés"
	@echo "  make lint        - Ejecuta flake8 y mypy con configuración estándar"
	@echo "  make lint-strict - Ejecuta flake8 y mypy en modo estricto"
	@echo "  make build       - Construye el paquete distribuible (whl/tar.gz)"

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build
	$(PIP) install mlx-2.2-py3-none-any.whl

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__
	rm -rf build/ dist/ *.egg-info/

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy --strict .

build:
	$(PYTHON) -m build
