"""
Application Scientifique - Évaporation et Cristallisation
Style MATLAB/Scientifique Professionnel
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
    page_title="Simulation Évaporation-Cristallisation",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE SCIENTIFIQUE MATLAB ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500;600&display=swap');
    
    /* === VARIABLES SCIENTIFIQUES === */
    :root {
        /* Couleurs académiques */
        --primary-blue: #1565C0;
        --primary-dark: #0D47A1;
        --accent-blue: #1976D2;
        --light-blue: #42A5F5;
        
        /* Gris techniques */
        --gray-bg: #F5F5F5;
        --gray-panel: #FAFAFA;
        --gray-border: #D0D0D0;
        --gray-sidebar: #E8E8E8;
        --gray-text: #212121;
        --gray-label: #616161;
        
        /* États */
        --success: #2E7D32;
        --warning: #F57C00;
        --error: #C62828;
        --info: #0277BD;
    }
    
    /* === RESET === */
    * {
        font-family: 'Roboto', -apple-system, sans-serif;
    }
    
    /* === BACKGROUND === */
    .main {
        background: var(--gray-bg);
    }
    
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1800px;
    }
    
    /* === SIDEBAR MATLAB === */
    [data-testid="stSidebar"] {
        background: var(--gray-sidebar);
        border-right: 2px solid var(--gray-border);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    /* Logo sidebar */
    .sidebar-logo {
        background: var(--primary-blue);
        padding: 1.25rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-logo h3 {
        color: white;
        font-size: 1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Navigation items */
    .nav-section {
        margin: 1.5rem 0;
    }
    
    .nav-title {
        color: var(--gray-label);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        padding: 0 0.75rem;
    }
    
    .nav-item {
        padding: 0.625rem 0.75rem;
        margin: 0.25rem 0;
        border-radius: 3px;
        cursor: pointer;
        transition: all 0.15s ease;
        font-size: 0.875rem;
        color: var(--gray-text);
        border-left: 3px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(21, 101, 192, 0.08);
        border-left-color: var(--primary-blue);
    }
    
    .nav-item.active {
        background: rgba(21, 101, 192, 0.12);
        border-left-color: var(--primary-blue);
        font-weight: 500;
        color: var(--primary-dark);
    }
    
    /* === HEADER === */
    .main-header {
        background: white;
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--primary-blue);
    }
    
    .main-header h1 {
        color: var(--gray-text);
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .main-header p {
        color: var(--gray-label);
        font-size: 0.875rem;
        margin: 0;
    }
    
    /* === PANEL SCIENTIFIQUE === */
    .sci-panel {
        background: white;
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    
    .sci-panel-header {
        background: var(--gray-panel);
        border: 1px solid var(--gray-border);
        border-bottom: 2px solid var(--primary-blue);
        padding: 0.75rem 1rem;
        margin: -1.25rem -1.25rem 1rem -1.25rem;
        border-radius: 4px 4px 0 0;
    }
    
    .sci-panel-header h3 {
        color: var(--gray-text);
        font-size: 0.875rem;
        font-weight: 700;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* === INPUTS SCIENTIFIQUES === */
    .input-group {
        margin-bottom: 1rem;
    }
    
    .input-label {
        display: block;
        color: var(--gray-text);
        font-size: 0.8125rem;
        font-weight: 500;
        margin-bottom: 0.375rem;
    }
    
    .input-unit {
        color: var(--gray-label);
        font-weight: 400;
        margin-left: 0.25rem;
    }
    
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stSlider {
        border: 1px solid var(--gray-border) !important;
        border-radius: 3px !important;
        background: white !important;
        font-family: 'Roboto Mono', monospace !important;
        font-size: 0.875rem !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 2px rgba(21, 101, 192, 0.1) !important;
    }
    
    /* === BOUTON CALCULER === */
    .stButton > button {
        background: var(--primary-blue) !important;
        color: white !important;
        border: none !important;
        padding: 0.625rem 1.5rem !important;
        border-radius: 3px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin-top: 0.5rem !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        box-shadow: 0 2px 8px rgba(21, 101, 192, 0.3) !important;
    }
    
    /* === ZONE RÉSULTATS === */
    .results-panel {
        background: var(--gray-panel);
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    
    .result-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary-blue);
    }
    
    .result-unit {
        font-family: 'Roboto', sans-serif;
        font-size: 0.8125rem;
        color: var(--gray-label);
        margin-left: 0.25rem;
    }
    
    /* === TABLEAUX SCIENTIFIQUES === */
    .sci-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.8125rem;
    }
    
    .sci-table th {
        background: var(--gray-panel);
        border: 1px solid var(--gray-border);
        padding: 0.625rem 0.75rem;
        text-align: left;
        font-weight: 600;
        color: var(--gray-text);
    }
    
    .sci-table td {
        border: 1px solid var(--gray-border);
        padding: 0.5rem 0.75rem;
        font-family: 'Roboto Mono', monospace;
        color: var(--gray-text);
    }
    
    .sci-table tr:nth-child(even) {
        background: rgba(0, 0, 0, 0.02);
    }
    
    /* Dataframe Streamlit */
    .dataframe {
        font-size: 0.8125rem !important;
        border: 1px solid var(--gray-border) !important;
    }
    
    .dataframe th {
        background: var(--gray-panel) !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        font-family: 'Roboto Mono', monospace !important;
    }
    
    /* === MÉTRIQUES === */
    .metric-sci {
        background: white;
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-sci-label {
        font-size: 0.75rem;
        color: var(--gray-label);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-sci-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary-blue);
        line-height: 1;
    }
    
    .metric-sci-unit {
        font-size: 0.875rem;
        color: var(--gray-label);
        margin-top: 0.25rem;
    }
    
    /* === ALERTS === */
    .alert-sci {
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 0.875rem 1rem;
        margin: 1rem 0;
        font-size: 0.875rem;
    }
    
    .alert-success {
        background: #E8F5E9;
        border-left: 4px solid var(--success);
        color: #1B5E20;
    }
    
    .alert-info {
        background: #E3F2FD;
        border-left: 4px solid var(--info);
        color: #01579B;
    }
    
    .alert-warning {
        background: #FFF3E0;
        border-left: 4px solid var(--warning);
        color: #E65100;
    }
    
    /* === GRAPHIQUES === */
    .plot-container {
        background: white;
        border: 1px solid var(--gray-border);
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* === TABS (cachées) === */
    .stTabs {
        display: none;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: var(--primary-blue) !important;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: var(--gray-panel);
        border: 1px solid var(--gray-border);
        border-radius: 3px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.25rem;
        }
        .metric-sci-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h3>🔬 Simulation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nav-title">Modules</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Évaporation", "Cristallisation", "Optimisation", "Calculateurs", "Documentation"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 1rem 0.75rem; font-size: 0.75rem; color: #616161;">
        <p style="margin: 0.25rem 0;"><strong>Projet:</strong> PIC 2025-2026</p>
        <p style="margin: 0.25rem 0;"><strong>Établissement:</strong> FST Settat</p>
        <p style="margin: 0.25rem 0; margin-top: 0.75rem;"><strong>Étudiants:</strong></p>
        <p style="margin: 0.25rem 0;">• OUMSSAAD EL GHAZI</p>
        <p style="margin: 0.25rem 0;">• KOLMAN GOD WIN TETE</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MODULE ÉVAPORATION ====================

if page == "Évaporation":
    st.markdown("""
    <div class="main-header">
        <h1>Évaporation à Multiples Effets</h1>
        <p>Simulation et dimensionnement d'évaporateurs industriels</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Panel Paramètres
    st.markdown("""
    <div class="sci-panel">
        <div class="sci-panel-header">
            <h3>⚙ Paramètres d'Entrée</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label">Débit d\'alimentation <span class="input-unit">(kg/h)</span></div>', unsafe_allow_html=True)
        F_debit = st.number_input("Débit", 5000, 50000, 20000, 1000, label_visibility="collapsed", key="F")
        
        st.markdown('<div class="input-label">Concentration entrée <span class="input-unit">(%  massique)</span></div>', unsafe_allow_html=True)
        x_entree = st.number_input("Concentration entrée", 5.0, 30.0, 15.0, 0.5, label_visibility="collapsed", key="x_in")
        
        st.markdown('<div class="input-label">Température alimentation <span class="input-unit">(°C)</span></div>', unsafe_allow_html=True)
        T_alim = st.number_input("Température", 60.0, 100.0, 85.0, 1.0, label_visibility="collapsed", key="T_in")
    
    with col2:
        st.markdown('<div class="input-label">Nombre d\'effets</div>', unsafe_allow_html=True)
        n_effets = st.selectbox("Nombre effets", [2, 3, 4, 5], index=1, label_visibility="collapsed")
        
        st.markdown('<div class="input-label">Concentration finale <span class="input-unit">(% massique)</span></div>', unsafe_allow_html=True)
        x_final = st.number_input("Concentration finale", 50.0, 80.0, 65.0, 1.0, label_visibility="collapsed", key="x_out")
        
        st.markdown('<div class="input-label">Pression vapeur <span class="input-unit">(bar abs)</span></div>', unsafe_allow_html=True)
        P_vapeur = st.number_input("Pression vapeur", 2.0, 5.0, 3.5, 0.1, label_visibility="collapsed", key="P_vap")
    
    # Bouton calculer
    if st.button("▶ CALCULER", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.F = F_debit
                evap.x_F = x_entree / 100
                evap.x_final = x_final / 100
                evap.P_vapeur = P_vapeur
                evap.T_F = T_alim
                evap.resoudre_bilans()
                
                st.markdown('<div class="alert-sci alert-success"><strong>✓ Simulation réussie</strong> - Convergence atteinte</div>', unsafe_allow_html=True)
                
                # Métriques KPI
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📊 Indicateurs Clés</h3></div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    ("Vapeur Chauffe", f"{evap.S:.0f}", "kg/h", col1),
                    ("Économie Vapeur", f"{evap.economie_vapeur():.3f}", "ratio", col2),
                    ("Surface Totale", f"{np.sum(evap.A):.1f}", "m²", col3),
                    ("Concentration", f"{evap.x[-1]*100:.2f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-sci">
                            <div class="metric-sci-label">{label}</div>
                            <div class="metric-sci-value">{value}</div>
                            <div class="metric-sci-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau résultats
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📋 Résultats par Effet</h3></div>', unsafe_allow_html=True)
                
                resultats = pd.DataFrame({
                    'Effet': range(1, n_effets + 1),
                    'T (°C)': [f"{T:.2f}" for T in evap.T],
                    'P (bar)': [f"{P:.3f}" for P in evap.P],
                    'L (kg/h)': [f"{L:.0f}" for L in evap.L],
                    'V (kg/h)': [f"{V:.0f}" for V in evap.V],
                    'x (%)': [f"{x*100:.2f}" for x in evap.x],
                    'A (m²)': [f"{A:.2f}" for A in evap.A]
                })
                
                st.dataframe(resultats, use_container_width=True, hide_index=True)
                
                # Graphiques
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📈 Profils Opératoires</h3></div>', unsafe_allow_html=True)
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Température par Effet', 'Concentration par Effet',
                                  'Pression par Effet', 'Surface d\'Échange par Effet'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.12
                )
                
                effets = list(range(1, n_effets + 1))
                
                # Température
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             line=dict(color='#1565C0', width=2),
                             marker=dict(size=8, color='#1565C0', symbol='circle',
                                       line=dict(color='white', width=2)),
                             name='T'),
                    row=1, col=1
                )
                
                # Concentration
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             line=dict(color='#0D47A1', width=2),
                             marker=dict(size=8, color='#0D47A1', symbol='square',
                                       line=dict(color='white', width=2)),
                             name='x'),
                    row=1, col=2
                )
                
                # Pression
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             line=dict(color='#1976D2', width=2),
                             marker=dict(size=8, color='#1976D2', symbol='diamond',
                                       line=dict(color='white', width=2)),
                             name='P'),
                    row=2, col=1
                )
                
                # Surfaces
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A,
                         marker=dict(color='#42A5F5',
                                   line=dict(color='#1565C0', width=1.5)),
                         name='A'),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Numéro d'Effet", showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="T (°C)", row=1, col=1, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="x (%)", row=1, col=2, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="P (bar)", row=2, col=1, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="A (m²)", row=2, col=2, showgrid=True, gridcolor='#E0E0E0')
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Roboto", size=11, color='#212121'),
                    paper_bgcolor='white',
                    plot_bgcolor='#FAFAFA'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.markdown(f'<div class="alert-sci alert-warning"><strong>⚠ Erreur</strong> - {str(e)}</div>', unsafe_allow_html=True)

# ==================== MODULE CRISTALLISATION ====================

elif page == "Cristallisation":
    st.markdown("""
    <div class="main-header">
        <h1>Cristallisation Batch</h1>
        <p>Simulation de cristallisation par refroidissement contrôlé</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Panel Paramètres
    st.markdown("""
    <div class="sci-panel">
        <div class="sci-panel-header">
            <h3>⚙ Paramètres d'Entrée</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label">Température initiale <span class="input-unit">(°C)</span></div>', unsafe_allow_html=True)
        T_initial = st.number_input("T initial", 60.0, 80.0, 70.0, 1.0, label_visibility="collapsed", key="T0")
        
        st.markdown('<div class="input-label">Température finale <span class="input-unit">(°C)</span></div>', unsafe_allow_html=True)
        T_final = st.number_input("T final", 25.0, 45.0, 35.0, 1.0, label_visibility="collapsed", key="Tf")
        
        st.markdown('<div class="input-label">Masse batch <span class="input-unit">(kg)</span></div>', unsafe_allow_html=True)
        masse_batch = st.number_input("Masse", 1000, 10000, 5000, 500, label_visibility="collapsed", key="masse")
    
    with col2:
        st.markdown('<div class="input-label">Durée opération <span class="input-unit">(heures)</span></div>', unsafe_allow_html=True)
        duree = st.number_input("Durée", 2.0, 8.0, 4.0, 0.5, label_visibility="collapsed", key="duree")
        
        st.markdown('<div class="input-label">Profil thermique</div>', unsafe_allow_html=True)
        profil = st.selectbox("Profil", ["lineaire", "exponentiel", "optimal"], label_visibility="collapsed")
        
        st.markdown('<div class="input-label">Points de calcul</div>', unsafe_allow_html=True)
        n_points = st.number_input("Points", 100, 1000, 500, 50, label_visibility="collapsed", key="npts")
    
    # Bouton calculer
    if st.button("▶ CALCULER", use_container_width=True, key="calc_crist"):
        with st.spinner("Simulation en cours..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                crist.masse = masse_batch
                crist.simuler(profil=profil, n_points=int(n_points))
                
                st.markdown('<div class="alert-sci alert-success"><strong>✓ Simulation terminée</strong> - Convergence atteinte</div>', unsafe_allow_html=True)
                
                # Métriques KPI
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📊 Indicateurs Clés</h3></div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    ("Taille L₅₀", f"{crist.L_50*1e6:.1f}", "µm", col1),
                    ("CV", f"{crist.CV:.2f}", "%", col2),
                    ("Concentration", f"{crist.concentration[-1]:.2f}", "g/100g", col3),
                    ("Sursaturation", f"{crist.sursaturation[-1]:.4f}", "-", col4)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-sci">
                            <div class="metric-sci-label">{label}</div>
                            <div class="metric-sci-value">{value}</div>
                            <div class="metric-sci-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Graphiques
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📈 Évolution Temporelle</h3></div>', unsafe_allow_html=True)
                
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Température vs Temps', 'Sursaturation vs Temps',
                                  'Concentration vs Temps', 'Population vs Temps'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.12
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             line=dict(color='#1565C0', width=2)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             line=dict(color='#0D47A1', width=2)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             line=dict(color='#1976D2', width=2)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             line=dict(color='#42A5F5', width=2)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (h)", showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="T (°C)", row=1, col=1, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="S (-)", row=1, col=2, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="C (g/100g)", row=2, col=1, showgrid=True, gridcolor='#E0E0E0')
                fig.update_yaxes(title_text="m₀ (#/m³)", row=2, col=2, type="log", showgrid=True, gridcolor='#E0E0E0')
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Roboto", size=11, color='#212121'),
                    paper_bgcolor='white',
                    plot_bgcolor='#FAFAFA'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Dimensionnement
                st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>🔧 Dimensionnement Équipement</h3></div>', unsafe_allow_html=True)
                dims = crist.dimensionnement()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Volume", f"{dims['volume']:.2f} m³")
                    st.metric("Diamètre", f"{dims['diametre']:.2f} m")
                with col2:
                    st.metric("Hauteur", f"{dims['hauteur']:.2f} m")
                    st.metric("Puissance Agitation", f"{dims['puissance_agitation']:.2f} kW")
                with col3:
                    st.metric("Surface Serpentin", f"{dims['surface_serpentin']:.2f} m²")
                
            except Exception as e:
                st.markdown(f'<div class="alert-sci alert-warning"><strong>⚠ Erreur</strong> - {str(e)}</div>', unsafe_allow_html=True)

# ==================== MODULE OPTIMISATION ====================

elif page == "Optimisation":
    st.markdown("""
    <div class="main-header">
        <h1>Optimisation Technico-Économique</h1>
        <p>Analyses de sensibilité et optimisation multi-critères</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="input-label">Type d\'analyse</div>', unsafe_allow_html=True)
    analyse = st.selectbox(
        "Analyse",
        ["Impact nombre d'effets", "Analyse économique comparative",
         "Sensibilité pression vapeur", "Sensibilité concentration"],
        label_visibility="collapsed"
    )
    
    if st.button("▶ DÉMARRER L'ANALYSE", use_container_width=True, key="optim"):
        with st.spinner("Analyse en cours..."):
            try:
                if analyse == "Impact nombre d'effets":
                    resultats = []
                    progress = st.progress(0)
                    
                    for idx, n in enumerate(range(2, 6)):
                        evap = EvaporateurMultiplesEffets(n_effets=n)
                        evap.resoudre_bilans()
                        resultats.append({
                            'N': n,
                            'Économie': f"{evap.economie_vapeur():.3f}",
                            'Surface (m²)': f"{np.sum(evap.A):.1f}",
                            'Vapeur (kg/h)': f"{evap.S:.0f}"
                        })
                        progress.progress((idx + 1) / 4)
                    
                    st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📋 Résultats</h3></div>', unsafe_allow_html=True)
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
                            'N': n,
                            'TCI (M€)': f"{TCI/1e6:.2f}",
                            'OPEX (k€/an)': f"{OPEX['total']/1000:.0f}",
                            'Coût (€/t)': f"{cout:.2f}",
                            'Prod (t/an)': f"{production:.0f}"
                        })
                        
                        progress.progress((idx + 1) / 4)
                    
                    st.markdown('<div class="sci-panel-header" style="margin: 1.5rem 0 1rem 0;"><h3>📋 Résultats</h3></div>', unsafe_allow_html=True)
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown('<div class="alert-sci alert-success"><strong>✓ Analyse terminée</strong></div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="alert-sci alert-warning"><strong>⚠ Erreur</strong> - {str(e)}</div>', unsafe_allow_html=True)

# ==================== MODULE CALCULATEURS ====================

elif page == "Calculateurs":
    st.markdown("""
    <div class="main-header">
        <h1>Calculateurs Thermodynamiques</h1>
        <p>Outils de calcul de propriétés physico-chimiques</p>
    </div>
    """, unsafe_allow_html=True)
    
    thermo = ProprietesThermodynamiques()
    
    st.markdown('<div class="input-label">Type de calcul</div>', unsafe_allow_html=True)
    calc = st.selectbox(
        "Calcul",
        ["Propriétés eau et vapeur", "Solubilité saccharose",
         "Élévation point ébullition", "Propriétés solutions"],
        label_visibility="collapsed"
    )
    
    if calc == "Propriétés eau et vapeur":
        st.markdown('<div class="input-label">Pression <span class="input-unit">(bar abs)</span></div>', unsafe_allow_html=True)
        P = st.slider("Pression", 0.1, 10.0, 3.5, 0.1, label_visibility="collapsed")
        
        if st.button("▶ CALCULER", use_container_width=True, key="calc1"):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-sci">
                    <div class="metric-sci-label">Température Saturation</div>
                    <div class="metric-sci-value">{T_sat:.2f}</div>
                    <div class="metric-sci-unit">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-sci">
                    <div class="metric-sci-label">Chaleur Latente</div>
                    <div class="metric-sci-value">{lambda_v/1e6:.3f}</div>
                    <div class="metric-sci-unit">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calc == "Solubilité saccharose":
        st.markdown('<div class="input-label">Température <span class="input-unit">(°C)</span></div>', unsafe_allow_html=True)
        T = st.slider("Température", 20, 90, 60, label_visibility="collapsed")
        
        C_star = thermo.solubilite_saccharose(T)
        
        st.markdown(f"""
        <div class="metric-sci">
            <div class="metric-sci-label">Solubilité à {T}°C</div>
            <div class="metric-sci-value">{C_star:.2f}</div>
            <div class="metric-sci-unit">g saccharose / 100g solution</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Courbe
        T_range = np.linspace(20, 90, 100)
        C_range = [thermo.solubilite_saccharose(t) for t in T_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=T_range, y=C_range, mode='lines',
            line=dict(color='#1565C0', width=3),
            fill='tozeroy', fillcolor='rgba(21, 101, 192, 0.1)'
        ))
        fig.add_vline(x=T, line_dash="dash", line_color='#0D47A1', line_width=2)
        
        fig.update_layout(
            xaxis_title="Température (°C)",
            yaxis_title="Solubilité (g/100g solution)",
            template='plotly_white',
            height=400,
            font=dict(family="Roboto", size=11, color='#212121'),
            paper_bgcolor='white',
            plot_bgcolor='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== MODULE DOCUMENTATION ====================

elif page == "Documentation":
    st.markdown("""
    <div class="main-header">
        <h1>Documentation Technique</h1>
        <p>Guide d'utilisation et références</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sci-panel">
        <div class="sci-panel-header">
            <h3>📚 Modules Disponibles</h3>
        </div>
        <p><strong>Évaporation :</strong> Simulation d'évaporateurs à multiples effets</p>
        <p><strong>Cristallisation :</strong> Modélisation batch par refroidissement</p>
        <p><strong>Optimisation :</strong> Analyses technico-économiques</p>
        <p><strong>Calculateurs :</strong> Propriétés thermodynamiques</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sci-panel">
        <div class="sci-panel-header">
            <h3>🔗 Ressources</h3>
        </div>
        <p><strong>Repository GitHub :</strong> github.com/OUMSSAAD/Projet_Evapo_Crist</p>
        <p><strong>Docker Hub :</strong> docker pull oumssaad123/evapo-crist-app:latest</p>
        <p><strong>Documentation CoolProp :</strong> coolprop.org</p>
    </div>
    """, unsafe_allow_html=True)