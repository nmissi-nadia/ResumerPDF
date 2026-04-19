import streamlit as st
import plotly.express as px
import os
from scripts.save_to_db import insérer_pdf_dans_db, mise_a_jour_resume
from scripts.summarizer import generer_resume 
from scripts.data_ingestion import extraire_et_nettoyer_texte
from scripts.evaluation import calculer_score_rouge

# Configuration de la page
st.set_page_config(page_title="Mon Résumeur PDF", page_icon="📄")

st.title(" Projet : Résumeur de PDF")
st.write("Bienvenue ! Dépose un fichier PDF ci-dessous pour l'analyser.")

# Créer le dossier data s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

# Zone de dépôt du fichier
fichier_uploade = st.file_uploader("Choisis un fichier PDF", type="pdf")

if fichier_uploade is not None:
    st.info(f"Fichier chargé : **{fichier_uploade.name}**")
    
    # --- Zone pour le résumé humain ---
    st.markdown("---")
    st.subheader(" Évaluation du modèle (Optionnel)")
    resume_reference = st.text_area("Si tu as déjà un résumé idéal pour ce PDF, colle-le ici pour calculer le score ROUGE :", height=100)
    
    # Bouton pour traiter
    if st.button(" Sauvegarder et Résumer"):
        
        chemin_sauvegarde = os.path.join("data", fichier_uploade.name)
        with open(chemin_sauvegarde, "wb") as f:
            f.write(fichier_uploade.getbuffer())
        
        with st.spinner('Extraction du texte et envoi vers MySQL...'):
            succes, message_ou_texte = insérer_pdf_dans_db(fichier_uploade.name)
            
        if succes:
            st.success(" PDF sauvegardé en base de données !")
            
            st.markdown("---")
            st.subheader(" Génération du résumé par IA...")
            
            with st.spinner('Le cerveau numérique réfléchit...'):
                texte_complet = extraire_et_nettoyer_texte(chemin_sauvegarde)
                resume = generer_resume(texte_complet)
                
                st.success("Résumé généré avec succès !")
                st.warning(resume) 
                
                mise_a_jour_resume(fichier_uploade.name, resume)
                st.success(" Résumé enregistré dans la base de données !")

                # --- Calcul et affichage du ROUGE avec Graphique ---
                if resume_reference: # Si tu as écrit quelque chose dans la case
                    st.markdown("---")
                    st.subheader("Score de précision (ROUGE-1)")
                    with st.spinner("Calcul des scores..."):
                        scores = calculer_score_rouge(resume, resume_reference)
                        
                        # On transforme le score de 0.xxx en pourcentage (ex: 0.196 devient 19.6)
                        rouge1_pct = scores.get("ROUGE-1 (Mots simples)", 0) * 100
                        
                        # Création du diagramme circulaire
                        fig = px.pie(
                            values=[rouge1_pct, 100 - rouge1_pct], 
                            names=["Mots en commun", "Différences"], 
                            hole=0.6, # Fait un trou au milieu (Donut)
                            color_discrete_sequence=["#00CC96", "#333333"] # Vert et Gris foncé
                        )
                        
                        # Ajout du texte au centre du donut
                        fig.update_layout(
                            annotations=[dict(text=f"{rouge1_pct:.1f}%", x=0.5, y=0.5, font_size=30, showarrow=False)]
                        )
                        
                        # Affichage du graphique
                        st.plotly_chart(fig)
                        
                        st.info(" Ce graphique montre le pourcentage de mots exactement identiques entre ton texte et celui de l'IA.")
                
        else:
            st.error(message_ou_texte)