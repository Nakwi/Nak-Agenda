import discord

DISCORD_TOKEN = ""
CHANNEL_ID = 1317552426592768010
CHECK_INTERVAL = 60  # Intervalle pour les rappels en secondes
intents = discord.Intents.default()
intents.message_content = True
