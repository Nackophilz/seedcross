FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Compilation des fichiers de traduction
RUN python manage.py compilemessages

# Création du dossier db et permission d'exécution pour le script
RUN mkdir -p db && chmod +x start.sh

# Exposition du port utilisé dans start.sh
EXPOSE 8019

# Volume pour la base de données
VOLUME ["/app/db"]

# Commande de démarrage
CMD ["./start.sh"]