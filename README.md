# Benin Insights Challenge — iSHEERO x DataCamp 2026

## Dashboard en ligne
> [Acceder au dashboard](URL_STREAMLIT_CLOUD)

## Mission
Analyser les donnees GDELT sur le Benin (12 mois de 2025) pour produire
des insights utiles aux journalistes, chercheurs et decideurs.

## Structure
```
data/raw/monthly/          # Events GDELT par mois (Parquet)
data/processed/            # Donnees nettoyees + visualisations
models/rf_classifier.pkl   # Modele Random Forest
dashboard/app.py           # Application Streamlit
requirements.txt
README.md
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

## 5 Insights cles
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