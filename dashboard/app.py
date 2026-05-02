"""
🇧🇯 Bénin Insights Challenge 2026
iSHEERO × DataCamp Donates
Dashboard Streamlit — app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import json, pickle, warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇧🇯 Bénin Insights 2026",
    page_icon="🇧🇯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────────────
C = {
    "primary":   "#E91E8C",
    "secondary": "#7B2FBE",
    "accent":    "#00D4AA",
    "dark":      "#1A1A2E",
}
PAL = ["#E91E8C","#7B2FBE","#00D4AA","#FF6B35","#4ECDC4","#45B7D1","#96CEB4","#FFEAA7"]

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#FAFAFA",
    "axes.grid":        True,
    "grid.alpha":       0.2,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "font.size":        10,
})

# ─────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#FAFAFA}
[data-testid="stSidebar"]{background:#1A1A2E}
[data-testid="stSidebar"] *{color:#FFF !important}
div[data-testid="metric-container"]{
    background:white;border-radius:12px;padding:16px;
    box-shadow:0 2px 8px rgba(0,0,0,.07);border-top:4px solid #E91E8C}
div[data-testid="metric-container"] label{color:#888 !important;font-size:.78rem !important;text-transform:uppercase}
div[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#E91E8C !important;font-size:1.8rem !important;font-weight:900}
.hero{background:linear-gradient(135deg,#1A1A2E 0%,#7B2FBE 60%,#E91E8C 100%);
      border-radius:16px;padding:36px 40px;color:white;margin-bottom:24px}
.hero h1{font-size:2.2rem;font-weight:900;margin:0}
.hero p{margin:6px 0 0;opacity:.85}
.insight-card{background:white;border-left:5px solid #E91E8C;border-radius:0 12px 12px 0;
              padding:18px 22px;margin:10px 0;box-shadow:0 2px 8px rgba(0,0,0,.07)}
.ins-title{font-weight:700;color:#1A1A2E;margin-bottom:6px}
.ins-body{color:#555;font-size:.9rem;line-height:1.55}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# CHEMINS
# ─────────────────────────────────────────────────────────────────────
BASE      = Path(__file__).parent.parent
DATA_PROC = BASE / "data" / "processed"
MODELS    = BASE / "models"

# ─────────────────────────────────────────────────────────────────────
# CHARGEMENT DONNÉES
# ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv = DATA_PROC / "gdelt_benin_clean.csv"
    if csv.exists():
        return pd.read_csv(csv, parse_dates=["date"])
    st.error("❌ Fichier CSV non trouvé. Exécutez d'abord le notebook.")
    st.stop()

@st.cache_data
def load_insights():
    p = DATA_PROC / "insights.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

@st.cache_resource
def load_models():
    p = MODELS / "models_bundle.pkl"
    if p.exists():
        return pickle.load(open(p, "rb"))
    return None

df_all   = load_data()
insights = load_insights()
bundle   = load_models()

# ─────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTRES
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇧🇯 Bénin Insights 2026")
    st.markdown("---")

    d_min = df_all["date"].min().date()
    d_max = df_all["date"].max().date()
    dr = st.date_input("📅 Période", value=(d_min, d_max),
                       min_value=d_min, max_value=d_max)

    quad_opts = sorted(df_all["QuadLabel"].dropna().unique())
    quads = st.multiselect("🏷️ Type d'événement", quad_opts, default=quad_opts)

    ville_opts = sorted(df_all["ActionGeo_FullName"].unique())
    villes = st.multiselect("📍 Villes", ville_opts, default=ville_opts)

    theme_opts = sorted(df_all["CameoTheme"].unique())
    themes = st.multiselect("🔖 Thèmes CAMEO", theme_opts, default=theme_opts)

    st.markdown("---")
    st.caption(f"Source : GDELT v2")
    st.caption(f"MAJ : {datetime.now().strftime('%d/%m/%Y')}")
    st.caption("iSHEERO × DataCamp 2026")

# ─────────────────────────────────────────────────────────────────────
# FILTRE
# ─────────────────────────────────────────────────────────────────────
if len(dr) == 2:
    mask = (
        (df_all["date"].dt.date >= dr[0]) &
        (df_all["date"].dt.date <= dr[1]) &
        df_all["QuadLabel"].isin(quads) &
        df_all["ActionGeo_FullName"].isin(villes) &
        df_all["CameoTheme"].isin(themes)
    )
    df = df_all[mask].copy()
else:
    df = df_all.copy()

# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🇧🇯 Bénin Insights Challenge 2026</h1>
  <p>Analyse GDELT — Pipeline complet sur les événements médiatiques du Bénin</p>
  <p style="opacity:.6;font-size:.85rem">iSHEERO × DataCamp Donates &nbsp;|&nbsp; Source : GDELT v2</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("📊 Événements",   f"{len(df):,}")
k2.metric("🌡️ Tone moyen",   f"{df['AvgTone'].mean():.2f}")
k3.metric("⚔️ Conflictuels", f"{(df['QuadClass']>=3).mean()*100:.1f}%")
k4.metric("📍 Villes",       df["ActionGeo_FullName"].nunique())
k5.metric("📰 Sources",      df["SourceDomain"].nunique() if "SourceDomain" in df else "—")
k6.metric("📅 Jours couverts", (df["date"].max()-df["date"].min()).days)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "📈 Temporel", "🗺️ Carte", "🏷️ Thèmes & Acteurs",
    "🤖 Machine Learning", "💡 Insights", "📋 Données"
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — TEMPOREL
# ══════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Évolution temporelle de l'activité médiatique")

    df_wk = df.groupby(df["date"].dt.to_period("W")).agg(
        nb=("EventCode","count"), tone=("AvgTone","mean")
    ).reset_index()
    df_wk["date"] = df_wk["date"].dt.start_time

    fig, axes = plt.subplots(2,1, figsize=(13,6), sharex=True)
    fig.suptitle("Volume & Tonalité hebdomadaires", fontsize=13, fontweight="bold")

    axes[0].fill_between(df_wk["date"], df_wk["nb"], alpha=.3, color=C["primary"])
    axes[0].plot(df_wk["date"], df_wk["nb"], color=C["primary"], lw=2.5)
    axes[0].set_ylabel("Événements / semaine")

    clrs = [C["accent"] if t>=0 else C["primary"] for t in df_wk["tone"]]
    axes[1].bar(df_wk["date"], df_wk["tone"], width=5, color=clrs, alpha=.8)
    axes[1].axhline(0, color="black", lw=.8, ls="--")
    axes[1].set_ylabel("Tone moyen")
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    # Mensuel
    st.markdown("#### Volume mensuel par type d'événement")
    mo = df.groupby(["month_label","QuadLabel"]).size().reset_index(name="count")
    order = df.groupby("month_label")["date"].min().sort_values().index.tolist()
    mo["month_label"] = pd.Categorical(mo["month_label"], categories=order, ordered=True)
    mo = mo.sort_values("month_label")

    fig2, ax2 = plt.subplots(figsize=(13,4))
    quads_uniq = mo["QuadLabel"].unique()
    pivot = mo.pivot_table(index="month_label", columns="QuadLabel",
                           values="count", aggfunc="sum", fill_value=0)
    pivot.plot(kind="bar", stacked=True, ax=ax2,
               color=PAL[:len(pivot.columns)], edgecolor="white", width=.8)
    ax2.set_xlabel(""); ax2.set_ylabel("Événements")
    ax2.legend(loc="upper left", fontsize=8)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig2); plt.close()

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — CARTE
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Géographie des événements au Bénin")

    geo = df.groupby("ActionGeo_FullName").agg(
        count=("EventCode","count"), tone=("AvgTone","mean"),
        gold=("GoldsteinScale","mean"),
        lat=("ActionGeo_Lat","mean"), lon=("ActionGeo_Long","mean")
    ).reset_index()

    ca, cb = st.columns([2,1])
    with ca:
        fig3, ax3 = plt.subplots(figsize=(8,11))
        fig3.patch.set_facecolor("#D6EAF8")
        ax3.set_facecolor("#D6EAF8")
        sc = ax3.scatter(
            geo["lon"], geo["lat"],
            s=geo["count"]*2, c=geo["tone"],
            cmap="RdYlGn", vmin=-5, vmax=5,
            alpha=.85, edgecolors="white", linewidths=1.5, zorder=3
        )
        plt.colorbar(sc, ax=ax3, label="Tone moyen", shrink=.6)
        for _, row in geo.iterrows():
            ax3.annotate(
                f"{row['ActionGeo_FullName']}\n({int(row['count'])})",
                (row["lon"], row["lat"]),
                textcoords="offset points", xytext=(7,4),
                fontsize=8, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=.75, edgecolor="none")
            )
        ax3.set_title("Événements par ville\n(taille=volume · couleur=tonalité)",
                      fontsize=12, fontweight="bold")
        ax3.set_xlim(1.0, 4.0); ax3.set_ylim(5.5, 13.0)
        ax3.set_xlabel("Longitude"); ax3.set_ylabel("Latitude")
        ax3.grid(alpha=.3, color="white")
        plt.tight_layout()
        st.pyplot(fig3); plt.close()

    with cb:
        st.markdown("#### Classement des villes")
        top_geo = geo.sort_values("count", ascending=False)
        for _, row in top_geo.iterrows():
            tc = C["accent"] if row["tone"] >= 0 else C["primary"]
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        padding:7px 0;border-bottom:1px solid #EEE">
              <span style="font-weight:600;font-size:.9rem">{row["ActionGeo_FullName"]}</span>
              <span style="color:{tc};font-weight:800">{int(row["count"])}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Score Goldstein moyen")
        top_gold = geo.sort_values("gold", ascending=False)
        for _, row in top_gold.iterrows():
            gc = C["accent"] if row["gold"] >= 0 else C["primary"]
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid #EEE">
              <span style="font-size:.85rem">{row["ActionGeo_FullName"]}</span>
              <span style="color:{gc};font-weight:700">{row["gold"]:.1f}</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — THÈMES & ACTEURS
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Analyse thématique et des acteurs")

    ta, tb = st.columns(2)
    with ta:
        tc_data = df["CameoTheme"].value_counts().head(12)
        fig4, ax4 = plt.subplots(figsize=(7,5))
        ax4.barh(tc_data.index[::-1], tc_data.values[::-1],
                 color=PAL[:len(tc_data)], edgecolor="white", height=.7)
        ax4.set_xlabel("Nombre d'événements")
        ax4.set_title("Top 12 Thèmes CAMEO", fontweight="bold")
        for i, v in enumerate(tc_data.values[::-1]):
            ax4.text(v+10, i, f"{v:,}", va="center", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig4); plt.close()

    with tb:
        qc_data = df["QuadLabel"].value_counts()
        fig5, ax5 = plt.subplots(figsize=(7,5))
        wedges, texts, autotexts = ax5.pie(
            qc_data.values, labels=qc_data.index,
            colors=PAL[:len(qc_data)],
            autopct="%1.1f%%", startangle=90,
            explode=[0.05]*len(qc_data)
        )
        for at in autotexts: at.set_fontsize(8)
        ax5.set_title("Répartition QuadClass", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig5); plt.close()

    # Acteurs + Sources
    st.markdown("---")
    tc2, td2 = st.columns(2)
    with tc2:
        a1 = df["Actor1Name"].value_counts().head(10)
        fig6, ax6 = plt.subplots(figsize=(7,5))
        ax6.barh(a1.index[::-1], a1.values[::-1], color=C["secondary"], alpha=.85)
        ax6.set_title("Top acteurs initiateurs", fontweight="bold")
        ax6.set_xlabel("Événements")
        plt.tight_layout()
        st.pyplot(fig6); plt.close()

    with td2:
        if "SourceDomain" in df.columns:
            src = df.groupby("SourceDomain").agg(
                nb=("EventCode","count"), tone=("AvgTone","mean")
            ).sort_values("nb", ascending=False).head(10)
            fig7, ax7 = plt.subplots(figsize=(7,5))
            clrs7 = [C["accent"] if t>=0 else C["primary"] for t in src["tone"].values[::-1]]
            ax7.barh(src.index[::-1], src["tone"].values[::-1], color=clrs7, alpha=.85)
            ax7.axvline(0, color="black", lw=.8, ls="--")
            ax7.set_title("Biais tonalité par source", fontweight="bold")
            ax7.set_xlabel("Tone moyen")
            plt.tight_layout()
            st.pyplot(fig7); plt.close()

# ══════════════════════════════════════════════════════════════════════
# TAB 4 — MACHINE LEARNING
# ══════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🤖 Résultats Machine Learning")

    if bundle:
        best_k = bundle["best_k"]
        report = bundle["report"]
        profile_d = bundle["profile"]
        sil = bundle.get("sil_scores", {})

        st.success(f"✅ Modèles chargés depuis models/models_bundle.pkl")

        ma, mb = st.columns(2)
        with ma:
            st.markdown(f"### K-Means — k optimal = {best_k}")
            if sil:
                fig8, axes8 = plt.subplots(1,1, figsize=(6,3.5))
                axes8.plot(list(sil.keys()), list(sil.values()),
                          "o-", color=C["primary"], lw=2.5, ms=8)
                axes8.axvline(best_k, ls="--", color=C["accent"],
                             label=f"k={best_k}")
                axes8.set_xlabel("k"); axes8.set_ylabel("Silhouette")
                axes8.set_title("Score Silhouette vs k")
                axes8.legend()
                plt.tight_layout()
                st.pyplot(fig8); plt.close()

            st.markdown("**Profil des clusters :**")
            profile_df = pd.DataFrame({
                "Cluster": list(profile_d["Événements"].keys()),
                "Événements": list(profile_d["Événements"].values()),
                "Tone moyen": [f"{v:.2f}" for v in profile_d["Tone_moyen"].values()],
                "Goldstein": [f"{v:.2f}" for v in profile_d["Goldstein_moy"].values()],
                "Thème top": list(profile_d["Thème_top"].values()),
                "Ville top": list(profile_d["Ville_top"].values()),
            })
            st.dataframe(profile_df, use_container_width=True, hide_index=True)

        with mb:
            st.markdown("### Random Forest — Conflit vs Coopération")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Accuracy",       f"{report['accuracy']:.2%}")
            mc2.metric("F1 Coopération", f"{report['Coopération']['f1-score']:.2%}")
            mc3.metric("F1 Conflit",     f"{report['Conflit']['f1-score']:.2%}")

            rf_table = pd.DataFrame({
                "Classe": ["Coopération","Conflit"],
                "Précision": [f"{report['Coopération']['precision']:.2%}",
                              f"{report['Conflit']['precision']:.2%}"],
                "Rappel": [f"{report['Coopération']['recall']:.2%}",
                           f"{report['Conflit']['recall']:.2%}"],
                "F1": [f"{report['Coopération']['f1-score']:.2%}",
                       f"{report['Conflit']['f1-score']:.2%}"],
                "Support": [int(report['Coopération']['support']),
                            int(report['Conflit']['support'])],
            })
            st.dataframe(rf_table, use_container_width=True, hide_index=True)

        # PCA scatter
        if "PCA1" in df_all.columns and "Cluster" in df_all.columns:
            st.markdown("---")
            st.markdown("### Clustering PCA 2D")
            samp = df_all.sample(min(2000, len(df_all)), random_state=42)
            fig9, ax9 = plt.subplots(figsize=(10,6))
            for i, c in enumerate(sorted(samp["Cluster"].dropna().unique())):
                mask9 = samp["Cluster"] == c
                ax9.scatter(samp.loc[mask9,"PCA1"], samp.loc[mask9,"PCA2"],
                           s=12, alpha=.45, color=PAL[i], label=f"Cluster {int(c)}")
            ax9.set_title(f"K-Means k={best_k} — PCA 2D", fontweight="bold")
            ax9.set_xlabel("PC1"); ax9.set_ylabel("PC2")
            ax9.legend()
            plt.tight_layout()
            st.pyplot(fig9); plt.close()
    else:
        st.warning("⚠️ Modèles non trouvés. Exécutez d'abord le notebook.")
        st.code("cd notebooks\njupyter notebook Benin_Insights.ipynb")

# ══════════════════════════════════════════════════════════════════════
# TAB 5 — INSIGHTS
# ══════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("💡 5 Insights Clés — Résumé non-technique")
    st.markdown("Pour journalistes, chercheurs et décideurs politiques.")
    st.markdown("<br>", unsafe_allow_html=True)

    if insights:
        for k, ins in insights.items():
            st.markdown(f"""
            <div class="insight-card">
              <div class="ins-title">{ins.get('icon','💡')} &nbsp; #{k} — {ins['title']}</div>
              <div class="ins-body">{ins['body']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Insights non disponibles. Exécutez le notebook.")

    # Sentiment chart
    st.markdown("<br>#### Distribution du sentiment", unsafe_allow_html=True)
    if "ToneCategory" in df.columns:
        sent = df["ToneCategory"].value_counts()
        fig10, ax10 = plt.subplots(figsize=(9,4))
        bars10 = ax10.bar(sent.index, sent.values,
                         color=[C["primary"],C["secondary"],"#888",C["accent"],"#006D5B"][:len(sent)],
                         edgecolor="white", width=.7)
        for bar in bars10:
            ax10.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
                     f"{int(bar.get_height()):,}", ha="center", fontsize=9)
        ax10.set_ylabel("Nombre d'événements")
        ax10.set_title("Répartition du sentiment", fontweight="bold")
        plt.setp(ax10.get_xticklabels(), rotation=20, ha="right")
        plt.tight_layout()
        st.pyplot(fig10); plt.close()

    # Goldstein par région source
    if "SourceRegion" in df.columns:
        st.markdown("#### Goldstein par région de source médiatique")
        gr = df.groupby("SourceRegion")["GoldsteinScale"].mean().sort_values()
        fig11, ax11 = plt.subplots(figsize=(7,3))
        clrs11 = [C["accent"] if v>=0 else C["primary"] for v in gr.values]
        ax11.barh(gr.index, gr.values, color=clrs11, alpha=.85)
        ax11.axvline(0, color="black", lw=.8, ls="--")
        ax11.set_xlabel("Goldstein moyen")
        ax11.set_title("Biais médiatique par région", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig11); plt.close()

# ══════════════════════════════════════════════════════════════════════
# TAB 6 — DONNÉES
# ══════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("📋 Données brutes filtrées")

    display_cols = ["date","ActionGeo_FullName","EventLabel","QuadLabel",
                    "CameoTheme","Actor1Name","AvgTone","GoldsteinScale",
                    "NumMentions","ToneCategory","SourceDomain"]
    available = [c for c in display_cols if c in df.columns]

    st.markdown(f"**{len(df):,} lignes** correspondant aux filtres actifs.")

    # Recherche texte
    search = st.text_input("🔍 Rechercher dans Actor1Name ou EventLabel", "")
    df_disp = df[available].copy()
    if search:
        mask_s = (
            df_disp.get("Actor1Name", pd.Series([""])*len(df_disp))
                   .str.contains(search, case=False, na=False) |
            df_disp.get("EventLabel", pd.Series([""])*len(df_disp))
                   .str.contains(search, case=False, na=False)
        )
        df_disp = df_disp[mask_s]

    st.dataframe(df_disp.sort_values("date", ascending=False).head(500),
                 use_container_width=True, height=450)

    csv_dl = df[available].to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Télécharger CSV (filtré)",
        data=csv_dl,
        file_name=f"benin_insights_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<p style="text-align:center;color:#AAA;font-size:.8rem">
  🇧🇯 <b>Bénin Insights Challenge 2026</b> — iSHEERO × DataCamp Donates<br>
  Source : GDELT v2 &nbsp;|&nbsp; IA utilisée : Claude (Anthropic)
</p>
""", unsafe_allow_html=True)