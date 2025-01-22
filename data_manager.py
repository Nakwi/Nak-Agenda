from database import fetch_devoirs, add_devoir, delete_devoir

def load_devoirs():
    """Récupère la liste des devoirs depuis la base de données."""
    return fetch_devoirs()

def save_devoirs(nom, deadline, pdf=None, description=None, rappel_at=None):
    """Ajoute un nouveau devoir dans la base de données."""
    add_devoir(nom, deadline, pdf, description, rappel_at)

def remove_devoir(devoir_id):
    """Supprime un devoir dans la base de données."""
    delete_devoir(devoir_id)
