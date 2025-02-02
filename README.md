# 📘 Gestionnaire de Devoirs – Documentation  

---

## 📝 Introduction  
Ce projet permet de gérer des devoirs de manière efficace via deux interfaces complémentaires :  

- **Un bot Discord** 🎮 : Ajoute, affiche et supprime des devoirs directement dans un serveur Discord avec une interface interactive (boutons et menus déroulants).  
- **Une interface graphique web** 🌐 : Basée sur Flask, elle offre une gestion visuelle moderne pour consulter et organiser ses tâches.  

L’objectif est de combiner la **flexibilité** de Discord avec une **interface web intuitive** accessible via un navigateur.

---

## ⚙️ Installation & Configuration  

### 📌 Prérequis  
Avant d’installer l’application, assurez-vous d’avoir les éléments suivants :  

- **Python 3.x**  
- **MySQL**  
- **Pip**  
- **Un serveur Discord** (pour tester le bot)  

### 📥 Installation des dépendances  
Clonez ce dépôt et installez les dépendances avec :  

```bash
git clone https://github.com/Nakwi/Nak-Agenda.git
cd Nak-Agenda
pip install -r requirements.txt
```

### ⚙️ Configuration de l’environnement  
Ajoutez un fichier `.env` à la racine du projet avec :  

```bash
DISCORD_TOKEN=ton_token_ici
DISCORD_CHANNEL_ID=123456789012345678
CHECK_INTERVAL=60
```

Remplacez `ton_token_ici` par votre token Discord et `123456789012345678` par l’ID du canal Discord où le bot interagira.

---

## 🏗️ Architecture du Projet  

Le projet est structuré ainsi :  

```
gestionnaire-devoirs/
│── main.py               # Point d’entrée principal du projet
│── ui.py                 # Interface utilisateur pour le bot Discord
│── events.py             # Gestion des événements asynchrones du bot
│── database.py           # Interaction avec la base de données MySQL
│── data_manager.py       # Centralisation des interactions entre modules
│── config.py             # Gestion des variables d’environnement
│── requirements.txt      # Liste des dépendances Python
│── .env                  # Variables d’environnement (non versionné)
│── templates/            # Templates HTML pour Flask
└── README.md             # Documentation du projet
```

---

## 🚀 Utilisation  

### 🤖 Commandes et interactions du bot Discord  
[![Image](https://i.goopics.net/meqo9u.gif)](https://goopics.net/i/meqo9u)

- **Ajouter un devoir** : via un modal dans Discord  
- **Afficher la liste des devoirs** : via un embed interactif  
- **Supprimer un devoir** : via un menu déroulant  

### 🖥️ Gestion des devoirs via l’interface web  
[![Image](https://i.goopics.net/wwa1ce.gif)](https://goopics.net/i/wwa1ce)

- **Ajout de devoirs** via un formulaire  
- **Consultation de la liste des devoirs**  
- **Suppression des devoirs**  

---

## 🛠️ Détails Techniques  

### 🔔 Programmation Asynchrone  
Le bot Discord repose sur `discord.py`, une bibliothèque asynchrone permettant d’exécuter des tâches en arrière-plan sans bloquer l’exécution principale.  
Les rappels sont gérés via une boucle `tasks.loop` qui vérifie périodiquement les devoirs.

### 📂 Explication des fichiers Python  

#### `main.py`  
Point d’entrée du projet, il :  
- Lance **Flask et le bot Discord** en parallèle via `threading.Thread`  
- Gère **les routes Flask** pour interagir avec la base de données  
- Initialise et exécute le **bot Discord**  

```python
from flask import Flask
import threading
import discord
from discord.ext import commands

app = Flask(__name__)

bot = commands.Bot(command_prefix="!")

@app.route("/")
def home():
    return "Serveur Flask en ligne"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_flask).start()
bot.run("VOTRE_DISCORD_TOKEN")
```

#### `ui.py`  
Gère **l’interface utilisateur** interactive sur Discord avec `discord.ui` :  
- Utilisation de **boutons et menus déroulants**  
- Gestion asynchrone des interactions  

```python
from discord.ui import Button, View

class DevoirButton(Button):
    def __init__(self, label, devoir_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.devoir_id = devoir_id

    async def callback(self, interaction):
        await interaction.response.send_message(f"Devoir {self.devoir_id} sélectionné", ephemeral=True)
```

#### `events.py`  
Gestion des **événements asynchrones** du bot :  
- Réaction aux événements Discord avec `@bot.event`  
- Suppression automatique des anciens messages  
- Planification de tâches répétitives avec `tasks.loop`  

```python
@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")
```

#### `database.py`  
Interaction avec **MySQL** pour stocker les devoirs :  
- **Connexion** à la base via `mysql.connector.connect()`  
- **Requêtes SQL** pour insérer, récupérer et supprimer des devoirs  
- **Utilisation de `conn.commit()`** pour garantir la persistance  

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="devoirs_db"
)

cursor = conn.cursor()

def ajouter_devoir(nom, date):
    query = "INSERT INTO devoirs (nom, date) VALUES (%s, %s)"
    cursor.execute(query, (nom, date))
    conn.commit()
```

#### `data_manager.py`  
Centralise les interactions entre **Flask, Discord et MySQL**.  

```python
def obtenir_devoirs():
    cursor.execute("SELECT * FROM devoirs")
    return cursor.fetchall()
```

#### `config.py`  
Stocke les variables d’environnement de manière sécurisée via `dotenv` :  

```python
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Résumé  
Chaque fichier du projet a un rôle bien défini et contribue à l’intégration fluide entre **Discord, Flask et MySQL**.  

- `main.py` : point d’entrée, exécution parallèle de Flask et du bot.  
- `ui.py` : interface interactive sur Discord avec boutons et menus.  
- `events.py` : gestion des événements et tâches planifiées.  
- `database.py` : interaction avec MySQL.  
- `data_manager.py` : centralisation des requêtes SQL.  
- `config.py` : gestion des variables d’environnement.  

L'architecture asynchrone du bot permet de **gérer efficacement les devoirs** tout en assurant une **réactivité optimale**.

---

## 🔥 Utilisation de Flask  

Le projet utilise **Flask** pour gérer l'interface web et permettre aux utilisateurs d'interagir avec la base de données via un navigateur.  

### 📌 Fonctionnalités de Flask  
Flask est utilisé pour :  

- **Afficher la liste des devoirs** via des templates HTML.  
- **Ajouter de nouveaux devoirs** à travers un formulaire.  
- **Supprimer des devoirs** grâce à des requêtes POST.  

### 🎓 Apprentissage de Flask  
L'utilisation de Flask a nécessité un apprentissage approfondi, car ce framework n'était pas connu au départ.  
Cela a permis d’acquérir des compétences en :  

- **Gestion de routes** (`@app.route()`).  
- **Templating Jinja** pour afficher dynamiquement les données.  
- **Manipulation de requêtes HTTP** (GET, POST) pour interagir avec la base de données.


---
## 🤖 Rôle de l'Intelligence Artificielle dans ce projet  

L’IA a joué un rôle clé dans la conception de ce projet, notamment pour :  

### 📚 Apprentissage des commandes Discord en Python  
- La documentation officielle de `discord.py` n’étant pas toujours claire, **ChatGPT** a été utilisé pour comprendre la création d'interfaces interactives comme les menus et les boutons.  

### 🔧 Construction de l’architecture Flask  
- Étant totalement novice sur Flask, l’IA a aidé à comprendre la logique derrière :  
  - La gestion des **routes**.  
  - L’utilisation des **templates** avec Jinja.  
  - L’interaction avec **MySQL** via Flask.  

### 🚀 Optimisation du code  
- **Amélioration des structures de code** grâce aux recommandations de l’IA.  
- **Meilleures pratiques** pour la gestion de la **programmation asynchrone** et des bases de données.  

Sans cette assistance, la mise en place de certaines fonctionnalités comme le système de **menus dans le bot Discord** ou la gestion **dynamique des devoirs** sur l’interface web aurait été beaucoup plus complexe.
---

## 🎯 Conclusion  

Le **gestionnaire de devoirs** est un projet qui allie **simplicité d’utilisation** et **flexibilité** :  

✔️ **Gestion efficace** des devoirs via Discord et une interface web.  
✔️ **Automatisation** pour ne plus oublier ses devoirs.  
✔️ **Expérience utilisateur fluide** avec une interface interactive.  
✔️ **Base de données MySQL** pour stocker les informations.  

Ce projet peut être amélioré avec :  
- **Des notifications avancées** (rappels personnalisés)  
- **Une gestion collaborative** des devoirs  
- **Une intégration avec d'autres outils éducatifs**  

🚀 **Prêt à être utilisé et amélioré !** 🚀  
