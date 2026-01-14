# Dockerfile pour Render avec Playwright
# Utiliser Debian Bookworm (mieux supporté par Playwright que Trixie)
FROM python:3.11-slim-bookworm

# Installer les dépendances système nécessaires pour Playwright/Chromium
# Basé sur la documentation officielle de Playwright pour Debian
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    fonts-unifont \
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
# Les dépendances système sont déjà installées manuellement ci-dessus
RUN playwright install chromium

# Exposer le port (Render définit $PORT)
ENV PORT=10000
EXPOSE $PORT

# Commande de démarrage
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
