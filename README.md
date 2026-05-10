# SRTF Scheduling Algorithm — SE-LIU-2026

## Description
Implémentation de l'algorithme d'ordonnancement *SRTF (Shortest Remaining Time First)* en Python avec stockage des résultats dans une base de données *MySQL, le tout conteneurisé avec **Docker* sur *Debian*.


## Structure du projet

srtf-project/
├── srtf.py              # Algorithme SRTF en Python
├── Dockerfile           # Image Debian + Python
├── docker-compose.yml   # Orchestration Python + MySQL
├── requirements.txt     # Dépendances Python
└── README.md            # Documentation


## Prérequis
- [Docker](https://www.docker.com/) installé sur votre machine
- [Git](https://git-scm.com/)

## Lancement du projet

bash
# 1. Cloner le dépôt
git clone https://github.com/VOTRE_NOM/srtf-project.git
cd s…