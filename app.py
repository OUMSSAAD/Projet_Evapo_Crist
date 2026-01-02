"""
Application Web - Évaporation et Cristallisation
Version Corporate Professionnelle
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
    page_title="Évaporation & Cristallisation Industrielle",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DESIGN CORPORATE PROFESSIONNEL ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* === PALETTE BLEUE PROFESSIONNELLE === */
    :root {
        /* Bleus corporates */
        --primary: #0A4B8F;
        --primary-light: #1565C0;
        --primary-dark: #073763;
        --primary-hover: #0D5CAB;
        
        /* Secondaires */
        --secondary: #1976D2;
        --accent: #2196F3;
        --info: #42A5F5;
        
        /* Neutres professionnels */
        --gray-50: #FAFAFA;
        --gray-100: #F5F5F5;
        --gray-200: #EEEEEE;
        --gray-300: #E0E0E0;
        --gray-400: #BDBDBD;
        --gray-500: #9E9E9E;
        --gray-600: #757575;
        --gray-700: #616161;
        --gray-800: #424242;
        --gray-900: #212121;
        
        --white: #FFFFFF;
        --black: #000000;
        
        /* États */
        --success: #2E7D32;
        --warning: #ED6C02;
        --error: #D32F2F;
    }
    
    /* === RESET GLOBAL === */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* === BACKGROUND === */
    .main {
        background: var(--gray-50);
    }
    
    .main .block-container {
        padding: 2.5rem 3rem;
        max-width: 1600px;
    }
    
    /* === TABS CORPORATE PROFESSIONNELLES === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 0;
        border-bottom: 2px solid var(--gray-200);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        border-radius: 0;
        font-weight: 700;
        font-size: 0.9375rem;
        color: var(--gray-600);
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary);
        border-bottom-color: var(--accent);
        background: var(--gray-50);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        background: var(--gray-50);
        border-bottom-color: var(--primary);
    }
    
    /* === HEADER PROFESSIONNEL === */
    .corporate-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        padding: 3rem 3.5rem;
        border-radius: 12px;
        margin-bottom: 3rem;
        box-shadow: 0 4px 20px rgba(10, 75, 143, 0.15);
        border-left: 4px solid var(--accent);
    }
    
    .corporate-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.75rem 0;
        letter-spacing: -0.02em;
    }
    
    .corporate-header .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.125rem;
        font-weight: 500;
        margin: 0;
        line-height: 1.6;
    }
    
    .header-meta {
        display: flex;
        gap: 2rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.9375rem;
        font-weight: 500;
    }
    
    .meta-label {
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
    }
    
    /* === SECTION HEADERS === */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 2rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid var(--primary);
    }
    
    .section-header h2 {
        color: var(--gray-900);
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .section-badge {
        background: var(--primary-light);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    
    /* === CARDS PROFESSIONNELLES === */
    .professional-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border-left: 3px solid transparent;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 24px rgba(10, 75, 143, 0.12);
        border-left-color: var(--primary);
        transform: translateY(-2px);
    }
    
    /* === METRIC CARDS === */
    .metric-corporate {
        background: linear-gradient(135deg, white 0%, var(--gray-50) 100%);
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 1.75rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .metric-corporate::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary) 0%, var(--accent) 100%);
    }
    
    .metric-corporate:hover {
        box-shadow: 0 8px 24px rgba(10, 75, 143, 0.15);
        transform: translateY(-3px);
    }
    
    .metric-label {
        font-size: 0.8125rem;
        font-weight: 700;
        color: var(--gray-600);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: var(--primary);
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .metric-unit {
        font-size: 0.9375rem;
        color: var(--gray-500);
        font-weight: 600;
        margin-top: 0.25rem;
    }
    
    .metric-change {
        font-size: 0.8125rem;
        color: var(--success);
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* === BUTTONS PROFESSIONNELS === */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9375rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(10, 75, 143, 0.2);
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover);
        box-shadow: 0 6px 20px rgba(10, 75, 143, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* === INPUTS PROFESSIONNELS === */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        border: 1.5px solid var(--gray-300);
        border-radius: 8px;
        font-size: 0.9375rem;
        font-weight: 500;
        color: var(--gray-900);
        transition: all 0.2s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(10, 75, 143, 0.1);
    }
    
    /* === SLIDER PROFESSIONNEL === */
    .stSlider > div > div > div {
        background: var(--primary);
    }
    
    .stSlider > div > div > div > div {
        background: white;
        border: 3px solid var(--primary);
        box-shadow: 0 2px 8px rgba(10, 75, 143, 0.2);
    }
    
    /* === ALERTS === */
    .alert-success {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 4px solid var(--success);
        padding: 1.25rem 1.5rem;
        border-radius: 8px;
        color: #1B5E20;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
    }
    
    .alert-info {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 4px solid var(--primary);
        padding: 1.25rem 1.5rem;
        border-radius: 8px;
        color: var(--primary-dark);
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(10, 75, 143, 0.1);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        border-left: 4px solid var(--warning);
        padding: 1.25rem 1.5rem;
        border-radius: 8px;
        color: #E65100;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(237, 108, 2, 0.1);
    }
    
    /* === DATAFRAME PROFESSIONNEL === */
    .dataframe {
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    /* === EXPANDER PROFESSIONNEL === */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid var(--gray-300);
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9375rem;
        color: var(--gray-900);
        padding: 1rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--gray-50);
        border-color: var(--primary);
    }
    
    /* === HEADERS === */
    h2 {
        color: var(--gray-900);
        font-size: 1.875rem;
        font-weight: 800;
        margin: 2.5rem 0 1.5rem 0;
        letter-spacing: -0.02em;
    }
    
    h3 {
        color: var(--primary);
        font-size: 1.375rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: var(--primary);
        height: 6px;
        border-radius: 10px;
    }
    
    /* === FOOTER PROFESSIONNEL === */
    .corporate-footer {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 2.5rem;
        margin-top: 4rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .corporate-footer p {
        color: var(--gray-600);
        font-size: 0.9375rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .corporate-footer strong {
        color: var(--primary);
        font-weight: 700;
    }
    

    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .corporate-header h1 {
            font-size: 1.75rem;
        }
        .metric-value {
            font-size: 1.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================

st.markdown("""
<div class="corporate-header">
    <h1>Système Industriel d'Évaporation & Cristallisation</h1>
    <p class="subtitle">
        Conception et simulation d'une unité intégrée de production de sucre cristallisé
    </p>
    <div class="header-meta">
        <div class="meta-item">
            <span class="meta-label">Université:</span> Hassan 1 - FST Settat
        </div>
        <div class="meta-item">
            <span class="meta-label">Filière:</span> PIC 2025-2026
        </div>
        <div class="meta-item">
            <span class="meta-label">Réalisé par:</span> OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== NAVIGATION TABS ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "TABLEAU DE BORD",
    "ÉVAPORATION", 
    "CRISTALLISATION",
    "OPTIMISATION",
    "CALCULATEURS"
])

# ==================== TABLEAU DE BORD ====================

with tab1:
    st.markdown("""
    <div class="corporate-header">
        <h1>Tableau de Bord</h1>
        <p class="subtitle">
            Vue d'ensemble du système intégré de production de sucre cristallisé
        </p>
        <div class="header-meta">
            <div class="meta-item">
                <span class="meta-label">Capacité:</span> 20 000 kg/h
            </div>
            <div class="meta-item">
                <span class="meta-label">Rendement:</span> 65% concentration
            </div>
            <div class="meta-item">
                <span class="meta-label">Efficacité:</span> 2.04 économie vapeur
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Production Annuelle", "43 000", "tonnes/an", "+12.5%", col1),
        ("Économie Vapeur", "2.04", "ratio", "+8.2%", col2),
        ("Retour Invest.", "0.08", "années", "-15.3%", col3),
        ("VAN Projet", "274", "M€", "+22.1%", col4)
    ]
    
    for label, value, unit, change, col in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-corporate">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-unit">{unit}</div>
                <div class="metric-change">{change}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Spécifications
    st.markdown('<div class="section-header"><h2>Spécifications Techniques</h2><span class="section-badge">SYSTÈME</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        
        specs = pd.DataFrame({
            'Paramètre': [
                'Débit alimentation',
                'Concentration entrée',
                'Concentration finale',
                'Température alimentation',
                'Pression vapeur',
                'Pression condenseur'
            ],
            'Valeur': [
                '20 000 kg/h',
                '15%',
                '65%',
                '85°C',
                '3.5 bar',
                '0.15 bar'
            ],
            'Statut': [
                'Optimal',
                'Conforme',
                'Cible',
                'Standard',
                'Nominal',
                'Minimum'
            ]
        })
        
        st.dataframe(specs, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown("### Indicateurs Clés")
        st.markdown("""
        - **Efficacité énergétique:** 87.3%
        - **Disponibilité système:** 96.5%
        - **Qualité produit:** 99.5%
        - **Taux utilisation:** 92.8%
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== ÉVAPORATION ====================

with tab2:
    st.markdown("""
    <div class="corporate-header">
        <h1>Module d'Évaporation</h1>
        <p class="subtitle">Simulation et dimensionnement d'évaporateurs à multiples effets</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("PARAMÈTRES DE SIMULATION", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n_effets = st.slider("Nombre d'effets", 2, 5, 3)
        with col2:
            P_vapeur = st.number_input("Pression vapeur (bar)", 2.0, 5.0, 3.5, 0.1)
        with col3:
            x_final = st.number_input("Concentration finale (%)", 50.0, 80.0, 65.0, 1.0)
        with col4:
            F_debit = st.number_input("Débit alimentation (kg/h)", 10000, 40000, 20000, 1000)
    
    if st.button("LANCER LA SIMULATION", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.P_vapeur = P_vapeur
                evap.x_final = x_final / 100
                evap.F = F_debit
                evap.resoudre_bilans()
                
                st.markdown('<div class="alert-success">✓ Simulation réussie - Résultats disponibles</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_data = [
                    ("Vapeur Chauffe", f"{evap.S:.0f}", "kg/h", col1),
                    ("Économie Vapeur", f"{evap.economie_vapeur():.2f}", "ratio", col2),
                    ("Surface Totale", f"{np.sum(evap.A):.0f}", "m²", col3),
                    ("Concentration", f"{evap.x[-1]*100:.1f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics_data:
                    with col:
                        st.markdown(f"""
                        <div class="metric-corporate">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau résultats
                st.markdown('<div class="section-header"><h2>Résultats par Effet</h2></div>', unsafe_allow_html=True)
                
                resultats = pd.DataFrame({
                    'Effet': range(1, n_effets + 1),
                    'Liquide (kg/h)': [f"{L:.0f}" for L in evap.L],
                    'Vapeur (kg/h)': [f"{V:.0f}" for V in evap.V],
                    'Concentration (%)': [f"{x*100:.1f}" for x in evap.x],
                    'Température (°C)': [f"{T:.1f}" for T in evap.T],
                    'Pression (bar)': [f"{P:.2f}" for P in evap.P],
                    'Surface (m²)': [f"{A:.1f}" for A in evap.A]
                })
                
                st.dataframe(resultats, use_container_width=True, hide_index=True)
                
                # Graphiques
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Profil de Température', 'Profil de Concentration', 
                                  'Profil de Pression', 'Surfaces d\'Échange'),
                    vertical_spacing=0.12
                )
                
                effets = list(range(1, n_effets + 1))
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             line=dict(color='#0A4B8F', width=3),
                             marker=dict(size=10, color='#0A4B8F', line=dict(color='white', width=2))),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             line=dict(color='#1976D2', width=3),
                             marker=dict(size=10, color='#1976D2', line=dict(color='white', width=2))),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             line=dict(color='#2196F3', width=3),
                             marker=dict(size=10, color='#2196F3', line=dict(color='white', width=2))),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A, marker=dict(color='#42A5F5', line=dict(color='#0A4B8F', width=1.5))),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Numéro d'Effet", showgrid=True, gridcolor='#F5F5F5')
                fig.update_yaxes(showgrid=True, gridcolor='#F5F5F5')
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12, color='#212121'),
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erreur lors de la simulation: {e}")

# ==================== CRISTALLISATION ====================

with tab3:
    st.markdown("""
    <div class="corporate-header">
        <h1>Module de Cristallisation</h1>
        <p class="subtitle">Simulation de cristallisation batch avec contrôle thermique</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("PARAMÈTRES DE SIMULATION", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            T_initial = st.number_input("Température initiale (°C)", 60.0, 80.0, 70.0, 1.0)
        with col2:
            T_final = st.number_input("Température finale (°C)", 25.0, 45.0, 35.0, 1.0)
        with col3:
            duree = st.number_input("Durée (heures)", 2.0, 8.0, 4.0, 0.5)
        with col4:
            profil = st.selectbox("Profil thermique", ["lineaire", "exponentiel", "optimal"])
    
    if st.button("LANCER LA SIMULATION ", use_container_width=True):
        with st.spinner("Simulation en cours..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                crist.simuler(profil=profil, n_points=500)
                
                st.markdown('<div class="alert-success">✓ Simulation terminée avec succès</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                
                metrics = [
                    ("Taille Moyenne Cristaux", f"{crist.L_50*1e6:.1f}", "µm", col1),
                    ("Coefficient Variation", f"{crist.CV:.1f}", "%", col2),
                    ("Concentration Finale", f"{crist.concentration[-1]:.2f}", "g/100g", col3)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-corporate">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Graphiques
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Évolution Température', 'Évolution Sursaturation',
                                  'Évolution Concentration', 'Évolution Population'),
                    vertical_spacing=0.12
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             line=dict(color='#0A4B8F', width=3)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             line=dict(color='#1976D2', width=3)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             line=dict(color='#2196F3', width=3)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             line=dict(color='#42A5F5', width=3)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (heures)", showgrid=True, gridcolor='#F5F5F5')
                fig.update_yaxes(showgrid=True, gridcolor='#F5F5F5')
                fig.update_yaxes(type="log", row=2, col=2)
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12, color='#212121')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Dimensionnement
                st.markdown('<div class="section-header"><h2>Dimensionnement Équipement</h2></div>', unsafe_allow_html=True)
                dims = crist.dimensionnement()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Volume Cristalliseur", f"{dims['volume']:.2f} m³")
                    st.metric("Diamètre", f"{dims['diametre']:.2f} m")
                with col2:
                    st.metric("Hauteur", f"{dims['hauteur']:.2f} m")
                    st.metric("Puissance Agitation", f"{dims['puissance_agitation']:.2f} kW")
                with col3:
                    st.metric("Surface Serpentin", f"{dims['surface_serpentin']:.2f} m²")
                
            except Exception as e:
                st.error(f"Erreur: {e}")

# ==================== OPTIMISATION ====================

with tab4:
    st.markdown("""
    <div class="corporate-header">
        <h1>Module d'Optimisation</h1>
        <p class="subtitle">Analyses de sensibilité et optimisation technico-économique</p>
    </div>
    """, unsafe_allow_html=True)
    
    analyse = st.selectbox(
        "Type d'analyse",
        ["Impact nombre d'effets", "Analyse économique comparative", 
         "Sensibilité pression vapeur", "Sensibilité concentration"]
    )
    
    if st.button("DÉMARRER L'ANALYSE", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            try:
                if analyse == "Impact nombre d'effets":
                    resultats = []
                    progress = st.progress(0)
                    
                    for idx, n in enumerate(range(2, 6)):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        resultats.append({
                            'Nombre Effets': n,
                            'Économie Vapeur': f"{evap.economie_vapeur():.2f}",
                            'Surface Totale (m²)': f"{np.sum(evap.A):.0f}",
                            'Vapeur Consommée (kg/h)': f"{evap.S:.0f}"
                        })
                        progress.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                
                elif analyse == "Analyse économique comparative":
                    eco = AnalyseEconomique()
                    resultats = []
                    progress = st.progress(0)
                    
                    for idx, n in enumerate([2, 3, 4, 5]):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        
                        crist_dims = {'volume': 3.85, 'puissance_agitation': 0.2, 'surface_serpentin': 3.73}
                        
                        TCI = eco.TCI(evap, crist_dims)
                        OPEX = eco.OPEX_annuel(evap, crist_dims)
                        production = evap.L[-1] * 8000 / 1000
                        cout = (OPEX['total'] + 0.03*TCI + TCI/15) / production
                        
                        resultats.append({
                            'Effets': n,
                            'TCI (M€)': f"{TCI/1e6:.2f}",
                            'OPEX (k€/an)': f"{OPEX['total']/1000:.0f}",
                            'Coût Production (€/t)': f"{cout:.2f}",
                            'Production (t/an)': f"{production:.0f}"
                        })
                        
                        progress.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    meilleur = df.loc[df['Coût Production (€/t)'].str.replace(',', '.').astype(float).idxmin()]
                    st.markdown(f"""
                    <div class="alert-info">
                        <strong>Configuration Optimale: {meilleur['Effets']} effets</strong><br>
                        Coût de production: {meilleur['Coût Production (€/t)']} €/tonne<br>
                        Investissement total: {meilleur['TCI (M€)']} M€
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="alert-success">✓ Analyse terminée avec succès</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur: {e}")

# ==================== CALCULATEURS ====================

with tab5:
    st.markdown("""
    <div class="corporate-header">
        <h1>Calculateurs Thermodynamiques</h1>
        <p class="subtitle">Outils de calcul pour propriétés physico-chimiques</p>
    </div>
    """, unsafe_allow_html=True)
    
    thermo = ProprietesThermodynamiques()
    
    calc = st.selectbox(
        "Type de calcul",
        ["Propriétés eau et vapeur", "Solubilité saccharose", 
         "Élévation point ébullition", "Économie vapeur"]
    )
    
    if calc == "Propriétés eau et vapeur":
        P = st.slider("Pression (bar)", 0.1, 10.0, 3.5, 0.1)
        
        if st.button("CALCULER LES PROPRIÉTÉS", use_container_width=True):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-corporate">
                    <div class="metric-label">Température Saturation</div>
                    <div class="metric-value">{T_sat:.2f}</div>
                    <div class="metric-unit">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-corporate">
                    <div class="metric-label">Chaleur Latente</div>
                    <div class="metric-value">{lambda_v/1e6:.2f}</div>
                    <div class="metric-unit">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calc == "Solubilité saccharose":
        T = st.slider("Température (°C)", 20, 90, 60)
        C_star = thermo.solubilite_saccharose(T)
        
        st.markdown(f"""
        <div class="metric-corporate">
            <div class="metric-label">Solubilité à {T}°C</div>
            <div class="metric-value">{C_star:.2f}</div>
            <div class="metric-unit">g saccharose / 100g solution</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Courbe
        T_range = np.linspace(20, 90, 100)
        C_range = [thermo.solubilite_saccharose(t) for t in T_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=T_range, y=C_range, mode='lines',
            line=dict(color='#0A4B8F', width=3),
            fill='tozeroy', fillcolor='rgba(10, 75, 143, 0.1)'
        ))
        fig.add_vline(x=T, line_dash="dash", line_color='#1976D2', line_width=2)
        
        fig.update_layout(
            xaxis_title="Température (°C)",
            yaxis_title="Solubilité (g/100g solution)",
            template='plotly_white',
            height=450,
            font=dict(family="Inter", size=12, color='#212121')
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER ====================

st.markdown("""
<div class="corporate-footer">
    <p style="font-size: 1.125rem; font-weight: 700; color: var(--primary); margin-bottom: 1rem;">
        SYSTÈME INDUSTRIEL D'ÉVAPORATION & CRISTALLISATION
    </p>
    <p>
        <strong>Université Hassan 1 - Faculté des Sciences et Techniques de Settat</strong><br>
        Filière Procédés et Ingénierie Chimique (PIC) | Année Universitaire 2025-2026
    </p>
    <p style="margin-top: 1.5rem;">
        <strong>Réalisé par:</strong> OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE
    </p>
    <p style="font-size: 0.875rem; color: var(--gray-500); margin-top: 1rem;">
        © 2025-2026 - Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)