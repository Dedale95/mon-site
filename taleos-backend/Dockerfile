# Dockerfile pour Render avec Playwright
FROM python:3.11-slim

# Installer les dépendances système de base nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY requirements.txt .
COPY app.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Installer Playwright et Chromium
# playwright install-deps installe automatiquement toutes les dépendances système nécessaires
RUN playwright install chromium && \
    playwright install-deps chromium

# Exposer le port (Render définit $PORT)
ENV PORT=10000
EXPOSE $PORT

# Commande de démarrage
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
