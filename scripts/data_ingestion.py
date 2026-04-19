import fitz  # PyMuPDF (Remplace pdfplumber pour mieux lire les accents)
import re
import os

def extraire_et_nettoyer_texte(chemin_pdf):
    texte_complet = ""
    
    # Vérifier si le fichier existe
    if not os.path.exists(chemin_pdf):
        return f"Erreur : Le fichier {chemin_pdf} est introuvable. Vérifie le chemin !"

    # 1. Extraction avec PyMuPDF (fitz)
    try:
        # Ouverture du document
        doc = fitz.open(chemin_pdf)
        
        # Lecture page par page
        for page in doc:
            texte_page = page.get_text()
            if texte_page:
                texte_complet += texte_page + "\n"
                
        # Fermeture du document (bonne pratique)
        doc.close()
        
    except Exception as e:
        return f"Erreur lors de la lecture du PDF : {e}"
                
    # 2. Nettoyage avec Regex
    # On nettoie le bruit habituel des PDF
    
    # 2.1 Enlever les URL/Liens web
    texte_nettoye = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', texte_complet)
    
    # 2.2 Enlever les adresses emails
    texte_nettoye = re.sub(r'[\w\.-]+@[\w\.-]+', ' ', texte_nettoye)
    
    # 2.3 Enlever les numéros de page isolés ou en-têtes (ex: "Page 1/12", " - 4 - ")
    texte_nettoye = re.sub(r'(?i)page\s+\d+(?:/\d+)?', ' ', texte_nettoye)
    texte_nettoye = re.sub(r'^\s*-\s*\d+\s*-\s*$', ' ', texte_nettoye, flags=re.MULTILINE)
    
    # 2.4 On remplace les sauts de ligne multiples par un espace
    texte_nettoye = re.sub(r'\n+', ' ', texte_nettoye)
    
    # 2.5 Garder uniquement les caractères lisibles (lettres, chiffres, ponctuation standard) en 
    # supprimant les caractères bizarres d'encodage PDF
    texte_nettoye = re.sub(r'[^\w\s.,;:!?\'"()-éèàùâêîôûçëïü]', ' ', texte_nettoye)
    
    # 2.6 On enlève les espaces en trop (double/triple espaces)
    texte_nettoye = re.sub(r'\s{2,}', ' ', texte_nettoye).strip()
    
    return texte_nettoye

# --- Zone de test ---
if __name__ == "__main__":
    # CHANGER LE NOM DU FICHIER ICI 👇
    chemin_test = "data/nom_de_ton_fichier.pdf" 
    
    texte = extraire_et_nettoyer_texte(chemin_test)
    
    if texte.startswith("Erreur"):
        print(texte)
    else:
        print("\n" + "="*50)
        print(" EXTRACTION RÉUSSIE ! Voici les 1000 premiers caractères :")
        print("="*50 + "\n")
        print(texte[:1000]) 
        print("\n" + "="*50)