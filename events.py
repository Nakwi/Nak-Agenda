import discord
from discord.ext import tasks
from config import CHANNEL_ID, CHECK_INTERVAL
from ui import DevoirsView
from data_manager import load_devoirs, remove_devoir
from datetime import datetime

# Déclaration globale de `bot`
bot = None

def setup_events(bot_instance):
    """Configure les événements et attache le bot."""
    global bot
    bot = bot_instance  # Stocke l'instance du bot

    @bot.event
    async def on_ready():
        """Événement déclenché lorsque le bot est prêt."""
        print(f"✅ Bot connecté en tant que {bot.user}")

        # Récupérer le channel
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"⚠️ Erreur : Canal avec ID {CHANNEL_ID} introuvable. Vérifie les permissions du bot.")
            return

        # Supprimer les anciens messages dans le canal
        print("🗑️ Suppression des anciens messages du canal...")
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
                "🎓 **Astuce :** N'oubliez pas de fixer une deadline pour vos devoirs !"
            ),
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3050/3050525.png")
        embed.set_footer(text="Bot Devoirs | Par Corsyn Ryan")
        view = DevoirsView()  # Crée la vue pour les interactions

        await channel.send(embed=embed, view=view)
        print("✅ Menu principal envoyé !")

        # Vérifier si la boucle de rappels est bien démarrée
        if not check_rappels.is_running():
            print("🔄 Lancement de la boucle de rappels...")
            check_rappels.start()
        else:
            print("✅ La boucle de rappels est déjà en cours.")

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_rappels():
    """Vérifie si un rappel doit être envoyé."""
    print("🔍 Vérification des rappels en cours...")

    if bot is None:
        print("⚠️ Erreur : `bot` est None dans `check_rappels()`. Assurez-vous que `setup_events()` est bien appelé avec le bot.")
        return

    maintenant = datetime.now()
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print(f"⚠️ Erreur : Canal avec ID {CHANNEL_ID} introuvable. Impossible d'envoyer des rappels.")
        return

    devoirs = load_devoirs()

    if not devoirs:
        print("ℹ️ Aucun devoir enregistré. Rien à rappeler.")
        return

    print(f"📌 Liste des rappels en attente ({len(devoirs)} devoirs) :")
    for devoir in devoirs:
        print(f"📚 {devoir['nom']} - Rappel prévu à : {devoir['rappel_at']}, Deadline : {devoir['deadline']}")

        # Vérification du format de la deadline
        if isinstance(devoir["deadline"], str):
            try:
                deadline = datetime.strptime(devoir["deadline"], "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠️ Erreur de format pour la deadline de {devoir['nom']}: {devoir['deadline']}")
                continue
        else:
            deadline = devoir["deadline"]

        # Vérification du format du rappel
        rappel_at = None
        if devoir["rappel_at"]:
            if isinstance(devoir["rappel_at"], str):
                try:
                    rappel_at = datetime.strptime(devoir["rappel_at"], "%Y-%m-%dT%H:%M")
                except ValueError:
                    print(f"⚠️ Erreur de format pour le rappel de {devoir['nom']}: {devoir['rappel_at']}")
                    continue
            else:
                rappel_at = devoir["rappel_at"]

        # Vérification si le rappel doit être envoyé
        if rappel_at and maintenant >= rappel_at:
            embed = discord.Embed(
                title="🔔 Rappel de devoir",
                description=f"📚 **{devoir['nom']}**\n📅 **Deadline :** {deadline.strftime('%d/%m/%Y')}",
                color=discord.Color.orange()
            )
            if devoir["description"]:
                embed.add_field(name="🖊️ Description", value=devoir["description"], inline=False)
            if devoir["pdf"]:
                embed.add_field(name="📎 Lien PDF", value=f"[Lien]({devoir['pdf']})", inline=False)

            await channel.send(embed=embed)
            print(f"✅ 📢 Rappel envoyé pour : {devoir['nom']}")

            # Si la deadline est passée, supprimer le devoir
            if maintenant.date() >= deadline:
                remove_devoir(devoir["id"])
                print(f"✅ ❌ Devoir supprimé après rappel : {devoir['nom']}")

