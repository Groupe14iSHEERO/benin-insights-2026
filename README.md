# 🌍 Bénin Insights Challenge 2026
**Observatoire Régional de Veille Stratégique (GDELT)**

Ce projet a été développé dans le cadre du hackathon *Bénin Insights Challenge 2026*. Il s'agit d'un dashboard interactif permettant d'analyser les dynamiques géopolitiques, les conflits et la tonalité médiatique au Bénin et dans la sous-région ouest-africaine.

## 🚀 Fonctionnalités Clés
- **Données Réelles** : Analyse de +30 000 événements GDELT (Jan 2025 - Avr 2026).
- **Ingestion Live** : Bouton de capture en temps réel des dernières 15 minutes d'actualité mondiale (API GDELT 2.0).
- **Cartographie Dynamique** : Visualisation de la densité des événements avec correction par jittering.
- **Extension Régionale** : Démonstration de scalabilité sur toute la zone CEDEAO.

## 🛠️ Installation et Lancement

1. **Cloner le projet** :
   ```bash
   git clone <url-du-repo>
   cd benin-insights-2026
   ```

2. **Installer les dépendances** :
   *(Il est recommandé d'utiliser un environnement virtuel)*
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer le Dashboard** :
   ```bash
   streamlit run dashboard/app.py
   ```

## 📊 Interprétation des Données (Insights)

D'après nos analyses sur le dataset actuel :

1. **Hypercentralisation mériatique** : La ville de **Cotonou** concentre près de 60% de la visibilité médiatique du pays. Cela souligne un besoin de décentralisation de la veille pour couvrir les zones frontalières plus sensibles.
2. **Stabilité Tonalité** : Malgré des pics de tension isolés, la tonalité moyenne au Bénin reste relativement stable autour de `-0.20`, indiquant une résilience médiatique face aux crises régionales.
3. **Corrélation Conflit/Impact** : Les événements classés comme "Conflits" génèrent en moyenne **2.5x plus d'articles** que les actions de coopération, confirmant le biais traditionnel des médias pour les crises.

## 📡 Sources
Les données proviennent du projet **GDELT (Global Database of Events, Language, and Tone)**.

---
*Réalisé pour le Bénin Insights Challenge 2026.*
