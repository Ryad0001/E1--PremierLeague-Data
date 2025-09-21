import streamlit as st
import requests
import pandas as pd

# URL de ton API FastAPI
API_URL = "http://127.0.0.1:8000"  # Assure-toi que l'API est lancée sur cette adresse

# Fonction pour récupérer toutes les équipes
def get_teams():
    response = requests.get(f"{API_URL}/test")
    if response.status_code == 200:
        teams = response.json()
        return pd.DataFrame(teams)
    else:
        st.error("Erreur lors de la récupération des équipes.")
        return pd.DataFrame()

# Fonction pour récupérer les équipes ayant plus de 80 points
def get_top_teams():
    response = requests.get(f"{API_URL}/top-teams")
    if response.status_code == 200:
        teams = response.json()
        return pd.DataFrame(teams)
    else:
        st.error("Erreur lors de la récupération des meilleures équipes.")
        return pd.DataFrame()

# Fonction pour récupérer la valeur marchande d'un club
def get_market_value(club_name):
    response = requests.get(f"{API_URL}/market-value/{club_name}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération de la valeur marchande pour {club_name}.")
        return {}

# Interface utilisateur avec Streamlit
st.title("API Premier League 2023-2024")

# Sélection de l'action par l'utilisateur
option = st.selectbox("Choisissez une action", ["Afficher toutes les équipes", "Afficher les meilleures équipes", "Consulter la valeur marchande d'un club"])

if option == "Afficher toutes les équipes":
    df_teams = get_teams()
    if not df_teams.empty:
        st.write(df_teams)
    else:
        st.write("Aucune équipe trouvée.")

elif option == "Afficher les meilleures équipes":
    df_top_teams = get_top_teams()
    if not df_top_teams.empty:
        st.write(df_top_teams)
    else:
        st.write("Aucune équipe ne correspond aux critères.")

elif option == "Consulter la valeur marchande d'un club":
    club_name = st.text_input("Entrez le nom du club")
    if club_name:
        market_value = get_market_value(club_name)
        if market_value:
            st.write(f"La valeur marchande de {club_name} est de {market_value['Market_Value']} millions.")
        else:
            st.write(f"Aucune donnée trouvée pour {club_name}.")
