import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="siham1234567890",  # Laisse bien les guillemets vides
        database="nlp_resume_db",
        port=3307     # <-- AJOUTE CETTE LIGNE ICI (n'oublie pas la virgule sur la ligne du dessus)
    )
    return conn