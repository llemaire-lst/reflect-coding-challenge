# Utilise une image Python officielle comme base
FROM python:3.10-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers requirements.txt (ou pyproject.toml) pour l'installation des dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Définit la commande de lancement (à adapter)
CMD ["python", "rest_api_lucca_pipeline.py"]
