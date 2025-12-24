"""
Application Web Streamlit - Évaporation et Cristallisation
Version Professionnelle avec Design Moderne
Auteur: Projet PIC 2025-2026
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import des modules du projet
from thermodynamique import ProprietesThermodynamiques
from evaporateurs import EvaporateurMultiplesEffets
from cristallisation import CristalliseurBatch
from optimisation import AnalyseSensibilite, AnalyseEconomique

# Configuration de la page
st.set_page_config(
    page_title="Évaporation & Cristallisation Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Style CSS professionnel
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #4ade80;
        --warning-color: #fbbf24;
        --error-color: #ef4444;
        --dark-bg: #1e293b;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
    }
    
    /* Reset et Base */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Container principal */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header professionnel */
    .pro-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .pro-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(10%, 10%); }
    }
    
    .pro-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .pro-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes modernes */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
    }
    
    .metric-card h3 {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-card .delta {
        font-size: 0.875rem;
        color: var(--success-color);
        margin-top: 0.25rem;
    }
    
    /* Onglets modernes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Boutons premium */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander élégant */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.05);
        border-color: var(--primary-color);
    }
    
    /* Messages */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid var(--success-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(74, 222, 128, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid var(--warning-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 4px solid #17a2b8;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.1);
    }
    
    /* Dataframe professionnel */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 8px;
    }
    
    /* Selectbox moderne */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Number input moderne */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid var(--border-color);
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Slider moderne */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Section headers */
    h2 {
        color: var(--text-primary);
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--primary-color);
    }
    
    h3 {
        color: var(--text-primary);
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Responsive mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .pro-header {
            padding: 2rem 1rem;
        }
        
        .pro-header h1 {
            font-size: 1.75rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1rem;
            font-size: 0.875rem;
        }
        
        .metric-card .value {
            font-size: 1.5rem;
        }
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card, .success-box, .warning-box, .info-box {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
        margin-top: 4rem;
    }
    
    .footer-gradient {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration matplotlib pour un style professionnel
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==================== HEADER ====================

st.markdown("""
<div class="pro-header">
    <h1>🏭 Évaporation & Cristallisation</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        Conception d'une Unité Intégrée de Production de Sucre
    </p>
    <p style="font-size: 0.95rem; opacity: 0.9; margin-top: 0.5rem;">
        Université Hassan 1 - FST Settat | Filière PIC 2025-2026
    </p>
    <p style="font-size: 0.95rem; opacity: 0.9; margin-top: 0.5rem;">
        Réalisé par : OUMSSAAD EL GHAZI |  KOLMAN GOD WIN TETE 
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== NAVIGATION ====================

tab_accueil, tab_evap, tab_crist, tab_optim, tab_calcul = st.tabs([
    "🏠 Accueil",
    "💧 Évaporation", 
    "💎 Cristallisation",
    "📊 Optimisation",
    "🧮 Calculateur"
])

# ==================== ONGLET ACCUEIL ====================

with tab_accueil:
    
    # Présentation en colonnes
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("## 📋 Présentation du Projet")
        
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 1rem 0;">
            <h3 style="color: #667eea; margin-top: 0;">🎯 Contexte Industriel</h3>
            <p style="line-height: 1.8; color: #64748b;">
                Conception d'une installation complète de production de sucre cristallisé 
                à partir de jus de canne à sucre. Le système intègre :
            </p>
            <ul style="line-height: 2; color: #475569;">
                <li>✅ <strong>Évaporation à multiples effets</strong> (2-5 effets)</li>
                <li>✅ <strong>Cristallisation batch</strong> avec contrôle de température</li>
                <li>✅ <strong>Récupération énergétique</strong> optimisée</li>
                <li>✅ <strong>Analyse technico-économique</strong> complète</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Spécifications Techniques")
        
        specs_data = {
            '⚙️ Paramètre': [
                'Débit alimentation',
                'Concentration entrée',
                'Concentration visée',
                'Température entrée',
                'Pression vapeur'
            ],
            '📈 Valeur': [
                '20 000 kg/h',
                '15 %',
                '65 %',
                '85 °C',
                '3.5 bar'
            ],
            '📌 Importance': [
                'Élevée',
                'Critique',
                'Critique',
                'Moyenne',
                'Élevée'
            ]
        }
        
        df_specs = pd.DataFrame(specs_data)
        st.dataframe(df_specs, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("""
        
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <h3 style="margin-top: 0;">✨ Fonctionnalités</h3>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Simulation en temps réel</li>
                <li>Graphiques interactifs</li>
                <li>Export des résultats</li>
                <li>Calculs personnalisés</li>
                <li>Analyses avancées</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques clés
        st.markdown("### 📈 Métriques Projet")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Production", "43k t/an", "+5%")
        with col_m2:
            st.metric("Économie", "2.04", "Excellent")
        
        col_m3, col_m4 = st.columns(2)
        with col_m3:
            st.metric("ROI", "0.08 ans", "Rapide")
        with col_m4:
            st.metric("VAN", "274 M€", "+12%")

# ==================== ONGLET ÉVAPORATION ====================

with tab_evap:
    st.markdown("## 💧 Évaporation à Multiples Effets")
    
    # Paramètres dans un expander élégant
    with st.expander("⚙️ Paramètres de Simulation", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n_effets = st.slider(
                "🔢 Nombre d'effets",
                min_value=2,
                max_value=5,
                value=3,
                help="Plus d'effets = meilleure économie d'énergie"
            )
        
        with col2:
            P_vapeur = st.number_input(
                "⚡ Pression vapeur (bar)",
                min_value=2.0,
                max_value=5.0,
                value=3.5,
                step=0.1
            )
        
        with col3:
            x_final = st.number_input(
                "🎯 Concentration finale (%)",
                min_value=50.0,
                max_value=80.0,
                value=65.0,
                step=1.0
            )
        
        with col4:
            F_debit = st.number_input(
                "💧 Débit alimentation (kg/h)",
                min_value=10000,
                max_value=40000,
                value=20000,
                step=1000
            )
    
    # Bouton de simulation avec style
    if st.button("▶️  Lancer la Simulation", type="primary", use_container_width=True):
        with st.spinner("⏳ Calcul en cours..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.P_vapeur = P_vapeur
                evap.x_final = x_final / 100
                evap.F = F_debit
                
                evap.resoudre_bilans()
                
                st.markdown('<div class="success-box">✅ <strong>Simulation réussie!</strong></div>', unsafe_allow_html=True)
                
                # Métriques dans des cartes élégantes
                st.markdown("### 📊 Résultats Clés")
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_data = [
                    ("🔥 Vapeur de chauffe", f"{evap.S:.0f}", "kg/h", col1),
                    ("♻️ Économie vapeur", f"{evap.economie_vapeur():.2f}", "ratio", col2),
                    ("📏 Surface totale", f"{np.sum(evap.A):.0f}", "m²", col3),
                    ("🎯 Concentration", f"{evap.x[-1]*100:.1f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics_data:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{label}</h3>
                            <div class="value">{value}</div>
                            <div style="color: #64748b; font-size: 0.875rem;">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau détaillé avec style
                st.markdown("### 📋 Détails par Effet")
                
                resultats = pd.DataFrame({
                    ' Effet': range(1, n_effets + 1),
                    ' Liquide (kg/h)': [f"{L:.0f}" for L in evap.L],
                    ' Vapeur (kg/h)': [f"{V:.0f}" for V in evap.V],
                    ' Concentration (%)': [f"{x*100:.1f}" for x in evap.x],
                    ' Température (°C)': [f"{T:.1f}" for T in evap.T],
                    ' Pression (bar)': [f"{P:.2f}" for P in evap.P],
                    ' Surface (m²)': [f"{A:.1f}" for A in evap.A]
                })
                
                st.dataframe(resultats, use_container_width=True, hide_index=True)
                
                # Graphiques avec Plotly pour l'interactivité
                st.markdown("### 📈 Visualisations")
                
                fig = go.Figure()
                
                # Créer les subplots
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=(' Température', ' Concentration', 
                                  ' Pression', ' Surfaces d\'échange'),
                    specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                           [{'type': 'scatter'}, {'type': 'bar'}]]
                )
                
                effets = list(range(1, n_effets + 1))
                
                # Température
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             name='Température', line=dict(color='#ef4444', width=3),
                             marker=dict(size=10)),
                    row=1, col=1
                )
                
                # Concentration
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             name='Concentration', line=dict(color='#22c55e', width=3),
                             marker=dict(size=10, symbol='square')),
                    row=1, col=2
                )
                
                # Pression
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             name='Pression', line=dict(color='#3b82f6', width=3),
                             marker=dict(size=10, symbol='diamond')),
                    row=2, col=1
                )
                
                # Surfaces
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A, name='Surface',
                          marker=dict(color='#f59e0b')),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Effet", row=1, col=1)
                fig.update_xaxes(title_text="Effet", row=1, col=2)
                fig.update_xaxes(title_text="Effet", row=2, col=1)
                fig.update_xaxes(title_text="Effet", row=2, col=2)
                
                fig.update_yaxes(title_text="T (°C)", row=1, col=1)
                fig.update_yaxes(title_text="C (%)", row=1, col=2)
                fig.update_yaxes(title_text="P (bar)", row=2, col=1)
                fig.update_yaxes(title_text="A (m²)", row=2, col=2)
                
                fig.update_layout(height=700, showlegend=False, 
                                template='plotly_white',
                                font=dict(family="Inter"))
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== ONGLET CRISTALLISATION ====================

with tab_crist:
    st.markdown("## 💎 Cristallisation Batch")
    
    with st.expander("⚙️ Paramètres de Cristallisation", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            T_initial = st.number_input(
                "🌡️ T initiale (°C)",
                min_value=60.0,
                max_value=80.0,
                value=70.0,
                step=1.0
            )
        
        with col2:
            T_final = st.number_input(
                "❄️ T finale (°C)",
                min_value=25.0,
                max_value=45.0,
                value=35.0,
                step=1.0
            )
        
        with col3:
            duree = st.number_input(
                "⏱️ Durée (heures)",
                min_value=2.0,
                max_value=8.0,
                value=4.0,
                step=0.5
            )
        
        with col4:
            profil = st.selectbox(
                "📉 Profil refroidissement",
                ["lineaire", "exponentiel", "optimal"],
                help="Optimal maintient une sursaturation constante"
            )
    
    if st.button("▶️  Simuler Cristallisation", type="primary", use_container_width=True):
        with st.spinner("⏳ Simulation en cours..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                
                crist.simuler(profil=profil, n_points=500)
                
                st.markdown('<div class="success-box">✅ <strong>Simulation terminée!</strong></div>', unsafe_allow_html=True)
                
                # Métriques
                st.markdown("### 📊 Résultats Clés")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>💎 Taille Moyenne</h3>
                        <div class="value">{crist.L_50*1e6:.1f}</div>
                        <div style="color: #64748b; font-size: 0.875rem;">µm</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 Coeff. Variation</h3>
                        <div class="value">{crist.CV:.1f}</div>
                        <div style="color: #64748b; font-size: 0.875rem;">%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🎯 Concentration</h3>
                        <div class="value">{crist.concentration[-1]:.2f}</div>
                        <div style="color: #64748b; font-size: 0.875rem;">g/100g</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Graphiques Plotly
                st.markdown("### 📈 Évolution")
                
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('🌡️ Température', '📊 Sursaturation', 
                                  '💧 Concentration', '📈 Population'),
                    specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                           [{'type': 'scatter'}, {'type': 'scatter'}]]
                )
                
                # Température
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             name='Température', line=dict(color='#ef4444', width=2)),
                    row=1, col=1
                )
                
                # Sursaturation
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             name='Sursaturation', line=dict(color='#3b82f6', width=2)),
                    row=1, col=2
                )
                fig.add_hline(y=0.02, line_dash="dash", line_color="green",
                             annotation_text="Zone métastable", row=1, col=2)
                
                # Concentration
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             name='Concentration', line=dict(color='#22c55e', width=2)),
                    row=2, col=1
                )
                
                # Population
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             name='m₀', line=dict(color='#f59e0b', width=2)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (h)", row=1, col=1)
                fig.update_xaxes(title_text="Temps (h)", row=1, col=2)
                fig.update_xaxes(title_text="Temps (h)", row=2, col=1)
                fig.update_xaxes(title_text="Temps (h)", row=2, col=2)
                
                fig.update_yaxes(title_text="T (°C)", row=1, col=1)
                fig.update_yaxes(title_text="S", row=1, col=2)
                fig.update_yaxes(title_text="C (g/100g)", row=2, col=1)
                fig.update_yaxes(title_text="Nombre", row=2, col=2, type="log")
                
                fig.update_layout(height=700, showlegend=False,
                                template='plotly_white',
                                font=dict(family="Inter"))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Dimensionnement
                st.markdown("### 📐 Dimensionnement")
                dims = crist.dimensionnement()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Volume", f"{dims['volume']:.2f} m³")
                    st.metric("Diamètre", f"{dims['diametre']:.2f} m")
                
                with col2:
                    st.metric("Hauteur", f"{dims['hauteur']:.2f} m")
                    st.metric("Puissance agitation", f"{dims['puissance_agitation']:.2f} kW")
                
                with col3:
                    st.metric("Surface serpentin", f"{dims['surface_serpentin']:.2f} m²")
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== ONGLET OPTIMISATION ====================

with tab_optim:
    st.markdown("## 📊 Analyse d'Optimisation")
    
    analyse_type = st.selectbox(
        "🎯 Type d'analyse",
        [
            "Impact du nombre d'effets",
            "Analyse économique",
            "Sensibilité - Pression vapeur",
            "Sensibilité - Concentration"
        ]
    )
    
    if st.button("▶️  Lancer l'Analyse", type="primary", use_container_width=True):
        with st.spinner("⏳ Analyse en cours..."):
            try:
                if analyse_type == "Impact du nombre d'effets":
                    st.markdown("### 🔬 Impact du Nombre d'Effets")
                    
                    resultats = []
                    progress_bar = st.progress(0)
                    
                    for idx, n in enumerate(range(2, 6)):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        resultats.append({
                            'Effets': n,
                            'Économie vapeur': evap.economie_vapeur(),
                            'Surface (m²)': np.sum(evap.A),
                            'Vapeur (kg/h)': evap.S
                        })
                        progress_bar.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    
                    # Tableau stylisé
                    st.dataframe(
                        df.style.format({
                            'Économie vapeur': '{:.3f}',
                            'Surface (m²)': '{:.1f}',
                            'Vapeur (kg/h)': '{:.0f}'
                        }).background_gradient(cmap='RdYlGn', subset=['Économie vapeur']),
                        use_container_width=True, 
                        hide_index=True
                    )
                    
                    # Graphiques Plotly
                    fig = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=('Économie de vapeur', 'Surface totale', 'Consommation vapeur')
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Économie vapeur'], 
                                 mode='lines+markers',
                                 line=dict(color='#667eea', width=3),
                                 marker=dict(size=12)),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Surface (m²)'], 
                                 mode='lines+markers',
                                 line=dict(color='#22c55e', width=3),
                                 marker=dict(size=12)),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Vapeur (kg/h)'], 
                                 mode='lines+markers',
                                 line=dict(color='#ef4444', width=3),
                                 marker=dict(size=12)),
                        row=1, col=3
                    )
                    
                    fig.update_xaxes(title_text="Nombre d'effets")
                    fig.update_yaxes(title_text="Économie", row=1, col=1)
                    fig.update_yaxes(title_text="Surface (m²)", row=1, col=2)
                    fig.update_yaxes(title_text="Vapeur (kg/h)", row=1, col=3)
                    
                    fig.update_layout(height=400, showlegend=False,
                                    template='plotly_white')
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif analyse_type == "Sensibilité - Pression vapeur":
                    st.markdown("### 🔬 Sensibilité à la Pression de Vapeur")
                    
                    P_range = np.linspace(2.5, 4.5, 15)
                    economies = []
                    surfaces = []
                    temperatures = []
                    
                    progress_bar = st.progress(0)
                    for idx, P in enumerate(P_range):
                        evap = EvaporateurMultiplesEffets(n_effets=3)
                        evap.P_vapeur = P
                        evap.resoudre_bilans()
                        
                        economies.append(evap.economie_vapeur())
                        surfaces.append(np.sum(evap.A))
                        temperatures.append(evap.T[0])
                        
                        progress_bar.progress((idx + 1) / len(P_range))
                    
                    df = pd.DataFrame({
                        'Pression (bar)': P_range,
                        'Économie': economies,
                        'Surface (m²)': surfaces,
                        'T (°C)': temperatures
                    })
                    
                    st.dataframe(
                        df.style.format({
                            'Pression (bar)': '{:.2f}',
                            'Économie': '{:.3f}',
                            'Surface (m²)': '{:.1f}',
                            'T (°C)': '{:.1f}'
                        }).background_gradient(cmap='coolwarm'),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Graphiques
                    fig = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=('Impact sur l\'économie', 'Impact sur les surfaces', 
                                      'Impact sur la température')
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=P_range, y=economies, mode='lines',
                                 fill='tozeroy', line=dict(color='#3b82f6', width=3)),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=P_range, y=surfaces, mode='lines',
                                 fill='tozeroy', line=dict(color='#22c55e', width=3)),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=P_range, y=temperatures, mode='lines',
                                 fill='tozeroy', line=dict(color='#ef4444', width=3)),
                        row=1, col=3
                    )
                    
                    fig.update_xaxes(title_text="Pression (bar)")
                    fig.update_layout(height=400, showlegend=False, template='plotly_white')
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif analyse_type == "Sensibilité - Concentration":
                    st.markdown("### 🔬 Sensibilité à la Concentration Finale")
                    
                    x_range = np.linspace(60, 70, 10)
                    vapeurs_totales = []
                    surfaces = []
                    vapeurs_chauffe = []
                    
                    progress_bar = st.progress(0)
                    for idx, x_final in enumerate(x_range):
                        evap = EvaporateurMultiplesEffets(n_effets=3)
                        evap.x_final = x_final / 100
                        evap.resoudre_bilans()
                        
                        vapeurs_totales.append(np.sum(evap.V))
                        surfaces.append(np.sum(evap.A))
                        vapeurs_chauffe.append(evap.S)
                        
                        progress_bar.progress((idx + 1) / len(x_range))
                    
                    df = pd.DataFrame({
                        'Concentration (%)': x_range,
                        'Vapeur totale (kg/h)': vapeurs_totales,
                        'Surface (m²)': surfaces,
                        'Vapeur chauffe (kg/h)': vapeurs_chauffe
                    })
                    
                    st.dataframe(
                        df.style.format({
                            'Concentration (%)': '{:.1f}',
                            'Vapeur totale (kg/h)': '{:.0f}',
                            'Surface (m²)': '{:.1f}',
                            'Vapeur chauffe (kg/h)': '{:.0f}'
                        }).background_gradient(cmap='viridis'),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Graphiques
                    fig = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=('Production de vapeur', 'Surfaces d\'échange', 
                                      'Consommation de vapeur')
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=x_range, y=vapeurs_totales, mode='lines+markers',
                                 line=dict(color='#3b82f6', width=3),
                                 marker=dict(size=10)),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=x_range, y=surfaces, mode='lines+markers',
                                 line=dict(color='#22c55e', width=3),
                                 marker=dict(size=10)),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=x_range, y=vapeurs_chauffe, mode='lines+markers',
                                 line=dict(color='#ef4444', width=3),
                                 marker=dict(size=10)),
                        row=1, col=3
                    )
                    
                    fig.update_xaxes(title_text="Concentration (%)")
                    fig.update_layout(height=400, showlegend=False, template='plotly_white')
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif analyse_type == "Analyse économique":
                    st.markdown("### 💰 Analyse Économique")
                    
                    eco = AnalyseEconomique()
                    resultats = []
                    
                    progress_bar = st.progress(0)
                    for idx, n in enumerate([2, 3, 4, 5]):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        
                        crist = CristalliseurBatch()
                        crist_dims = {
                            'volume': 3.85,
                            'puissance_agitation': 0.2,
                            'surface_serpentin': 3.73
                        }
                        
                        TCI = eco.TCI(evap, crist_dims)
                        OPEX = eco.OPEX_annuel(evap, crist_dims)
                        production = evap.L[-1] * 8000 / 1000
                        cout_unit = (OPEX['total'] + 0.03*TCI + TCI/15) / production
                        
                        resultats.append({
                            'Effets': n,
                            'TCI (M€)': TCI/1e6,
                            'OPEX (k€/an)': OPEX['total']/1000,
                            'Coût (€/t)': cout_unit,
                            'Production (t/an)': production
                        })
                        
                        progress_bar.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    
                    st.dataframe(
                        df.style.format({
                            'TCI (M€)': '{:.2f}',
                            'OPEX (k€/an)': '{:.0f}',
                            'Coût (€/t)': '{:.2f}',
                            'Production (t/an)': '{:.0f}'
                        }).background_gradient(cmap='RdYlGn_r', subset=['Coût (€/t)']),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    meilleur = df.loc[df['Coût (€/t)'].idxmin()]
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="margin-top: 0;">✅ Configuration Optimale: {int(meilleur['Effets'])} effets</h3>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            <li><strong>Coût production:</strong> {meilleur['Coût (€/t)']:.2f} €/tonne</li>
                            <li><strong>Investissement:</strong> {meilleur['TCI (M€)']:.2f} M€</li>
                            <li><strong>Production:</strong> {meilleur['Production (t/an)']:.0f} t/an</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="success-box">✅ <strong>Analyse terminée!</strong></div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== ONGLET CALCULATEUR ====================

with tab_calcul:
    st.markdown("## 🧮 Calculateur Rapide")
    
    calcul_type = st.selectbox(
        "🎯 Type de calcul",
        [
            "Propriétés thermodynamiques",
            "Solubilité saccharose",
            "EPE (Élévation Point Ébullition)",
            "Économie de vapeur"
        ]
    )
    
    thermo = ProprietesThermodynamiques()
    
    if calcul_type == "Propriétés thermodynamiques":
        st.markdown("### 💧 Propriétés de l'Eau/Vapeur")
        
        P = st.slider("Pression (bar)", 0.1, 10.0, 3.5, 0.1)
        
        if st.button("🔍 Calculer", use_container_width=True):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🌡️ Température Saturation</h3>
                    <div class="value">{T_sat:.2f}</div>
                    <div style="color: #64748b; font-size: 0.875rem;">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔥 Chaleur Latente</h3>
                    <div class="value">{lambda_v/1e6:.2f}</div>
                    <div style="color: #64748b; font-size: 0.875rem;">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calcul_type == "Solubilité saccharose":
        st.markdown("### 🍬 Solubilité du Saccharose")
        
        T = st.slider("Température (°C)", 20, 90, 60)
        
        C_star = thermo.solubilite_saccharose(T)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>💎 Solubilité à {T}°C</h3>
            <div class="value">{C_star:.2f}</div>
            <div style="color: #64748b; font-size: 0.875rem;">g saccharose / 100g solution</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Courbe avec Plotly
        T_range = np.linspace(20, 90, 100)
        C_range = [thermo.solubilite_saccharose(t) for t in T_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=T_range, y=C_range, mode='lines',
                               line=dict(color='#667eea', width=3),
                               fill='tozeroy'))
        fig.add_vline(x=T, line_dash="dash", line_color="red",
                     annotation_text=f"T = {T}°C")
        fig.add_hline(y=C_star, line_dash="dash", line_color="red", opacity=0.5)
        
        fig.update_layout(
            title="Courbe de Solubilité du Saccharose",
            xaxis_title="Température (°C)",
            yaxis_title="Solubilité (g/100g)",
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif calcul_type == "EPE (Élévation Point Ébullition)":
        st.markdown("### 📈 Élévation du Point d'Ébullition")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x = st.slider("Concentration (%)", 0, 80, 50)
        
        with col2:
            P = st.number_input("Pression (bar)", 0.1, 5.0, 1.0, 0.1, key="epe_p")
        
        EPE = thermo.EPE_saccharose(x)
        T_sat = thermo.temperature_saturation(P)
        T_eb = T_sat + EPE
        
        col1, col2, col3 = st.columns(3)
        
        metrics = [
            ("📊 EPE", f"{EPE:.2f}", "°C", col1),
            ("💧 T ébullition eau pure", f"{T_sat:.2f}", "°C", col2),
            ("🍬 T ébullition solution", f"{T_eb:.2f}", "°C", col3)
        ]
        
        for label, value, unit, col in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{label}</h3>
                    <div class="value">{value}</div>
                    <div style="color: #64748b; font-size: 0.875rem;">{unit}</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calcul_type == "Économie de vapeur":
        st.markdown("### 💨 Économie de Vapeur")
        
        n = st.slider("Nombre d'effets", 1, 5, 3)
        
        E_theorique = n * 0.95
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>♻️ Économie Théorique avec {n} effet(s)</h3>
            <div class="value">{E_theorique:.2f}</div>
            <div style="color: #64748b; font-size: 0.875rem;">kg vapeur produite / kg vapeur consommée</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Graphique
        effets = list(range(1, 6))
        economies = [e * 0.95 for e in effets]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=effets, y=economies,
                           marker=dict(color=economies,
                                     colorscale='Blues',
                                     showscale=False)))
        fig.add_hline(y=E_theorique, line_dash="dash", line_color="red",
                     annotation_text=f"{n} effet(s)")
        
        fig.update_layout(
            title="Économie de Vapeur Théorique",
            xaxis_title="Nombre d'effets",
            yaxis_title="Économie de vapeur",
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER ====================

st.markdown("""
<div class="footer-gradient">
    <div style="text-align: center;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">
            🏭 Application Évaporation & Cristallisation
        </h3>
        <p style="color: #64748b; margin: 0.5rem 0;">
            <strong>Université Hassan 1 - FST Settat</strong><br>
            Filière Procédés et Ingénierie Chimique (PIC) | Année 2025-2026
        </p>
        
</div>
""", unsafe_allow_html=True)