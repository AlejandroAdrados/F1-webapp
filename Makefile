# Variables
APP_NAME=mi_app
DOCKER_IMAGE=$(APP_NAME):latest
DOCKER_FILE=Dockerfile
PYTHON=python3
PIP=pip
VENV_DIR=./venv
PORT=8050

# Detectar sistema operativo para configurar las rutas del entorno virtual
ifeq ($(OS),Windows_NT)
    VENV_PYTHON=$(VENV_DIR)/Scripts/python
    VENV_PIP=$(VENV_DIR)/Scripts/pip
else
    VENV_PYTHON=$(VENV_DIR)/bin/python
    VENV_PIP=$(VENV_DIR)/bin/pip
endif

# Directorios y archivos
SRC_DIR=app
TEST_DIR=tests
REQ_FILE=requirements/requirements.txt
REQ_FILE_TEST=requirements/requirements-test.txt

.PHONY: all run test docker-build docker-run install-requirements create-venv clean

# Crear un entorno virtual
create-venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Entorno virtual creado en $(VENV_DIR)"; \
	else \
		echo "El entorno virtual ya existe en $(VENV_DIR)"; \
	fi

# Instalar requisitos usando el entorno virtual
install-requirements: create-venv
	$(VENV_PIP) install -r $(REQ_FILE)

# Instalar requisitos de testing usando el entorno virtual
install-requirements-test: install-requirements
	$(VENV_PIP) install -r $(REQ_FILE_TEST)

# Ejecutar el programa Python localmente
run: install-requirements
	$(VENV_PYTHON) run.py

# Ejecutar pruebas
test: install-requirements-test
	$(VENV_PYTHON) -m pytest $(TEST_DIR)

# Construir la imagen Docker
docker-build:
	docker build -t $(DOCKER_IMAGE) -f $(DOCKER_FILE) .

# Ejecutar la imagen Docker
docker-run:
	docker run --rm -it -p $(PORT):8050 $(DOCKER_IMAGE)

# Limpiar archivos generados
clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf $(VENV_DIR)
	docker image prune -f
	@echo "Archivos temporales y datos limpiados."
