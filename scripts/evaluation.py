import evaluate

# On charge la métrique ROUGE (le téléchargement se fera la première fois)
rouge = evaluate.load("rouge")

def calculer_score_rouge(resume_ia, resume_humain):
    """
    Compare le résumé de l'IA avec le résumé humain et renvoie les scores ROUGE.
    """
    try:
        # La fonction compute a besoin de listes (même pour un seul texte)
        resultats = rouge.compute(predictions=[resume_ia], references=[resume_humain])
        
        # On arrondit les scores pour que ce soit plus joli (ex: 0.45 au lieu de 0.452398)
        scores_arrondis = {
            "ROUGE-1 (Mots simples)": round(resultats["rouge1"], 3),
            "ROUGE-2 (Paires de mots)": round(resultats["rouge2"], 3),
            "ROUGE-L (Phrases entières)": round(resultats["rougeL"], 3)
        }
        return scores_arrondis
        
    except Exception as e:
        return {"erreur": str(e)}