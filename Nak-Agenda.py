

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput, Select
import json
from datetime import datetime, timedelta


DISCORD_TOKEN = "Votre TOKEN" 
CHANNEL_ID = 1317552426592768010 
CHECK_INTERVAL = 60 
DEVOIRS_FILE = "devoirs.json"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def load_devoirs():
    try:
        with open(DEVOIRS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_devoirs(liste_devoirs):
    with open(DEVOIRS_FILE, "w") as file:
        json.dump(liste_devoirs, file, indent=4)

liste_devoirs = load_devoirs()


class AddDevoirModal(Modal):
    def __init__(self):
        super().__init__(title="Ajouter un nouveau devoir 📝")
        self.nom = TextInput(label="📘 Nom du devoir", placeholder="Exemple : Maths", style=discord.TextStyle.short)
        self.deadline = TextInput(label="⏰ Date limite (jj/mm/aaaa)", placeholder="Exemple : 15/12/2024", style=discord.TextStyle.short)
        self.pdf = TextInput(label="📎 Lien PDF (optionnel)", placeholder="Exemple : https://example.com/devoir.pdf", required=False)
        self.add_item(self.nom)
        self.add_item(self.deadline)
        self.add_item(self.pdf)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            deadline = datetime.strptime(self.deadline.value, "%d/%m/%Y").date()
            devoir = {
                "nom": self.nom.value.strip(),
                "deadline": deadline.isoformat(),
                "pdf": self.pdf.value.strip() if self.pdf.value else None,
            }
            liste_devoirs.append(devoir)
            save_devoirs(liste_devoirs)

            embed = discord.Embed(
                title="📓 Nouveau devoir ajouté",
                description=f"**Nom :** {self.nom.value}\n**Deadline :** {deadline.strftime('%d/%m/%Y')}",
                color=discord.Color.green()
            )
            if self.pdf.value:
                embed.add_field(name="📎 Fichier PDF", value=f"[Lien PDF]({self.pdf.value})", inline=False)
            embed.set_footer(text="Bot Devoirs | Par Corsyn Ryan", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Erreur",
                    description="Format de date invalide. Utilisez `jj/mm/aaaa`.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )


class DevoirsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ajouter un devoir", style=discord.ButtonStyle.green, emoji="📝")
    async def add_devoir(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AddDevoirModal())

    @discord.ui.button(label="Liste des devoirs", style=discord.ButtonStyle.blurple, emoji="📋")
    async def list_devoirs(self, interaction: discord.Interaction, button: Button):
        if not liste_devoirs:
            embed = discord.Embed(
                title="📜 Aucun devoir enregistré",
                description="Ajoutez un devoir avec le bouton **Ajouter un devoir**.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        devoirs_tries = sorted(liste_devoirs, key=lambda x: x["deadline"])
        embed = discord.Embed(
            title="📜 Liste des devoirs à venir",
            color=discord.Color.blurple()
        )
        for i, devoir in enumerate(devoirs_tries, start=1):
            deadline = datetime.fromisoformat(devoir["deadline"]).date()
            description = f"📅 {deadline.strftime('%d/%m/%Y')}"
            if devoir["pdf"]:
                description += f"\n📎 [Lien PDF]({devoir['pdf']})"
            embed.add_field(
                name=f"{i}. {devoir['nom']}",
                value=description,
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Supprimer un devoir", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def delete_devoir(self, interaction: discord.Interaction, button: Button):
        if not liste_devoirs:
            embed = discord.Embed(
                title="❌ Aucun devoir à supprimer",
                description="Ajoutez un devoir avec le bouton **Ajouter un devoir**.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        options = [
            discord.SelectOption(
                label=f"{i + 1}. {devoir['nom']}",
                value=str(i),
                description=f"Deadline : {datetime.fromisoformat(devoir['deadline']).strftime('%d/%m/%Y')}"
            )
            for i, devoir in enumerate(liste_devoirs)
        ]

        select = Select(placeholder="Choisissez un devoir à supprimer", options=options)

        async def select_callback(interaction_select: discord.Interaction):
            index = int(select.values[0])
            supprime = liste_devoirs.pop(index)
            save_devoirs(liste_devoirs)
            embed = discord.Embed(
                title="🗑️ Devoir supprimé",
                description=f"**Nom :** {supprime['nom']}",
                color=discord.Color.red()
            )
            await interaction_select.response.send_message(embed=embed, ephemeral=True)

        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("🗑️ Sélectionnez un devoir à supprimer :", view=view, ephemeral=True)


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Clear le canal
        async for message in channel.history(limit=None):
            await message.delete()

        embed = discord.Embed(
            title="🎓 Menu principal des devoirs",
            description=(
                "Bienvenue dans le **menu principal des devoirs** !\n"
                "\n"
                "📝 **Ajouter un devoir** : Cliquez pour créer un nouveau devoir.\n"
                "📋 **Voir la liste des devoirs** : Consultez vos devoirs à venir.\n"
                "🗑️ **Supprimer un devoir** : Retirez un devoir déjà ajouté.\n"
                "\n"
                "📅 Planifiez vos tâches et restez organisé !"
            ),
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3050/3050525.png")
        embed.set_footer(text="Bot Devoirs | Par Corsyn Ryan")
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


bot.run(DISCORD_TOKEN)
