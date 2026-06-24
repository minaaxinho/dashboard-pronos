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

# 3. Fonction pour charger les données
@st.cache_data(ttl=300)
def charger_donnees(url):
    df = pd.read_csv(url, decimal=',')
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    return df

# --- FONCTIONS DE NAVIGATION ---
def aller_a_indiv():
    st.session_state.page = "indiv"

def aller_a_equipe():
    st.session_state.page = "equipe"

def aller_a_stats():
    st.session_state.page = "stats"

def retour_accueil():
    st.session_state.page = "accueil"

# --- LOGIQUE D'AFFICHAGE ---
try:
    df = charger_donnees(URL_SHEET_CSV)

    # ÉCRAN D'ACCUEIL
    if st.session_state.page == "accueil":
        st.title("🏆 Tournoi de Pronostics")
        st.write("Bienvenue ! Choisissez la section que vous souhaitez consulter :")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("👤 Classement Individuel", use_container_width=True, on_click=aller_a_indiv)
        with col2:
            st.button("👥 Classement par Équipe", use_container_width=True, on_click=aller_a_equipe)
        with col3:
            st.button("📊 Statistiques (Jours en tête)", use_container_width=True, on_click=aller_a_stats)

    # PAGE INDIVIDUELLE (Colonnes A à AH)
    elif st.session_state.page == "indiv":
        if st.button("⬅️ Retour au menu"):
            retour_accueil()
            st.rerun()

        st.title("👤 Classement Individuel")
        
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
        
        df_equipe = pd.concat([df.iloc[:, [0]], df.iloc[:, 34:39]], axis=1)
        df_long = df_equipe.melt(id_vars='Date', var_name='Équipe', value_name='Points')
        
        fig = px.line(df_long, x='Date', y='Points', color='Équipe', markers=True)
        fig.update_layout(hovermode="x unified", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    # PAGE STATISTIQUES (Jours en tête)
    elif st.session_state.page == "stats":
        if st.button("⬅️ Retour au menu"):
            retour_accueil()
            st.rerun()

        st.title("📊 Statistiques : Jours en tête")
        st.write("Découvrez qui a dominé le classement le plus longtemps au cours du tournoi.")
        
        # --- Calcul des jours en tête (Individuel) ---
        # On enlève la colonne Date pour faire des calculs mathématiques
        df_indiv_calcul = df.iloc[:, 1:34].apply(pd.to_numeric, errors='coerce')
        # On compare chaque cellule au max de sa ligne, puis on compte combien de fois c'est Vrai
        jours_tete_indiv = df_indiv_calcul.eq(df_indiv_calcul.max(axis=1), axis=0).sum()
        top3_indiv = jours_tete_indiv.sort_values(ascending=False).head(3)

        # --- Calcul des jours en tête (Équipe) ---
        df_equipe_calcul = df.iloc[:, 34:39].apply(pd.to_numeric, errors='coerce')
        jours_tete_equipe = df_equipe_calcul.eq(df_equipe_calcul.max(axis=1), axis=0).sum()
        top3_equipe = jours_tete_equipe.sort_values(ascending=False).head(3)

        # --- Affichage des résultats en deux colonnes ---
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.subheader("🥇 Top 3 Individuel")
            for idx, (participant, jours) in enumerate(top3_indiv.items(), start=1):
                if jours > 0:
                    st.metric(label=f"N°{idx} - {participant}", value=f"{jours} jour(s)")
                
        with col_stat2:
            st.subheader("🥇 Top 3 Équipe")
            for idx, (equipe, jours) in enumerate(top3_equipe.items(), start=1):
                if jours > 0:
                    st.metric(label=f"N°{idx} - {equipe}", value=f"{jours} jour(s)")

except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")
