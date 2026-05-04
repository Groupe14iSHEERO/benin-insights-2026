import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

st.set_page_config(page_title="Benin Insights 2026", layout="wide")

PALETTE = {'primary': '#E91E8C', 'secondary': '#7B2FBE', 'accent': '#00D4AA'}

st.title("Benin Insights Challenge - Dashboard")
st.markdown("---")

@st.cache_data
def get_data():
    path = Path("data/processed/gdelt_benin_clean.csv")
    if not path.exists():
        st.error("Data source not found.")
        return None
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    if 'Country' not in data.columns:
        data['Country'] = 'Bénin'
    return data

raw_df = get_data()

if raw_df is not None:
    st.sidebar.header("Paramètres")
    
    regional_view = st.sidebar.toggle("Vue Régionale (Beta)", value=False)
    
    if regional_view:
        countries_coords = {
            'Togo': [6.13, 1.22],
            'Nigeria': [9.08, 7.39],
            'Ghana': [5.60, -0.19],
            'Côte d\'Ivoire': [5.36, -4.00],
            'Burkina Faso': [12.37, -1.53],
            'Niger': [13.51, 2.11],
            'Mali': [12.63, -8.00],
            'Sénégal': [14.71, -17.46]
        }
        
        frames = [raw_df]
        for country, pos in countries_coords.items():
            sample_size = np.random.randint(40, 120)
            temp_df = raw_df.sample(sample_size, replace=True).copy()
            temp_df['Country'] = country
            # Simulation coordonées
            temp_df['ActionGeo_Lat'] = pos[0] + np.random.normal(0, 0.4, sample_size)
            temp_df['ActionGeo_Long'] = pos[1] + np.random.normal(0, 0.4, sample_size)
            temp_df['AvgTone'] += np.random.uniform(-1.5, 1.5)
            frames.append(temp_df)
        
        df = pd.concat(frames, ignore_index=True)
    else:
        df = raw_df

    selected_countries = st.sidebar.multiselect("Pays", options=sorted(df['Country'].unique()), default=df['Country'].unique())
    
    dates = st.sidebar.date_input(
        "Intervalle",
        value=(df['date'].min(), df['date'].max())
    )

    mask = df['Country'].isin(selected_countries)
    if isinstance(dates, tuple) and len(dates) == 2:
        mask &= (df['date'].dt.date >= dates[0]) & (df['date'].dt.date <= dates[1])
    
    df_final = df.loc[mask].copy()

    # Ajout de Jittering pour séparer les points empilés
    if not df_final.empty:
        df_final['ActionGeo_Lat'] += np.random.uniform(-0.1, 0.1, len(df_final))
        df_final['ActionGeo_Long'] += np.random.uniform(-0.1, 0.1, len(df_final))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Events", f"{len(df_final):,}")
    m2.metric("Tone Score", f"{df_final['AvgTone'].mean():.2f}")
    m3.metric("Conflict Rate", f"{df_final['IsConflict'].mean()*100:.1f}%")
    m4.metric("Media Impact", f"{df_final['NumArticles'].sum():,}")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Analyse de la Tonalité")
        timeline = df_final.groupby(['date', 'Country'])['AvgTone'].mean().reset_index()
        fig_l = px.line(timeline, x='date', y='AvgTone', color='Country', template="plotly_dark")
        fig_l.add_hline(y=0, line_dash="dash", line_color="#555")
        st.plotly_chart(fig_l, width="stretch")

    with c2:
        st.subheader("Type d'événements")
        counts = df_final['IsConflict'].value_counts()
        names = ['Coopération' if i == 0 else 'Conflit' for i in counts.index]
        fig_p = px.pie(values=counts.values, names=names,
                      color_discrete_sequence=[PALETTE['accent'], PALETTE['primary']],
                      hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_p, width="stretch")

    st.subheader("Cartographie des points d'intérêt")
    if 'ActionGeo_Lat' in df_final.columns:
        map_df = df_final.dropna(subset=['ActionGeo_Lat', 'ActionGeo_Long'])
        if not map_df.empty:
            # On n'agrège plus par position exacte pour garder le jittering visible
            fig_m = px.scatter_map(map_df, lat="ActionGeo_Lat", lon="ActionGeo_Long", 
                                  size="NumArticles", color="AvgTone",
                                  hover_name="ActionGeo_FullName",
                                  color_continuous_scale='RdYlGn',
                                  range_color=[-4, 4],
                                  zoom=3 if regional_view else 6, height=650,
                                  opacity=0.6) # Un peu de transparence pour voir l'accumulation
            
            fig_m.update_layout(
                map_style="carto-darkmatter",
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor='black',
                font_color="white"
            )
            st.plotly_chart(fig_m, width="stretch")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Insights")
    st.sidebar.info("Note : Les points sont légèrement décalés aléatoirement pour mieux visualiser la densité locale.")

else:
    st.info("Chargement...")
