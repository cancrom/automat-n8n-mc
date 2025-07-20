# Projet d'Automatisation MC App avec N8n et Puppeteer

Ce projet fournit une solution d'automatisation pour gérer les mises à jour de stock sur la plateforme MC App (web.mc.app) en utilisant N8n et le nœud `n8n-nodes-puppeteer`.

## Prérequis

- Docker et Docker Compose
- Un compte MC App Gérant
- Les identifiants de votre serveur SMTP (pour l'envoi d'e-mails)
- Une clé API de votre choix pour sécuriser le webhook

## Installation

1. Clonez ce projet :
   ```bash
   git clone <URL_DU_PROJET>
   ```
2. Accédez au répertoire du projet :
   ```bash
   cd <NOM_DU_PROJET>
   ```
3. Créez un fichier `.env` à partir de l'exemple et remplissez les valeurs :
   ```bash
   cp .env.example .env
   ```
4. Lancez les conteneurs Docker :
   ```bash
   docker-compose up -d
   ```
5. **Installez le nœud Puppeteer :**
   - Ouvrez l'interface N8n à `http://localhost:5678`.
   - Allez dans `Settings > Community Nodes`.
   - Cliquez sur `Install a new community node`.
   - Dans le champ "npm Package Name", entrez `n8n-nodes-puppeteer`.
   - Cochez la case "I understand the risks...".
   - Cliquez sur `Install`.
   - Redémarrez N8n pour appliquer les changements : `docker-compose restart n8n`.

6. Importez les workflows du répertoire `n8n/workflows` dans votre instance N8n.

## Configuration

- **`.env`** : Configurez les variables d'environnement dans ce fichier, notamment `N8N_HOST`, `ENCRYPTION_KEY`, `API_TOKEN`, et vos identifiants SMTP.
- **Workflows N8n** : Activez les workflows après les avoir importés.

## Utilisation

### Authentification

Le workflow `authentication_workflow.json` gère l'authentification. Lors de la première exécution, il vous enverra un QR code par e-mail. Scannez-le avec l'application MC Gérant pour vous connecter. La session sera ensuite automatiquement renouvelée.

### Mise à Jour en Masse

1. Ouvrez le fichier `index.html` dans votre navigateur.
2. Sélectionnez le fichier Excel contenant les mises à jour de stock.
3. Entrez votre clé API.
4. Cliquez sur "Lancer la mise à jour".

## Maintenance

- **Sélecteurs CSS/XPath** : Si l'interface de MC App change, vous devrez peut-être mettre à jour les sélecteurs dans les nœuds "Puppeteer" des workflows.
- **Logs** : Les logs des exécutions de workflows sont disponibles dans l'interface de N8n.

## Résolution des problèmes

- **Session Expirée** : Relancez manuellement le workflow d'authentification.
- **Blocage IP** : Configurez un proxy dans les nœuds "Puppeteer".
- **Fichier Corrompu** : Assurez-vous que votre fichier Excel a les colonnes `productSku` et `newStock`.
