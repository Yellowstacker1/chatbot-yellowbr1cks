import streamlit as st
import requests
import json
from typing import Optional

# Données de l'API Langflow
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "e8c4251b-7d97-4c85-9ba5-42cab83b0120"
FLOW_ID = "e8322657-9520-4788-9c44-ad671f77c852"
APPLICATION_TOKEN = "0VoF0NZ_P2LLzU_AoWrb36qrVJy3EIoF"
ENDPOINT = ""  # Spécifier l'endpoint si nécessaire

# Tweaks prédéfinis
TWEAKS = {
  "ChatInput-veSQz": {},
  "Prompt-nziAE": {},
  "ChatOutput-6mSTT": {},
  "OpenAIModel-uzYPY": {}
}

# Fonction pour exécuter le flux via l'API Langflow
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Application Streamlit
st.title("Langflow Workflow avec Streamlit")

# Champ pour saisir le message utilisateur
user_input = st.text_input("Entrez votre message :")

# Sélectionnez un endpoint ou utilisez celui par défaut
endpoint = st.text_input("Endpoint (facultatif) :", value=FLOW_ID)

# Bouton pour exécuter le workflow
if st.button("Exécuter le Workflow"):
    if user_input:
        # Appel à la fonction run_flow
        try:
            response = run_flow(
                message=user_input,
                endpoint=endpoint or FLOW_ID,
                tweaks=TWEAKS,
                application_token=APPLICATION_TOKEN
            )
            st.write("Résultat :")
            st.json(response)  # Affiche la réponse formatée
        except Exception as e:
            st.error(f"Erreur : {e}")
    else:
        st.warning("Veuillez entrer un message.")
