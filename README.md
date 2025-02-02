# 📘 Gestionnaire de Devoirs – Documentation  

---

## 📝 Introduction  
Dans le cadre de ce projet, j’ai développé une application permettant de gérer des devoirs de manière efficace et interactive. Ce gestionnaire repose sur deux interfaces complémentaires :  

- **Un bot Discord** : Il permet d'ajouter, afficher et supprimer des devoirs directement depuis un serveur Discord grâce à une interface interactive utilisant des boutons et des menus déroulants.  
- **Une interface graphique web** : Basée sur Flask, elle offre une gestion visuelle des devoirs avec un design moderne, permettant aux utilisateurs d'ajouter, consulter et supprimer leurs tâches facilement.  

L’objectif de ce projet est de simplifier l’organisation des devoirs en combinant la flexibilité de Discord avec une interface accessible via un navigateur.


## ⚙️ Installation & Configuration  

### 📌 Prérequis  
Avant d’installer l’application, assurez-vous d’avoir les éléments suivants installés sur votre machine :  

- Python 3.x  
- MySQL  
- Pip  
- Un serveur Discord pour tester le bot  

### 📥 Installation des dépendances  
Clonez ce dépôt et installez les dépendances avec :  

```bash
git clone https://github.com/Nakwi/Nak-Agenda.git
cd Nak-Agenda
pip install -r requirements.txt
```
### ⚙️ Configuration de l’environnement
Créez un fichier .env à la racine du projet et ajoutez-y les informations suivantes :

```bash
DISCORD_TOKEN=ton_token_ici
DISCORD_CHANNEL_ID=123456789012345678
CHECK_INTERVAL=60
```
Remplacez ton_token_ici par votre token Discord et 123456789012345678 par l’ID du canal Discord où le bot interagira.

## 🏗️ Architecture du Projet  

Le projet est structuré de la manière suivante :  
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

## 🚀 Utilisation  

### 🖥️ Lancement du serveur Flask  
Exécutez la commande suivante pour démarrer le serveur Flask :  

```bash
python main.py
```

### 🤖 Commandes et interactions du bot Discord  
Le bot Discord propose plusieurs interactions :  

[![Image](https://i.goopics.net/meqo9u.gif)](https://goopics.net/i/meqo9u)

- **Ajouter un devoir** : via un modal dans Discord  
- **Afficher la liste des devoirs** : via un embed interactif  
- **Supprimer un devoir** : via un menu déroulant  

### 🖥️ Gestion des devoirs via l’interface web  
L’interface web permet :  

[![Image](https://i.goopics.net/wwa1ce.gif)](https://goopics.net/i/wwa1ce)

- **D’ajouter un devoir** via un formulaire  
- **De consulter la liste des devoirs**  
- **De supprimer un devoir**

## 🛠️ Détails Techniques  

### 🔔 Programmation Asynchrone  
Le bot Discord repose sur `discord.py`, une bibliothèque asynchrone permettant d’exécuter des tâches en arrière-plan sans bloquer l’exécution principale.  
La gestion des rappels repose sur une boucle de vérification (`tasks.loop`).  

### 📂 Explication des fichiers Python

## `main.py`
Ce fichier est le **point d’entrée principal** du projet. Il a plusieurs responsabilités :  

### 🔹 Lancement du bot Discord et du serveur Flask en parallèle  
L’utilisation de `threading.Thread` permet d’exécuter Flask et le bot Discord simultanément, garantissant que l’interface web et le bot fonctionnent ensemble sans conflit.  

### 🔹 Gestion des routes Flask  
Les routes Flask définissent les points d’accès pour l’interface web afin d’interagir avec la base de données (ajouter, afficher et supprimer des devoirs).  

### 🔹 Initialisation et exécution du bot Discord  
La connexion au serveur Discord se fait via le `DISCORD_TOKEN` récupéré dans un fichier `.env`.  

#### 🖥️ Extrait de `main.py` :  
```python
from flask import Flask
import threading
import discord
from discord.ext import commands

app = Flask(__name__)

# Création du bot Discord
bot = commands.Bot(command_prefix="!")

@app.route("/")
def home():
    return "Serveur Flask en ligne"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Démarrage de Flask en parallèle
threading.Thread(target=run_flask).start()

# Lancement du bot Discord
bot.run("VOTRE_DISCORD_TOKEN")
```

---

## `ui.py`
Ce fichier gère **l’interface utilisateur interactive** sur Discord.  

### 🔹 Utilisation de `discord.ui` pour les interactions  
Les boutons et menus déroulants permettent aux utilisateurs de gérer les devoirs sans avoir à taper de commandes.  

### 🔹 Gestion asynchrone des interactions  
`interaction.response.send_message()` est utilisé pour répondre aux utilisateurs de manière interactive.  

#### 🖥️ Exemple d’un bouton interactif :  
```python
from discord.ui import Button, View

class DevoirButton(Button):
    def __init__(self, label, devoir_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.devoir_id = devoir_id

    async def callback(self, interaction):
        await interaction.response.send_message(f"Devoir {self.devoir_id} sélectionné", ephemeral=True)
```

---

## `events.py`
Ce fichier gère les **événements asynchrones** du bot.  

### 🔹 Utilisation du décorateur `@bot.event`  
Permet d’exécuter des actions en réponse aux événements Discord (messages envoyés, bot connecté, etc.).  

### 🔹 Suppression automatique des anciens messages  
Utile pour garder le chat propre lorsque le bot affiche régulièrement la liste des devoirs.  

### 🔹 Planification de tâches répétitives avec `tasks.loop`  
Utilisé pour vérifier les devoirs à échéance et envoyer des rappels.  

#### 🖥️ Exemple d'un événement qui affiche un message lorsque le bot est en ligne :  
```python
@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")
```

---

## `database.py`
Ce fichier gère l’**interaction avec la base de données MySQL**.  

### 🔹 Connexion à MySQL avec `mysql.connector.connect()`  
Permet d’établir un lien avec une base de données externe pour stocker les devoirs.  

### 🔹 Exécution de requêtes SQL  
Insertion, récupération et suppression des devoirs en base de données.  

### 🔹 Utilisation de `conn.commit()`  
Assure la persistance des modifications.  

#### 🖥️ Exemple de connexion à la base de données et d'insertion d'un devoir :  
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

---

## `data_manager.py`
Ce fichier **centralise les interactions** entre Flask, Discord et la base de données.  

### 🔹 Encapsulation des appels SQL  
Permet d’avoir une interface unique pour interagir avec la base de données sans dupliquer du code dans plusieurs fichiers.  

### 🔹 Facilite l’intégration entre les différents modules  
Les fonctions ici sont utilisées aussi bien par Flask que par le bot Discord.  

#### 🖥️ Exemple d’une fonction qui récupère tous les devoirs :  
```python
def obtenir_devoirs():
    cursor.execute("SELECT * FROM devoirs")
    return cursor.fetchall()
```

---

## `config.py`
Ce fichier gère la **configuration et les variables d’environnement**.  

### 🔹 Utilisation de `dotenv`  
Permet de stocker les tokens et identifiants dans un fichier `.env` au lieu du code source.  

### 🔹 Chargement sécurisé des variables  
`os.getenv()` est utilisé pour récupérer les valeurs sans les exposer dans le code.  

#### 🖥️ Exemple :  
```python
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

### 🏁 Conclusion  
Chaque fichier du projet a un rôle bien défini et contribue à l’intégration fluide entre **Discord, Flask et MySQL**.  

- `main.py` : point d’entrée, exécution parallèle de Flask et du bot.  
- `ui.py` : interface interactive sur Discord avec boutons et menus.  
- `events.py` : gestion des événements et tâches planifiées.  
- `database.py` : interaction avec MySQL.  
- `data_manager.py` : centralisation des requêtes SQL.  
- `config.py` : gestion des variables d’environnement.  

L'architecture asynchrone du bot permet de **gérer efficacement les devoirs** tout en assurant une **réactivité optimale**.


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

## 🎯 Conclusion  

Ce projet permet de **gérer efficacement les devoirs** via deux interfaces intuitives : **Discord** et une **interface web**.  
Il peut être facilement **amélioré** et **personnalisé** selon les besoins.  

### 🚀 Points forts du projet :  
✔️ **Gestion centralisée des devoirs** via Discord et une interface web.  
✔️ **Automatisation et rappels** pour ne plus oublier ses devoirs.  
✔️ **Expérience utilisateur fluide** avec une interface interactive.  
✔️ **Utilisation d’une base de données** pour stocker les informations.  

### 📌 Apprentissage et amélioration :  
L’intelligence artificielle a permis :  
- D’**accélérer** le développement du projet.  
- D’**apprendre** des concepts avancés en programmation (Flask, Discord.py).  
- D’**optimiser** l’architecture du projet.  

Ce projet est une **base solide** qui peut être étendue avec des **nouvelles fonctionnalités**, comme l’intégration d’un **système de notifications avancé** ou la gestion **collaborative des devoirs**. 🚀  

