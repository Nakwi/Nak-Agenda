from flask import Flask, render_template, request, redirect
from data_manager import save_devoirs, load_devoirs, remove_devoir
from datetime import datetime
from threading import Thread
import discord
from discord.ext import commands
from events import setup_events
from config import CHANNEL_ID, CHECK_INTERVAL
from config import DISCORD_TOKEN, intents


# Configuration de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
setup_events(bot)

# Configuration de Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Affiche la liste des devoirs."""
    print("[DEBUG] Page principale chargée.")
    devoirs = load_devoirs()
    return render_template('index.html', devoirs=devoirs)

@app.route('/add', methods=['POST'])
def add_devoir():
    """Ajoute un nouveau devoir."""
    nom = request.form['nom']
    deadline = request.form['deadline']
    rappel_at = request.form['rappel_at']
    description = request.form.get('description', None)
    pdf = None

    if 'pdf' in request.files:
        pdf_file = request.files['pdf']
        if pdf_file.filename != '':
            pdf_path = f"uploads/{pdf_file.filename}"
            pdf_file.save(pdf_path)
            pdf = pdf_path

    deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
    rappel_datetime = datetime.strptime(rappel_at, '%Y-%m-%dT%H:%M')

    save_devoirs(
        nom=nom,
        deadline=deadline_date,
        rappel_at=rappel_datetime,
        description=description,
        pdf=pdf
    )

    print(f"[DEBUG] Devoir ajouté : {nom}")
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_devoir():
    """Supprime un devoir."""
    print("[DEBUG] Route /delete appelée.")
    devoir_id = request.form.get('devoir_id')  # Récupère l'ID du devoir
    if devoir_id:
        remove_devoir(int(devoir_id))  # Supprime le devoir
        print(f"[DEBUG] Devoir supprimé : {devoir_id}")
    else:
        print("[ERROR] Aucun ID de devoir reçu pour suppression.")
    return redirect('/')

def run_flask():
    """Lance le serveur Flask."""
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_discord():
    """Lance le bot Discord."""
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    # Lancer Flask et Discord en parallèle
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    run_discord()
