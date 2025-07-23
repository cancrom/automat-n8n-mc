import os
import sys
import subprocess
import json
import csv
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.utils import secure_filename

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'une-cle-secrete-tres-complexe-pour-la-securite'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Gère la page d'accueil et la soumission du formulaire de mise à jour manuelle. """
    manual_result = None
    if request.method == 'POST':
        sku = request.form.get('sku')
        quantity = request.form.get('quantity')

        if not sku or not quantity:
            flash("Le SKU et la quantité sont requis pour la mise à jour manuelle.", "error")
        else:
            # Exécute le script pour une seule mise à jour
            result_json = run_update_script(sku, quantity)
            manual_result = json.loads(result_json)

    return render_template('index.html', manual_result=manual_result)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """ Gère le téléversement du fichier CSV et redirige vers la page de mappage. """
    if 'csv_file' not in request.files:
        flash('Aucun fichier sélectionné.', 'error')
        return redirect(url_for('index'))

    file = request.files['csv_file']
    if file.filename == '':
        flash('Aucun fichier sélectionné.', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Lire les en-têtes pour le mappage
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)

        return render_template('mapping.html', filename=filename, headers=headers)

    flash('Type de fichier non autorisé. Veuillez utiliser un fichier CSV.', 'error')
    return redirect(url_for('index'))

@app.route('/process_batch', methods=['POST'])
def process_batch():
    """ Traite le fichier CSV en utilisant le mappage fourni par l'utilisateur. """
    filename = request.form.get('filename')
    sku_col = request.form.get('sku_col')
    quantity_col = request.form.get('quantity_col')

    if not all([filename, sku_col, quantity_col]):
        flash("Informations de mappage manquantes.", "error")
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    results = []

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row.get(sku_col)
            quantity = row.get(quantity_col)

            if sku and quantity:
                result_json = run_update_script(sku, quantity)
                results.append(json.loads(result_json))

    # Stocker les résultats dans la session pour l'export
    session['last_results'] = results

    return render_template('results.html', results=results)

@app.route('/export_results')
def export_results():
    """ Exporte les derniers résultats de traitement en tant que fichier CSV. """
    results = session.get('last_results', [])
    if not results:
        flash("Aucun résultat à exporter.", "info")
        return redirect(url_for('index'))

    # Utilisation de io.StringIO pour créer un fichier en mémoire
    import io
    output = io.StringIO()
    writer = csv.writer(output)

    # Écrire les en-têtes
    writer.writerow(['SKU', 'Quantity', 'Status', 'Message', 'Screenshot'])

    # Écrire les données
    for result in results:
        writer.writerow([
            result.get('sku'),
            result.get('quantity'),
            result.get('status'),
            result.get('message'),
            result.get('screenshot')
        ])

    output.seek(0)

    from flask import Response
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=export_results.csv"}
    )

# --- Fonctions auxiliaires ---

def run_update_script(sku, quantity):
    """ Lance le script update_stock.py et retourne sa sortie JSON. """
    script_path = os.path.join(os.path.dirname(__file__), 'update_stock.py')
    command = [
        sys.executable,
        script_path,
        '--sku', str(sku),
        '--quantity', str(quantity)
    ]

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        # Si le script lui-même échoue (return code non-zéro), sa sortie d'erreur est capturée
        return json.dumps({
            "sku": sku, "quantity": quantity, "status": "error",
            "message": f"Erreur d'exécution du script: {e.stderr}", "screenshot": ""
        })
    except Exception as e:
        # Pour les autres erreurs (ex: script non trouvé)
        return json.dumps({
            "sku": sku, "quantity": quantity, "status": "error",
            "message": f"Erreur système: {e}", "screenshot": ""
        })

# --- Point d'entrée ---

if __name__ == '__main__':
    # Créer les répertoires nécessaires s'ils n'existent pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5001)
