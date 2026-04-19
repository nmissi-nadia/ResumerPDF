import os
import sys
# On permet au script de voir les autres dossiers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import get_connection
from scripts.data_ingestion import extraire_et_nettoyer_texte

def insérer_pdf_dans_db(nom_fichier):
    # Chemin vers le fichier dans le dossier data
    chemin_pdf = os.path.join("data", nom_fichier)
    
    # 1. Extraction du texte
    texte_extrait = extraire_et_nettoyer_texte(chemin_pdf)
    
    if texte_extrait.startswith("Erreur"):
        return False, texte_extrait

    # 2. Connexion BD
    conn = get_connection()
    if conn is None:
        return False, "Erreur de connexion à la base de données."

    try:
        cursor = conn.cursor()
        
        # --- CORRECTION ICI : On utilise tes vrais noms de colonnes ---
        query = "INSERT INTO documents (filename, original_text) VALUES (%s, %s)"
        valeurs = (nom_fichier, texte_extrait)
        
        cursor.execute(query, valeurs)
        conn.commit()
        return True, "Succès ! PDF sauvegardé."
        
    except Exception as e:
        return False, f"Erreur SQL : {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def mise_a_jour_resume(nom_fichier, resume_genere):
    """ Met à jour la colonne summary dans la base de données """
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        # On met à jour la ligne qui a ce nom de fichier
        query = "UPDATE documents SET summary = %s WHERE filename = %s"
        valeurs = (resume_genere, nom_fichier)
        
        cursor.execute(query, valeurs)
        conn.commit()
        print("Résumé sauvegardé en base de données.")
        
    except Exception as e:
        print(f"Erreur lors de la mise à jour du résumé : {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()