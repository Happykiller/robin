# Étape 1 : base image
FROM python:3.11-slim

# Étape 2 : variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

# Étape 3 : install utilitaires
# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Étape 5 : créer le dossier app
WORKDIR /app

# Étape 6 : copier les fichiers
COPY pyproject.toml poetry.lock* /app/

# Étape 7 : installer dépendances
RUN poetry install --no-root --only main

# Étape 8 : copier le code
COPY . /app/

# Étape 9 : exposer le port
EXPOSE 8000

# Étape 10 : commande de lancement
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
