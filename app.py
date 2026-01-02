"""
Application Web - Évaporation et Cristallisation
Version Ultra-Premium - Style Moderne Élégant
Université Hassan 1 - FST Settat | PIC 2025-2026
Réalisé par: OUMSSAAD EL GHAZI | KOLMAN GOD WIN TETE
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import des modules
from thermodynamique import ProprietesThermodynamiques
from evaporateurs import EvaporateurMultiplesEffets
from cristallisation import CristalliseurBatch
from optimisation import AnalyseEconomique

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="Évaporation & Cristallisation Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DESIGN MODERNE ÉLÉGANT ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* === PALETTE MODERNE ÉLÉGANTE === */
    :root {
        /* Couleurs principales - Ton sombre et élégant */
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #0f3460;
        --highlight: #e94560;
        
        /* Couleurs vives */
        --cyan: #00d9ff;
        --orange: #ff6b35;
        --purple: #a855f7;
        --green: #22c55e;
        
        /* Neutres élégants */
        --white: #ffffff;
        --light: #f8fafc;
        --gray: #94a3b8;
        --dark: #0f172a;
        
        /* Effets */
        --glow-cyan: rgba(0, 217, 255, 0.5);
        --glow-pink: rgba(233, 69, 96, 0.5);
    }
    
    /* === RESET GLOBAL === */
    * {
        font-family: 'Poppins', -apple-system, sans-serif;
    }
    
    /* === BACKGROUND === */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        background: transparent;
    }
    
    /* === HEADER MODERNE === */
    .modern-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
        padding: 4rem 3rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    
    .modern-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, var(--glow-cyan) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .modern-header::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: -20%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, var(--glow-pink) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite reverse;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    .modern-header h1 {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 30px var(--glow-cyan);
        letter-spacing: -0.02em;
    }
    
    .modern-header .subtitle {
        font-size: 1.125rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 1rem;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    .modern-badge {
        display: inline-block;
        background: rgba(0, 217, 255, 0.15);
        border: 1px solid var(--cyan);
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--cyan);
        margin-top: 1.5rem;
        margin-right: 0.75rem;
        position: relative;
        z-index: 1;
        box-shadow: 0 0 20px var(--glow-cyan);
    }
    
    /* === TABS MODERNES === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
        color: var(--gray);
        background: transparent;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 217, 255, 0.1);
        color: var(--cyan);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
        color: white;
        box-shadow: 0 10px 30px var(--glow-cyan);
    }
    
    /* === CARDS MODERNES === */
    .modern-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--cyan) 0%, var(--purple) 50%, var(--highlight) 100%);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-8px);
        border-color: rgba(0, 217, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 217, 255, 0.2);
    }
    
    .modern-card:hover::before {
        transform: scaleX(1);
    }
    
    /* === METRIC CARDS === */
    .metric-modern {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .metric-modern::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, var(--cyan), transparent 30%);
        animation: rotate 4s linear infinite;
        opacity: 0.1;
    }
    
    .metric-modern::after {
        content: '';
        position: absolute;
        inset: 1px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border-radius: 17px;
        z-index: 0;
    }
    
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }
    
    .metric-modern:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 217, 255, 0.3);
        border-color: var(--cyan);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 40px var(--glow-cyan);
    }
    
    .metric-unit {
        font-size: 0.875rem;
        color: var(--gray);
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* === BUTTONS MODERNES === */
    .stButton > button {
        background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 14px;
        font-weight: 800;
        font-size: 1.0625rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px var(--glow-cyan);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.5s, height 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 60px var(--glow-cyan), 0 0 40px var(--glow-pink);
    }
    
    .stButton > button:hover::before {
        width: 400px;
        height: 400px;
    }
    
    /* === INPUTS MODERNES === */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stSlider {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 20px var(--glow-cyan) !important;
    }
    
    /* === ALERTS === */
    .alert-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 2px solid var(--green);
        padding: 1.5rem;
        border-radius: 16px;
        color: var(--green);
        font-weight: 700;
        box-shadow: 0 10px 40px rgba(34, 197, 94, 0.2);
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 2px solid var(--cyan);
        padding: 1.5rem;
        border-radius: 16px;
        color: var(--cyan);
        font-weight: 700;
        box-shadow: 0 10px 40px var(--glow-cyan);
    }
    
    /* === DATAFRAME === */
    .dataframe {
        background: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.3);
        border-radius: 14px;
        font-weight: 700;
        color: var(--cyan);
        padding: 1.25rem 1.5rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 217, 255, 0.1);
        box-shadow: 0 0 30px var(--glow-cyan);
    }
    
    /* === HEADERS === */
    h2 {
        font-size: 2rem;
        font-weight: 900;
        color: white;
        margin: 3rem 0 1.5rem 0;
        text-shadow: 0 0 20px var(--glow-cyan);
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--cyan);
        margin: 2rem 0 1rem 0;
    }
    
    /* === FOOTER === */
    .modern-footer {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 3rem;
        margin-top: 4rem;
        text-align: center;
    }
    
    .modern-footer p {
        color: var(--gray);
        font-size: 1rem;
        margin: 0.75rem 0;
    }
    
    .modern-footer strong {
        background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--cyan) 0%, var(--purple) 100%);
        height: 8px;
        border-radius: 10px;
        box-shadow: 0 0 20px var(--glow-cyan);
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .modern-header h1 {
            font-size: 2rem;
        }
        .metric-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================

st.markdown("""
<div class="modern-header">
    <h1>🏭 ÉVAPORATION & CRISTALLISATION</h1>
    <div class="subtitle">
        Conception Avancée d'une Unité Intégrée de Production de Sucre
    </div>
    <span class="modern-badge">Université Hassan 1 - FST Settat</span>
    <span class="modern-badge">PIC 2025-2026</span>
    <span class="modern-badge">OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE</span>
</div>
""", unsafe_allow_html=True)

# ==================== NAVIGATION ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 ACCUEIL",
    "💧 ÉVAPORATION", 
    "💎 CRISTALLISATION",
    "📊 OPTIMISATION",
    "🧮 CALCULATEUR"
])

# ==================== ACCUEIL ====================

with tab1:
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("## 📋 PRÉSENTATION")
        
        st.markdown("""
        <div class="modern-card">
            <h3 style="color: var(--cyan); margin-top: 0;">🎯 CONTEXTE INDUSTRIEL</h3>
            <p style="line-height: 2; color: var(--gray); font-size: 1.0625rem;">
                Application de <strong style="color: white;">simulation avancée</strong> pour la conception d'une unité 
                complète de production de sucre cristallisé à partir de jus de canne à sucre.
            </p>
            <p style="line-height: 2; color: white; font-weight: 600; margin-top: 1.5rem;">
                ⚡ FONCTIONNALITÉS :
            </p>
            <ul style="line-height: 2.5; color: var(--gray); font-size: 1rem; list-style: none; padding-left: 0;">
                <li>✅ Évaporation à multiples effets (2-5 configurations)</li>
                <li>✅ Cristallisation batch avec contrôle thermique avancé</li>
                <li>✅ Optimisation énergétique et récupération de chaleur</li>
                <li>✅ Analyse technico-économique complète</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 SPÉCIFICATIONS")
        
        specs = pd.DataFrame({
            'Paramètre': [
                'Débit alimentation',
                'Concentration entrée',
                'Concentration visée',
                'Température entrée',
                'Pression vapeur'
            ],
            'Valeur': [
                '20 000 kg/h',
                '15 %',
                '65 %',
                '85 °C',
                '3.5 bar'
            ]
        })
        
        st.dataframe(specs, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📈 MÉTRIQUES")
        
        metrics = [
            ("PRODUCTION", "43", "kt/an"),
            ("ÉCONOMIE", "2.04", "ratio"),
            ("ROI", "0.08", "ans"),
            ("VAN", "274", "M€")
        ]
        
        for label, value, unit in metrics:
            st.markdown(f"""
            <div class="metric-modern">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== ÉVAPORATION ====================

with tab2:
    st.markdown("## 💧 SIMULATION ÉVAPORATION")
    
    with st.expander("⚙️ PARAMÈTRES", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n_effets = st.slider("Effets", 2, 5, 3)
        with col2:
            P_vapeur = st.number_input("Pression (bar)", 2.0, 5.0, 3.5, 0.1)
        with col3:
            x_final = st.number_input("Concentration (%)", 50.0, 80.0, 65.0, 1.0)
        with col4:
            F_debit = st.number_input("Débit (kg/h)", 10000, 40000, 20000, 1000)
    
    if st.button("▶️ LANCER", use_container_width=True):
        with st.spinner("⏳ Calcul..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.P_vapeur = P_vapeur
                evap.x_final = x_final / 100
                evap.F = F_debit
                evap.resoudre_bilans()
                
                st.markdown('<div class="alert-success">✓ SIMULATION RÉUSSIE</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_data = [
                    ("VAPEUR", f"{evap.S:.0f}", "kg/h", col1),
                    ("ÉCONOMIE", f"{evap.economie_vapeur():.2f}", "ratio", col2),
                    ("SURFACE", f"{np.sum(evap.A):.0f}", "m²", col3),
                    ("CONCENTRATION", f"{evap.x[-1]*100:.1f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics_data:
                    with col:
                        st.markdown(f"""
                        <div class="metric-modern">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau
                resultats = pd.DataFrame({
                    'Effet': range(1, n_effets + 1),
                    'L (kg/h)': [f"{L:.0f}" for L in evap.L],
                    'V (kg/h)': [f"{V:.0f}" for V in evap.V],
                    'x (%)': [f"{x*100:.1f}" for x in evap.x],
                    'T (°C)': [f"{T:.1f}" for T in evap.T],
                    'P (bar)': [f"{P:.2f}" for P in evap.P],
                    'A (m²)': [f"{A:.1f}" for A in evap.A]
                })
                
                st.dataframe(resultats, use_container_width=True, hide_index=True)
                
                # Graphiques
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Température', 'Concentration', 'Pression', 'Surface'),
                    vertical_spacing=0.15
                )
                
                effets = list(range(1, n_effets + 1))
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             line=dict(color='#00d9ff', width=3),
                             marker=dict(size=12, color='#00d9ff', line=dict(color='white', width=2))),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             line=dict(color='#a855f7', width=3),
                             marker=dict(size=12, color='#a855f7', line=dict(color='white', width=2))),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             line=dict(color='#ff6b35', width=3),
                             marker=dict(size=12, color='#ff6b35', line=dict(color='white', width=2))),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A, marker=dict(color='#22c55e', line=dict(color='#00d9ff', width=2))),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Effet", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                
                fig.update_layout(
                    height=700,
                    showlegend=False,
                    template='plotly_dark',
                    font=dict(family="Poppins", size=13, color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(15, 23, 42, 0.6)',
                    margin=dict(t=50, b=40, l=40, r=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== CRISTALLISATION ====================

with tab3:
    st.markdown("## 💎 CRISTALLISATION BATCH")
    
    with st.expander("⚙️ PARAMÈTRES", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            T_initial = st.number_input("T initiale (°C)", 60.0, 80.0, 70.0, 1.0)
        with col2:
            T_final = st.number_input("T finale (°C)", 25.0, 45.0, 35.0, 1.0)
        with col3:
            duree = st.number_input("Durée (h)", 2.0, 8.0, 4.0, 0.5)
        with col4:
            profil = st.selectbox("Profil", ["lineaire", "exponentiel", "optimal"])
    
    if st.button("▶️ SIMULER", use_container_width=True, key="crist"):
        with st.spinner("⏳ Simulation..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                crist.simuler(profil=profil, n_points=500)
                
                st.markdown('<div class="alert-success">✓ SIMULATION TERMINÉE</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                
                metrics = [
                    ("TAILLE", f"{crist.L_50*1e6:.1f}", "µm", col1),
                    ("CV", f"{crist.CV:.1f}", "%", col2),
                    ("CONCENTRATION", f"{crist.concentration[-1]:.2f}", "g/100g", col3)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-modern">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Graphiques
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('🌡️ Température', '📊 Sursaturation', '💧 Concentration', '📈 Population'),
                    vertical_spacing=0.15
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             line=dict(color='#e94560', width=3)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             line=dict(color='#00d9ff', width=3)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             line=dict(color='#22c55e', width=3)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             line=dict(color='#a855f7', width=3)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (h)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                fig.update_yaxes(type="log", row=2, col=2)
                
                fig.update_layout(
                    height=700,
                    showlegend=False,
                    template='plotly_dark',
                    font=dict(family="Poppins", size=13, color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(15, 23, 42, 0.6)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== OPTIMISATION ====================

with tab4:
    st.markdown("## 📊 ANALYSE D'OPTIMISATION")
    
    analyse = st.selectbox(
        "Type d'analyse",
        ["Impact nombre d'effets", "Analyse économique"]
    )
    
    if st.button("▶️ ANALYSER", use_container_width=True):
        with st.spinner("⏳ Analyse..."):
            try:
                if analyse == "Impact nombre d'effets":
                    resultats = []
                    progress = st.progress(0)
                    
                    for idx, n in enumerate(range(2, 6)):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        resultats.append({
                            'Effets': n,
                            'Économie': evap.economie_vapeur(),
                            'Surface': np.sum(evap.A),
                            'Vapeur': evap.S
                        })
                        progress.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown('<div class="alert-success">✓ ANALYSE TERMINÉE</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== CALCULATEUR ====================

with tab5:
    st.markdown("## 🧮 CALCULATEURS")
    
    thermo = ProprietesThermodynamiques()
    
    calc = st.selectbox("Type", ["Propriétés eau/vapeur", "Solubilité"])
    
    if calc == "Propriétés eau/vapeur":
        P = st.slider("Pression (bar)", 0.1, 10.0, 3.5, 0.1)
        
        if st.button("🔍 CALCULER", use_container_width=True):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-modern">
                    <div class="metric-label">TEMPÉRATURE</div>
                    <div class="metric-value">{T_sat:.2f}</div>
                    <div class="metric-unit">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-modern">
                    <div class="metric-label">CHALEUR LATENTE</div>
                    <div class="metric-value">{lambda_v/1e6:.2f}</div>
                    <div class="metric-unit">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)

# ==================== FOOTER ====================

st.markdown("""
<div class="modern-footer">
    <p style="font-size: 1.25rem; font-weight: 800; margin-bottom: 1rem;">
        <strong>🏭 ÉVAPORATION & CRISTALLISATION</strong>
    </p>
    <p>
        <strong>Université Hassan 1 - FST Settat</strong><br>
        Filière PIC 2025-2026
    </p>
    <p style="margin-top: 1.5rem;">
        <strong>Réalisé par:</strong> OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE
    </p>
</div>
""", unsafe_allow_html=True)