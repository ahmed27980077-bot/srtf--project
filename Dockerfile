# Utiliser Debian comme système de base
FROM debian:latest

# Installer Python et pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

# Répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY srtf.py .
COPY requirements.txt .

# Installer la bibliothèque MySQL
RUN pip3 install -r requirements.txt --break-system-packages

# Lancer le programme
CMD ["python3", "srtf.py"]