import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Dashboard Pronos", layout="wide")

# Initialisation du menu dans l'état de la session (session_state)
if 'page' not in st.session_state:
    st.session_state.page = "accueil"

# 2. Ton lien Google Sheets publié en CSV
URL_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQZTYmWFgWslN3Co8nlcUxCYJWMML6D28tGcEBDJTZHTSfIHOwOdagpX_W8ekhtyqV4I4Qn24VQtBD/pub?gid=868769003&single=true&output=csv"

# 3. Fonction pour charger les données (avec correction des virgules)
@st.cache_data(ttl=300)
def charger_donnees(url):
    # decimal=',' permet de transformer "7,14" en 7.14 pour que Python comprenne les chiffres
    df = pd.read_csv(url, decimal=',')
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    return df

# --- FONCTIONS DE NAVIGATION ---
def aller_a_indiv():
    st.session_state.page = "indiv"

def aller_a_equipe():
    st.session_state.page = "equipe"

def retour_accueil():
    st.session_state.page = "accueil"

# --- LOGIQUE D'AFFICHAGE ---
try:
    df = charger_donnees(URL_SHEET_CSV)

    # ÉCRAN D'ACCUEIL
    if st.session_state.page == "accueil":
        st.title("🏆 Tournoi de Pronostics")
        st.write("Bienvenue ! Choisissez le classement que vous souhaitez consulter :")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("👤 Classement Individuel", use_container_width=True, on_click=aller_a_indiv)
        with col2:
            st.button("👥 Classement par Équipe", use_container_width=True, on_click=aller_a_equipe)

    # PAGE INDIVIDUELLE (Colonnes A à AH)
    elif st.session_state.page == "indiv":
        if st.button("⬅️ Retour au menu"):
            retour_accueil()
            st.rerun()

        st.title("👤 Classement Individuel")
        
        # Sélection des colonnes A à AH (Index 0 à 34 exclu)
        df_indiv = df.iloc[:, 0:34]
        df_long = df_indiv.melt(id_vars='Date', var_name='Participant', value_name='Points')
        
        fig = px.line(df_long, x='Date', y='Points', color='Participant', markers=True)
        fig.update_layout(hovermode="x unified", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    # PAGE ÉQUIPE (Colonnes AI à AM)
    elif st.session_state.page == "equipe":
        if st.button("⬅️ Retour au menu"):
            retour_accueil()
            st.rerun()

        st.title("👥 Classement par Équipe")
        
        # Sélection de la colonne Date + colonnes AI à AM (index 34 à 39 exclu)
        df_equipe = pd.concat([df.iloc[:, [0]], df.iloc[:, 34:39]], axis=1)
        df_long = df_equipe.melt(id_vars='Date', var_name='Équipe', value_name='Points')
        
        fig = px.line(df_long, x='Date', y='Points', color='Équipe', markers=True)
        fig.update_layout(hovermode="x unified", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")
