import discord
from discord.ext import tasks
from config import CHANNEL_ID, CHECK_INTERVAL
from ui import DevoirsView
from data_manager import load_devoirs, remove_devoir
from datetime import datetime

def setup_events(bot):
    @bot.event
    async def on_ready():
        """Événement déclenché lorsque le bot est prêt."""
        print(f"Bot connecté en tant que {bot.user}")
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            # Effacer les anciens messages dans le canal
            async for message in channel.history(limit=None):
                await message.delete()

            # Créer et envoyer le menu principal
            embed = discord.Embed(
                title="📚 Bienvenue dans votre gestionnaire de devoirs",
                description=(
                    "Organisez vos devoirs et recevez des rappels grâce à ce bot. Voici ce que vous pouvez faire :\n\n"
                    "📝 **Ajouter un devoir** : Cliquez pour ajouter un nouveau devoir.\n"
                    "📋 **Voir la liste des devoirs** : Consultez les devoirs à venir.\n"
                    "🗑️ **Supprimer un devoir** : Retirez un devoir que vous ne voulez plus suivre.\n\n"
                    "🎓 **Astuce :** N'oubliez pas de fixer une deadline pour vos devoirs !"
                ),
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3050/3050525.png")
            embed.set_footer(text="Bot Devoirs | Par Corsyn Ryan")
            view = DevoirsView()  # Crée la vue pour les interactions
            await channel.send(embed=embed, view=view)
        else:
            print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_rappels():
        """Vérifie si un rappel doit être envoyé."""
        maintenant = datetime.now().date()
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")
            return

        devoirs = load_devoirs()
        for devoir in devoirs:
            deadline = datetime.fromisoformat(devoir["deadline"]).date()
            if maintenant == deadline:
                embed = discord.Embed(
                    title="🔔 Rappel de devoir",
                    description=f"**{devoir['nom']}** est prévu pour aujourd'hui !",
                    color=discord.Color.orange()
                )
                await channel.send(embed=embed)
                remove_devoir(devoir["id"])  # Supprime le devoir après le rappel
