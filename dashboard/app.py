import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
import requests
import zipfile
import io

st.set_page_config(page_title="Benin Insights 2026", layout="wide")

PALETTE = {'primary': '#E91E8C', 'secondary': '#7B2FBE', 'accent': '#00D4AA'}

st.title("Benin Insights Challenge - Dashboard")
st.markdown("---")

# Liste des codes pays CEDEAO
ECOWAS_CODES = ['BN', 'TO', 'NG', 'GH', 'IV', 'UV', 'NI', 'ML', 'SG', 'SL', 'LI', 'GV', 'PU', 'GM', 'CV']

def fetch_live_gdelt():
    """Télécharge les dernières 15 minutes de données GDELT réelles"""
    try:
        url = "http://data.gdeltproject.org/gdeltv2/last15min.export.CSV.zip"
        r = requests.get(url, timeout=10)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        file_name = z.namelist()[0]
        
        # GDELT 2.0 columns (subset)
        cols = [0, 1, 2, 3, 4, 5, 6, 7, 26, 27, 28, 29, 30, 31, 32, 33, 34, 40, 52, 53, 56, 57, 58, 60]
        col_names = ['GlobalEventID', 'Day', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone', 'Actor2Name', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'SOURCEURL']
        
        df_live = pd.read_csv(z.open(file_name), sep='\t', header=None, usecols=cols, names=col_names)
        
        # Filtrage sur la CEDEAO
        df_ecowas = df_live[df_live['ActionGeo_CountryCode'].isin(ECOWAS_CODES)].copy()
        
        # Formattage
        df_ecowas['date'] = pd.to_datetime(df_ecowas['Day'], format='%Y%m%d')
        df_ecowas['IsConflict'] = (df_ecowas['QuadClass'] >= 3).astype(int)
        df_ecowas['Country'] = df_ecowas['ActionGeo_CountryCode']
        
        return df_ecowas
    except Exception as e:
        st.sidebar.error(f"Erreur de connexion GDELT: {e}")
        return None

@st.cache_data
def get_data():
    path = Path("data/processed/gdelt_benin_clean.csv")
    if not path.exists():
        return None
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    if 'Country' not in data.columns:
        data['Country'] = 'BN'
    return data

# Initialisation du session state pour les données live
if 'live_data' not in st.session_state:
    st.session_state.live_data = pd.DataFrame()

raw_df = get_data()

if raw_df is not None:
    st.sidebar.header("Paramètres")
    
    # Bouton de téléchargement à la demande
    st.sidebar.subheader("Données Live")
    if st.sidebar.button("🔌 Charger données CEDEAO (Live)"):
        with st.sidebar.status("Connexion GDELT..."):
            new_data = fetch_live_gdelt()
            if new_data is not None and not new_data.empty:
                st.session_state.live_data = pd.concat([st.session_state.live_data, new_data], ignore_index=True).drop_duplicates(subset=['GlobalEventID'])
                st.sidebar.success(f"{len(new_data)} événements capturés !")
            else:
                st.sidebar.warning("Aucun nouvel événement détecté à l'instant.")

    # Fusion avec les données de base
    if not st.session_state.live_data.empty:
        df = pd.concat([raw_df, st.session_state.live_data], ignore_index=True)
    else:
        df = raw_df

    # Demo mode si pas de données live
    regional_demo = st.sidebar.toggle("Mode Simulation Régionale", value=False)
    if regional_demo and st.session_state.live_data.empty:
        wa_coords = {'Togo':[6.13,1.22], 'Nigeria':[9.08,7.39], 'Ghana':[5.6,-0.19], 'Niger':[13.5,2.1]}
        frames = [df]
        for country, pos in wa_coords.items():
            temp = raw_df.sample(50, replace=True).copy()
            temp['Country'] = country
            temp['ActionGeo_Lat'] = pos[0] + np.random.normal(0,0.4,50)
            temp['ActionGeo_Long'] = pos[1] + np.random.normal(0,0.4,50)
            frames.append(temp)
        df = pd.concat(frames, ignore_index=True)

    selected_countries = st.sidebar.multiselect("Filtrer par Pays", options=sorted(df['Country'].unique()), default=df['Country'].unique())
    dates = st.sidebar.date_input("Intervalle", value=(df['date'].min(), df['date'].max()))

    mask = df['Country'].isin(selected_countries)
    if isinstance(dates, tuple) and len(dates) == 2:
        mask &= (df['date'].dt.date >= dates[0]) & (df['date'].dt.date <= dates[1])
    
    df_final = df.loc[mask].copy()

    # Jittering
    if not df_final.empty:
        df_final['ActionGeo_Lat'] += np.random.uniform(-0.1, 0.1, len(df_final))
        df_final['ActionGeo_Long'] += np.random.uniform(-0.1, 0.1, len(df_final))

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Événements", f"{len(df_final):,}")
    m2.metric("Score Tonalité", f"{df_final['AvgTone'].mean():.2f}")
    m3.metric("Taux Conflit", f"{df_final['IsConflict'].mean()*100:.1f}%")
    m4.metric("Impact Média", f"{df_final['NumArticles'].sum():,}")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Suivi de la Tonalité")
        timeline = df_final.groupby(['date', 'Country'])['AvgTone'].mean().reset_index()
        st.plotly_chart(px.line(timeline, x='date', y='AvgTone', color='Country', template="plotly_dark"), width="stretch")
    with c2:
        st.subheader("Nature des Événements")
        counts = df_final['IsConflict'].value_counts()
        names = ['Coopération' if i == 0 else 'Conflit' for i in counts.index]
        st.plotly_chart(px.pie(values=counts.values, names=names, color_discrete_sequence=[PALETTE['accent'], PALETTE['primary']], hole=0.4, template="plotly_dark"), width="stretch")

    st.subheader("Cartographie des Points d'Intérêt")
    if 'ActionGeo_Lat' in df_final.columns and not df_final.empty:
        fig_m = px.scatter_map(df_final, lat="ActionGeo_Lat", lon="ActionGeo_Long", 
                              size="NumArticles", color="AvgTone",
                              hover_name="ActionGeo_FullName",
                              color_continuous_scale='RdYlGn', range_color=[-4, 4],
                              zoom=3 if len(selected_countries)>1 else 6, height=650, opacity=0.6)
        fig_m.update_layout(map_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='black', font_color="white")
        st.plotly_chart(fig_m, width="stretch")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Status")
    if not st.session_state.live_data.empty:
        st.sidebar.success("📡 Données Live intégrées")
    else:
        st.sidebar.info("Utilisation des archives locales")

else:
    st.info("Chargement...")
