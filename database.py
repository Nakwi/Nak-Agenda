import mysql.connector

def get_connection():
    """Créer une connexion à la base de données MySQL."""
    return mysql.connector.connect(
        host="localhost",       # Adresse du serveur MySQL
        user="nak_user",        # Utilisateur MySQL
        password="mdp",      # Mot de passe utilisateur
        database="nak_agenda",  # Nom de la base de données
        port=3306               # Port exposé par MySQL
    )

def add_devoir(nom, deadline, pdf=None, description=None, rappel_at=None):
    """Ajoute un devoir dans la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO devoirs (nom, deadline, pdf, description, rappel_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nom, deadline, pdf, description, rappel_at))
    conn.commit()
    conn.close()

def fetch_devoirs():
    """Récupère tous les devoirs depuis la base de données."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM devoirs ORDER BY deadline"
    cursor.execute(query)
    devoirs = cursor.fetchall()
    conn.close()
    return devoirs

def delete_devoir(devoir_id):
    """Supprime un devoir par son ID."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM devoirs WHERE id = %s"
    cursor.execute(query, (devoir_id,))
    conn.commit()
    conn.close()
