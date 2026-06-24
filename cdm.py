import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Dashboard Pronos", layout="wide")
st.title("🏆 Évolution du Tournoi de Pronostics")

# 2. Ton lien Google Sheets publié en CSV
URL_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQZTYmWFgWslN3Co8nlcUxCYJWMML6D28tGcEBDJTZHTSfIHOwOdagpX_W8ekhtyqV4I4Qn24VQtBD/pub?gid=868769003&single=true&output=csv"

# 3. Fonction pour charger les données (avec un cache pour la rapidité)
@st.cache_data(ttl=300) # Le dashboard gardera les données en mémoire 5 minutes avant de revérifier le Sheet
def charger_donnees(url):
    df = pd.read_csv(url)
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df_long = df.melt(id_vars='Date', var_name='Participant', value_name='Points Cumulés')
    return df_long

try:
    # 4. Récupération des données
    donnees = charger_donnees(URL_SHEET_CSV)

    # 5. Création du graphique interactif
    fig = px.line(
        donnees, 
        x='Date', 
        y='Points Cumulés', 
        color='Participant',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Points",
        legend_title="Participants",
        hovermode="x unified"
    )

    # 6. Affichage sur le dashboard
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Impossible de charger les données. Vérifie que le lien Google Sheets est correct. Erreur: {e}")
