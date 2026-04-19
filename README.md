# 📄 ResumerPDF - Résumeur de PDF Intelligent

ResumerPDF est une application interactive permettant d'extraire, de résumer et d'évaluer automatiquement des fichiers PDF à l'aide de l'intelligence artificielle. L'application utilise des modèles de langage (Transformers) pour générer des résumés concis et permet de comparer ces résumés avec une version de référence via le score ROUGE.

## 🚀 Fonctionnalités

- **Extraction de texte** : Extraction précise du contenu textuel des fichiers PDF via `pdfplumber`.
- **Résumé automatique** : Utilisation de modèles de Hugging Face (`transformers`) pour générer des résumés intelligents.
- **Stockage MySQL** : Sauvegarde automatique des informations du PDF et de son résumé dans une base de données MySQL.
- **Évaluation ROUGE** : Calcul du score de précision ROUGE-1 pour comparer le résumé IA avec un résumé humain.
- **Interface Streamlit** : Une interface web fluide et réactive pour charger les fichiers et visualiser les résultats.
- **Visualisation de données** : Graphiques interactifs avec Plotly pour afficher les scores d'évaluation.

## 🛠️ Technologies utilisées

- **Langage** : Python 3.x
- **Interface** : Streamlit, Plotly
- **IA/NLP** : Transformers (Hugging Face), Torch, Rouge-score
- **Base de données** : MySQL, SQLAlchemy
- **Manipulation PDF** : pdfplumber

## 📋 Prérequis

- Python 3.8+
- Un serveur MySQL actif

## 🔧 Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/nmissi-nadia/ResumerPDF.git
   cd ResumerPDF
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer la base de données** :
   Assurez-vous que votre serveur MySQL est lancé et configurez vos accès dans `database/db_connection.py`.

4. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

## 📂 Structure du projet

- `app.py` : Point d'entrée de l'application Streamlit.
- `scripts/` : Contient la logique pour l'ingestion, le résumé, l'évaluation et la sauvegarde.
- `database/` : Configuration de la connexion à la base de données.
- `data/` : Dossier temporaire pour le stockage des fichiers PDF chargés.
- `requirements.txt` : Liste des bibliothèques nécessaires.

---
Développé avec ❤️ pour simplifier la lecture de vos documents.
