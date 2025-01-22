import discord
from discord.ext import commands
from config import DISCORD_TOKEN, intents
from ui import DevoirsView
from events import setup_events

bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les événements
setup_events(bot)

# Lancer le bot
bot.run(DISCORD_TOKEN)
