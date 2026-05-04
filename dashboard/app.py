import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuration de la page
st.set_page_config(page_title="Bénin Insights 2026", page_icon="🇧🇯", layout="wide")

# Couleurs iSHEERO
COLORS = {'primary': '#E91E8C', 'secondary': '#7B2FBE', 'accent': '#00D4AA', 'dark': '#1A1A2E'}

st.title("🇧🇯 Bénin Insights Challenge 2026")
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    path = Path("data/processed/gdelt_benin_clean.csv")
    if not path.exists():
        st.error("❌ Données introuvables. Veuillez lancer le pipeline d'extraction.")
        return None
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

if df is not None:
    # --- Sidebar : Filtres ---
    st.sidebar.header("🔍 Filtres")
    date_range = st.sidebar.date_input(
        "Période d'analyse",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )

    # Filtrage des données
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

    # --- Métriques Clés ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Événements", f"{len(df_filtered):,}")
    col2.metric("Tonalité Moyenne", f"{df_filtered['AvgTone'].mean():.2f}")
    col3.metric("% Conflits", f"{df_filtered['IsConflict'].mean()*100:.1f}%")
    col4.metric("Articles", f"{df_filtered['NumArticles'].sum():,}")

    st.markdown("---")

    # --- Visualisations ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("📈 Évolution de la Tonalité")
        df_timeline = df_filtered.groupby('date')['AvgTone'].mean().reset_index()
        fig_tone = px.line(df_timeline, x='date', y='AvgTone', 
                          color_discrete_sequence=[COLORS['primary']])
        fig_tone.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_tone, use_container_width=True)

    with row1_col2:
        st.subheader("⚖️ Coopération vs Conflit")
        conf_counts = df_filtered['IsConflict'].value_counts()
        # On s'assure d'avoir les bonnes étiquettes même s'il manque une catégorie
        labels = []
        if 0 in conf_counts.index: labels.append('Coopération')
        if 1 in conf_counts.index: labels.append('Conflit')
        
        fig_pie = px.pie(values=conf_counts.values, names=labels,
                        color_discrete_sequence=[COLORS['accent'], COLORS['primary']],
                        hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Carte ---
    st.subheader("🗺️ Localisation des Événements")
    if 'ActionGeo_Lat' in df_filtered.columns and 'ActionGeo_Long' in df_filtered.columns:
        # On retire les lignes sans coordonnées pour la carte
        df_map_data = df_filtered.dropna(subset=['ActionGeo_Lat', 'ActionGeo_Long'])
        if not df_map_data.empty:
            df_geo = df_map_data.groupby(['ActionGeo_FullName', 'ActionGeo_Lat', 'ActionGeo_Long']).size().reset_index(name='count')
            fig_map = px.scatter_mapbox(df_geo, lat="ActionGeo_Lat", lon="ActionGeo_Long", 
                                       size="count", hover_name="ActionGeo_FullName",
                                       color_discrete_sequence=[COLORS['secondary']],
                                       zoom=6, height=500)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Aucune donnée géographique disponible pour la période sélectionnée.")

    # --- Insights ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Insights")
    st.sidebar.info("Utilisez ces résultats pour votre Executive Summary !")
    
    st.sidebar.write(f"- **Polarisation :** Le ton moyen est de {df_filtered['AvgTone'].mean():.2f}.")
    st.sidebar.write(f"- **Volume :** {len(df_filtered)} faits marquants recensés sur la période.")

else:
    st.info("Veuillez patienter pendant la génération des données...")
