# Variables
PROJECT_NAME=product-api
SERVICE=apis

# ---------------------------
# 🐳 Docker
# ---------------------------

up:
	docker-compose up --build

down:
	docker-compose down

restart: down up

# ---------------------------
# 🧪 Tests (à compléter plus tard)
# ---------------------------

test:
	poetry run pytest

# ---------------------------
# 🔍 Linting
# ---------------------------

lint:
	poetry run flake8 apis

# ---------------------------
# 🧹 Nettoyage
# ---------------------------

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .mypy_cache .pytest_cache *.pyc *.pyo *.pyd .coverage htmlcov

# ---------------------------
# 🧰 Dev utils
# ---------------------------

shell:
	docker exec -it $$(docker ps -qf "name=${SERVICE}") /bin/bash

logs:
	docker-compose logs -f ${SERVICE}

# ---------------------------
# 📦 Packaging / install
# ---------------------------

install:
	poetry install

update:
	poetry update

lock:
	poetry lock
