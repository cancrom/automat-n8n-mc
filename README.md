# Panneau de Contrôle pour Automatisation Web

Ce projet est une application web complète conçue pour automatiser des tâches de mise à jour de stock sur une application web cible. Il dispose d'une interface de contrôle conviviale construite avec Flask et d'un puissant bot d'automatisation basé sur Playwright.

![Capture d'écran de l'interface](https://i.imgur.com/your-screenshot.png) <!-- Image à remplacer par une vraie capture d'écran -->

## Fonctionnalités Principales

- **Automatisation Robuste** : Utilise Playwright pour une interaction fiable avec les applications web modernes.
- **Authentification Persistante** : Contourne la nécessité de scanner un code QR à chaque exécution grâce à un système de sauvegarde de session.
- **Interface Web Intuitive** : Un panneau de contrôle basé sur Flask pour gérer toutes les opérations sans toucher au code.
- **Double Mode de Mise à Jour** :
  - **Manuel** : Pour des mises à jour rapides et uniques.
  - **En Masse** : Via le téléversement de fichiers CSV pour traiter des centaines de produits à la fois.
- **Mappage de Colonnes Flexible** : Permet aux utilisateurs d'utiliser leurs propres fichiers CSV en faisant correspondre leurs colonnes aux champs requis par le système.
- **Rapports Visuels** : Affiche un tableau de bord détaillé des résultats de chaque traitement en masse, avec un statut de succès/échec et des liens vers des captures d'écran.
- **Export des Résultats** : Permet de télécharger un rapport complet des opérations au format CSV.

## Architecture

Le système est articulé autour de trois piliers technologiques :

1.  **Noyau d'Automatisation (Playwright)** : Un bot qui simule les interactions humaines.
2.  **Interface de Contrôle (Flask)** : Une application web qui sert de panneau de contrôle.
3.  **Communication Découplée (Subprocess)** : L'interface et le bot communiquent via des appels en ligne de commande, garantissant modularité et stabilité.

## Installation

Suivez ces étapes pour mettre en place et lancer le projet sur votre machine locale.

### Prérequis

- Python 3.8+
- `pip` (gestionnaire de paquets Python)

### 1. Cloner le Dépôt

```bash
git clone <url-du-depot>
cd <nom-du-dossier>
2. Installer les Dépendances
Installez les bibliothèques Python nécessaires et téléchargez les navigateurs pour Playwright.

pip install -r requirements.txt
playwright install
Guide d'Utilisation
Étape 1 : Authentification Initiale (à faire une seule fois)
Ce processus va créer un fichier de session pour éviter de vous reconnecter à chaque fois.

Exécutez le script auth.py :
python auth.py
Une fenêtre de navigateur s'ouvrira. Connectez-vous sur le site web en scannant le code QR.
Une fois connecté, retournez au terminal et appuyez sur la touche Entrée.
Un fichier playwright/.auth/state.json sera créé. Il contient votre session et doit rester privé.

Étape 2 : Lancer l'Application
Démarrez le serveur web Flask :

python app.py
Le serveur sera accessible à l'adresse http://127.0.0.1:5001.

Étape 3 : Utiliser le Panneau de Contrôle
Ouvrez votre navigateur et allez sur http://127.0.0.1:5001.
Choisissez votre mode de mise à jour :
Mise à Jour Manuelle : Remplissez les champs SKU et Quantité, puis cliquez sur "Lancer la Mise à Jour".
Mise à Jour par Fichier (CSV) :
Allez dans l'onglet correspondant.
Téléversez votre fichier CSV.
Sur l'écran suivant, mappez les colonnes de votre fichier aux champs "SKU" et "Quantité".
Cliquez sur "Lancer le Traitement".
Consultez les résultats sur la page de rapport.
Exportez les résultats en CSV si nécessaire.
Pistes d'Amélioration
Planification des Tâches : Intégrer un scheduler (ex: APScheduler) pour lancer des mises à jour automatiques.
Notifications : Envoyer des rapports par email ou Slack à la fin des traitements.
Historique des Tâches : Sauvegarder les résultats dans une base de données (SQLite) pour consultation ultérieure.
Dockerisation : Empaqueter l'application dans une image Docker pour un déploiement simplifié.
