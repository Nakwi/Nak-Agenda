import discord
from discord.ext import tasks
from config import CHANNEL_ID, CHECK_INTERVAL
from ui import DevoirsView, liste_devoirs
from data_manager import save_devoirs
from datetime import datetime

def setup_events(bot):
    @bot.event
    async def on_ready():
        print(f"Bot connecté en tant que {bot.user}")
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            async for message in channel.history(limit=None):
                await message.delete()
            embed = discord.Embed(
                title="🎓 Menu principal des devoirs",
                description="📝 **Ajouter un devoir**\n📋 **Voir la liste**\n🗑️ **Supprimer un devoir**",
                color=discord.Color.blurple()
            )
            view = DevoirsView()
            await channel.send(embed=embed, view=view)
        else:
            print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_rappels():
        maintenant = datetime.now().date()
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")
            return

        for devoir in liste_devoirs[:]:
            deadline = datetime.fromisoformat(devoir["deadline"]).date()
            if maintenant == deadline:
                embed = discord.Embed(
                    title="🔔 Rappel de devoir",
                    description=f"**{devoir['nom']}** est prévu pour aujourd'hui !",
                    color=discord.Color.orange()
                )
                await channel.send(embed=embed)
                liste_devoirs.remove(devoir)
                save_devoirs(liste_devoirs)
