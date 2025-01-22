import discord

DISCORD_TOKEN = "TOKEN"
CHANNEL_ID = 1317552426592768010
CHECK_INTERVAL = 60
DEVOIRS_FILE = "devoirs.json"

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
