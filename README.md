# 📘 Gestionnaire de Devoirs – Documentation  

---

## 📝 Introduction  
Dans le cadre de ce projet, j’ai développé une application permettant de gérer des devoirs de manière efficace et interactive. Ce gestionnaire repose sur deux interfaces complémentaires :  

- **Un bot Discord ** : Il permet d'ajouter, afficher et supprimer des devoirs directement depuis un serveur Discord grâce à une interface interactive utilisant des boutons et des menus déroulants.  
- **Une interface graphique web ** : Basée sur Flask, elle offre une gestion visuelle des devoirs avec un design moderne, permettant aux utilisateurs d'ajouter, consulter et supprimer leurs tâches facilement.  

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
cd gestionnaire-devoirs
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

#### `main.py`  
- Point d’entrée principal du projet.  
- Exécution parallèle de Flask et du bot Discord avec `threading.Thread`.  
- Gestion des routes Flask pour interagir avec la base de données.  
- Initialisation et exécution du bot Discord.  

#### `ui.py`  
- Interface utilisateur interactive avec Discord.  
- Utilisation des modaux et boutons de `discord.ui` pour capturer des entrées utilisateurs.  
- Gestion des interactions asynchrones avec `interaction.response.send_message`.  

#### `events.py`  
- Gestion des événements asynchrones.  
- Utilisation du décorateur `@bot.event` pour réagir aux actions utilisateur.  
- Suppression automatique des anciens messages au lancement du bot.  
- Exécution d’une tâche planifiée (`tasks.loop`) pour vérifier et envoyer des rappels.  

#### `database.py`  
- Interaction avec une base de données MySQL.  
- Connexion avec `mysql.connector.connect()`.  
- Exécution de requêtes SQL pour insérer, récupérer et supprimer des devoirs.  
- Transactions SQL avec `conn.commit()` pour garantir la persistance des données.  

#### `data_manager.py`  
- Centralisation des interactions entre Flask, Discord et la base de données.  
- Encapsulation des appels SQL pour simplifier l’utilisation des autres modules.  

#### `config.py`  
- Gestion des variables d’environnement avec `dotenv`.  
- Chargement sécurisé des tokens et identifiants via `os.getenv()`.  


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

