# update_stock.py
import asyncio
from playwright.async_api import async_playwright, Playwright, Error
import os
import argparse
import json
import sys

AUTH_FILE_PATH = "playwright/.auth/state.json"

def get_args():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Bot de mise à jour de stock pour web.mc.app")
    parser.add_argument('--sku', required=True, help="Le SKU du produit à mettre à jour.")
    parser.add_argument('--quantity', required=True, type=int, help="La nouvelle quantité de stock.")
    return parser.parse_args()

async def run(sku: str, quantity: int) -> dict:
    """
    Exécute le bot de mise à jour de stock pour un seul produit et retourne un résultat structuré.
    """
    result = {
        "sku": sku,
        "quantity": quantity,
        "status": "error",
        "message": "",
        "screenshot": ""
    }

    if not os.path.exists(AUTH_FILE_PATH):
        result["message"] = f"Le fichier d'authentification '{AUTH_FILE_PATH}' n'a pas été trouvé. Veuillez exécuter 'python auth.py'."
        return result

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=AUTH_FILE_PATH)
            page = await context.new_page()

            await page.goto("https://web.mc.app/#/dashboard/inventory")

            # --- Logique d'automatisation réelle (à adapter avec les vrais sélecteurs) ---
            # Exemple de ce à quoi cela pourrait ressembler :
            # await page.get_by_label("Rechercher un produit").fill(sku)
            # await page.get_by_role("button", name="Rechercher").click()
            # await page.locator(".stock-input[data-sku='" + sku + "']").fill(str(quantity))
            # await page.get_by_role("button", name="Sauvegarder").click()
            # await page.wait_for_selector("text=Succès") # Attendre une confirmation

            # Pour la simulation, nous allons juste attendre un peu.
            await asyncio.sleep(2)

            # S'assurer que le répertoire static existe
            os.makedirs("static", exist_ok=True)
            screenshot_path = os.path.join("static", f"screenshot_{sku}.png")
            await page.screenshot(path=screenshot_path)

            await browser.close()

            result.update({
                "status": "success",
                "message": f"Mise à jour pour {sku} terminée avec succès.",
                "screenshot": screenshot_path
            })

    except Error as e:
        # Gère les erreurs spécifiques à Playwright (ex: TimeoutError)
        result["message"] = f"Une erreur Playwright est survenue : {e}"
    except Exception as e:
        # Gère toutes les autres erreurs
        result["message"] = f"Une erreur inattendue est survenue : {e}"

    return result

if __name__ == "__main__":
    # Ce bloc est exécuté lorsque le script est appelé directement
    args = get_args()

    # Exécute la fonction principale
    final_result = asyncio.run(run(sku=args.sku, quantity=args.quantity))

    # Imprime le résultat final en tant que chaîne JSON sur stdout
    # C'est ce que le processus parent (Flask) lira
    print(json.dumps(final_result))
