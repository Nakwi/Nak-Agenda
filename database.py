import mysql.connector

def get_connection():
    """Créer une connexion à la base de données MySQL."""
    return mysql.connector.connect(
        host="",       # Adresse du serveur MySQL
        user="",        # Utilisateur MySQL
        password="",      # Mot de passe utilisateur
        database="",  # Nom de la base de données
        port=3306               # Port exposé par MySQL
    )

def add_devoir(nom, deadline, pdf=None, rappel_at=None):
    """Ajoute un devoir dans la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO devoirs (nom, deadline, pdf, rappel_at) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nom, deadline, pdf, rappel_at))
    conn.commit()
    conn.close()

def fetch_devoirs():
    """Récupère tous les devoirs depuis la base de données."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devoirs ORDER BY deadline")
    devoirs = cursor.fetchall()
    conn.close()
    return devoirs

def delete_devoir(devoir_id):
    """Supprime un devoir par son ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devoirs WHERE id = %s", (devoir_id,))
    conn.commit()
    conn.close()
