# auth.py
import asyncio
from playwright.async_api import async_playwright
import os
import json

# Le chemin vers le fichier où l'état de la session sera stocké.
# Il est recommandé de placer ce fichier dans un répertoire .auth et d'ajouter ce répertoire à .gitignore. [8]
AUTH_FILE_PATH = "playwright/.auth/state.json"

async def run():
    async with async_playwright() as p:
        # Lancement du navigateur en mode "headed" (avec interface graphique) pour permettre l'interaction manuelle.
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Ouverture de la page de connexion...")
        await page.goto("https://web.mc.app/#/login")

        # Pause du script pour permettre la connexion manuelle.
        # L'utilisateur doit scanner le code QR dans la fenêtre du navigateur qui s'est ouverte.
        print("="*50)
        print("ACTION REQUISE : Veuillez scanner le code QR dans la fenêtre du navigateur.")
        print("Une fois connecté, appuyez sur la touche 'Entrée' dans cette console pour continuer.")
        print("="*50)
        input() # Le script attend ici une action de l'utilisateur.

        # Une fois que l'utilisateur a appuyé sur Entrée, on suppose qu'il est connecté.
        # Le script capture alors l'état de stockage du contexte.
        print("Sauvegarde de l'état d'authentification...")

        # Création du répertoire si il n'existe pas.
        os.makedirs(os.path.dirname(AUTH_FILE_PATH), exist_ok=True)

        # Écriture de l'état dans un fichier JSON.
        storage_state = await context.storage_state()
        with open(AUTH_FILE_PATH, 'w') as f:
            json.dump(storage_state, f)

        print(f"État d'authentification sauvegardé avec succès dans '{AUTH_FILE_PATH}'")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
