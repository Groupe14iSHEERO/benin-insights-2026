# Benin Insights Challenge — iSHEERO x DataCamp 2026

## Dashboard en ligne
> [Acceder au dashboard](URL_STREAMLIT_CLOUD)

## Mission
Analyser les donnees GDELT sur le Benin (12 mois de 2025) pour produire
des insights utiles aux journalistes, chercheurs et decideurs.

## Structure
```
benin-insights-2026/
├── dashboard/
│   └── app.py                    ← Application Streamlit
├── data/
│   ├── raw/                      ← Données brutes GDELT
│   └── processed/
│       ├── gdelt_benin_clean.csv ← Dataset nettoyé (8 000 événements)
│       ├── insights.json         ← 5 insights non-techniques
│       └── viz*.png              ← Visualisations générées
├── models/
│   └── models_bundle.pkl         ← K-Means + Random Forest + scalers
├── notebooks/
│   └── 01_DE_Pipeline.ipynb      ← Pipeline Données (DE)
│   └── 02_exploration.ipynb      ← EDA (DS+DA)
│   └── 03_ML_models.ipynb      ← Modèles ML (ME+DS)
│   └── 04_Prediction_Prospective_Benin.ipynb      ← Modele de prédiction (ME+DS)
├── requirements.txt
└── README.md
```

## Installation
```bash
git clone https://github.com/FidTCHANDO/benin-insights-2026
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Acces donnees GDELT
BigQuery : `gdelt-bq.gdeltv2.events` + `gdelt-bq.gdeltv2.gkg`
Filtre   : YEAR >= 2025 AND ActionGeo_CountryCode IN ('BN')

## Modeles ML
- PCA + K-Means clustering 
- Random Forest classification conflit/cooperation
- XGBOOST
- PERL, DBSCAN

## 5 Insights clés
1. 
2. 
3. 
4. 
5. 

## Equipe
| Role | Membre |
|------|--------|
| Data Engineer  | Ibrahim KONE |
| Data Analyst   | Georges AYENI |
| ML Engineer    | Sika Fidèle TCHANDO |
| Data Scientist | Léonel Junior Sêdjro VODOUNOU |

## Usage IA
Claude (Anthropic) utilisée pour la structure initiale.
Analyse, nettoyage et modelisation realises par l'équipe.