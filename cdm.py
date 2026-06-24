import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Dashboard Pronos", layout="wide")
st.title("🏆 Évolution du Tournoi de Pronostics")

# 2. Ton lien Google Sheets publié en CSV
URL_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQZTYmWFgWslN3Co8nlcUxCYJWMML6D28tGcEBDJTZHTSfIHOwOdagpX_W8ekhtyqV4I4Qn24VQtBD/pub?gid=868769003&single=true&output=csv"

# 3. Fonction pour charger les données
@st.cache_data(ttl=300)
def charger_donnees(url):
    df = pd.read_csv(url)
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    return df

try:
    # 4. Récupération des données
    df = charger_donnees(URL_SHEET_CSV)

    # 5. Séparation des données en deux DataFrames
    # A à AH : Index 0 à 33 inclus (donc tranche 0:34)
    df_groupe1 = df.iloc[:, 0:34]
    
    # AI à AM : Index 34 à 38 inclus (donc tranche 34:39)
    # On ajoute la colonne Date (index 0) avec pd.concat
    df_groupe2 = pd.concat([df.iloc[:, [0]], df.iloc[:, 34:39]], axis=1)

    # Passage au format "long" pour que Plotly puisse tracer les courbes
    df_long_1 = df_groupe1.melt(id_vars='Date', var_name='Participant', value_name='Points Cumulés')
    df_long_2 = df_groupe2.melt(id_vars='Date', var_name='Participant', value_name='Points Cumulés')

    # 6. Création et affichage du premier graphique (A à AH)
    st.subheader("Classement Principal (A à AH)")
    fig1 = px.line(
        df_long_1, 
        x='Date', 
        y='Points Cumulés', 
        color='Participant',
        markers=True
    )
    fig1.update_layout(
        xaxis_title="",
        yaxis_title="Points",
        legend_title="Participants",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 7. Création et affichage du second graphique (AI à AM)
    st.subheader("Classement Secondaire (AI à AM)")
    fig2 = px.line(
        df_long_2, 
        x='Date', 
        y='Points Cumulés', 
        color='Participant',
        markers=True
    )
    fig2.update_layout(
        xaxis_title="",
        yaxis_title="Points",
        legend_title="Participants",
        hovermode="x unified"
    )
    st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Impossible de charger les données. Vérifie que le lien Google Sheets est correct et contient toutes les colonnes ciblées. Erreur: {e}")
