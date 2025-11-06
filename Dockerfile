FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Définir la timezone (pour le scheduler à 18h)
ENV TZ=Europe/Paris

# Commande pour lancer le bot
CMD ["python", "app.py"]
