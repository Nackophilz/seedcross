#!/bin/sh

# On s'assure d'être dans le bon dossier
cd /app

# 1. Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --noinput

# 2. Collecter les fichiers statiques
# python manage.py collectstatic --noinput

# 3. Lancer les tâches de fond
echo "Lancement des tâches de fond..."
python manage.py process_tasks &

# 4. Lancer le serveur
echo "Démarrage du serveur..."
python manage.py runserver 0.0.0.0:8019