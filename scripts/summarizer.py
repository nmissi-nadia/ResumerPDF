from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import streamlit as st

# 1. On charge un LLM léger mais puissant pour les longs contextes (jusqu'à 32k mots)
model_name = "Qwen/Qwen2.5-0.5B-Instruct"

@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Chargement de {model_name} sur {device} (cela peut prendre du temps la 1ère fois)...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None
    )
    if device == "cpu":
        model = model.to(device)
    
    return tokenizer, model, device

tokenizer, model, device = load_model()
def generer_resume(texte_complet):
    """
    Génère un résumé en français à partir d'un long texte en utilisant un LLM.
    Le prompt force la création d'un résumé humainement cohérent et structuré.
    """
    if not texte_complet or len(texte_complet.strip()) == 0:
        return ""

    # Construction du Prompt structuré pour l'IA
    prompt = f"""Tu es un assistant IA expert en analyse de documents français. 
Lis attentivement le texte ci-dessous (provenant d'un PDF). 
Produis un résumé clair, structuré et détaillé qui capture l'essence du texte, les idées principales, et le contexte global. N'invente pas d'informations. Réponds uniquement en français.

Texte à résumer :
{texte_complet}

Résumé détaillé :
"""

    messages = [
        {"role": "system", "content": "You are a helpful and intelligent assistant."},
        {"role": "user", "content": prompt}
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    # Paramètres de génération (autoriser jusqu'à ~800 mots en sortie pour un texte long)
    print("Génération du résumé en cours par le LLM...")
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1000, 
        do_sample=True, # Un peu de créativité et de fluidité
        temperature=0.7, 
        top_p=0.9
    )
    
    # On retire le texte du prompt de la réponse pour ne garder que le résumé
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    resume_final = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return resume_final