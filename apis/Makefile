# Makefile
# Variables
PROJECT_NAME=robin
PYTHON_EXEC=poetry run python

# ---------------------------
# 🧪 Tests
# ---------------------------

test:
	$(PYTHON_EXEC) -m pytest

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
# 📦 Packaging / install
# ---------------------------

install:
	poetry install

update:
	poetry update

lock:
	poetry lock
