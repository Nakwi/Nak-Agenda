# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput
import json
from datetime import datetime, timedelta

DISCORD_TOKEN = "DISCORD_TOKEN"
CHANNEL_ID = ID_DU_CHANNEL
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
        super().__init__(title="Ajouter un devoir")
        self.nom = TextInput(label="Nom du devoir", placeholder="Exemple : Maths")
        self.deadline = TextInput(label="Date (jj/mm/aa)", placeholder="Exemple : 15/12/24")
        self.add_item(self.nom)
        self.add_item(self.deadline)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            deadline = datetime.strptime(self.deadline.value, "%d/%m/%y").date()
            liste_devoirs.append({"nom": self.nom.value, "deadline": deadline.isoformat()})
            save_devoirs(liste_devoirs)
            embed = discord.Embed(
                title="\ud83d\udcd3 Nouveau devoir ajouté",
                description=f"**Nom :** {self.nom.value}\n**Deadline :** {deadline.strftime('%d/%m/%Y')}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            embed = discord.Embed(
                title="\u274c Erreur",
                description="Format de date invalide. Utilise `jj/mm/aa`.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

class DevoirsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ajouter un devoir", style=discord.ButtonStyle.green)
    async def add_devoir(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AddDevoirModal())

    @discord.ui.button(label="Liste des devoirs", style=discord.ButtonStyle.blurple)
    async def list_devoirs(self, interaction: discord.Interaction, button: Button):
        if not liste_devoirs:
            embed = discord.Embed(
                title="\ud83d\udcdc Aucun devoir enregistré",
                description="Ajoute-en un avec le bouton **Ajouter un devoir**.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        devoirs_tries = sorted(liste_devoirs, key=lambda x: x["deadline"])
        embed = discord.Embed(
            title="\ud83d\udcdc Liste des devoirs à venir",
            color=discord.Color.blurple()
        )
        for i, devoir in enumerate(devoirs_tries, start=1):
            deadline = datetime.fromisoformat(devoir["deadline"]).date()
            embed.add_field(
                name=f"{i}. {devoir['nom']}",
                value=f"\ud83d\udcc5 {deadline.strftime('%d/%m/%Y')}",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Supprimer un devoir", style=discord.ButtonStyle.danger)
    async def delete_devoir(self, interaction: discord.Interaction, button: Button):
        if not liste_devoirs:
            embed = discord.Embed(
                title="\u274c Aucun devoir à supprimer",
                description="Ajoute-en un avec le bouton **Ajouter un devoir**.",
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

        select = discord.ui.Select(placeholder="Choisissez un devoir à supprimer", options=options)

        async def select_callback(interaction_select: discord.Interaction):
            index = int(select.values[0])
            supprime = liste_devoirs.pop(index)
            save_devoirs(liste_devoirs)
            embed = discord.Embed(
                title="\ud83d\uddd1\ufe0f Devoir supprimé",
                description=f"**Nom :** {supprime['nom']}",
                color=discord.Color.red()
            )
            await interaction_select.response.send_message(embed=embed, ephemeral=True)

        select.callback = select_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("\ud83d\uddd1\ufe0f Sélectionnez un devoir à supprimer :", view=view, ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="\ud83c\udf93 Menu des devoirs",
            description="Utilisez les boutons ci-dessous pour gérer vos devoirs.",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Bot Devoirs | Par Corsyn Ryan")
        view = DevoirsView()
        await channel.send(embed=embed, view=view)
    else:
        print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")

    check_rappels.start()  

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_rappels():
    maintenant = datetime.now().date()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Erreur : Canal avec ID {CHANNEL_ID} introuvable.")
        return

    for devoir in liste_devoirs[:]:
        try:
            deadline = datetime.fromisoformat(devoir["deadline"]).date()
            print(f"Vérification du devoir : {devoir['nom']}, deadline : {deadline}, aujourd'hui : {maintenant}")
            if maintenant == deadline:
                embed = discord.Embed(
                    title="\ud83d\udd14 Rappel de devoir",
                    description=f"**{devoir['nom']}** est prévu pour aujourd'hui !",
                    color=discord.Color.orange()
                )
                await channel.send(embed=embed)
                liste_devoirs.remove(devoir)
                save_devoirs(liste_devoirs)
        except Exception as e:
            print(f"Erreur lors du traitement du devoir {devoir}: {e}")

bot.run(DISCORD_TOKEN)
