import os
import discord
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer les variables d'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))  # Convertir en int
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # Valeur par défaut 60s

# Vérifier si les variables sont bien chargées
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN est introuvable. Vérifie ton fichier .env.")

if CHANNEL_ID == 0:
    raise ValueError("❌ DISCORD_CHANNEL_ID est introuvable ou incorrect.")

# Définir les intents pour le bot Discord
intents = discord.Intents.default()
intents.message_content = True
