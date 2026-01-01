"""
Application Web - Évaporation et Cristallisation
Version Ultra-Professionnelle Simplifiée
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
    page_title="Évaporation & Cristallisation",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== STYLE MINIMALISTE PROFESSIONNEL ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables Épurées */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-600: #4b5563;
        --gray-900: #111827;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    /* Reset Global */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Container */
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1280px;
    }
    
    /* Header Minimaliste */
    .app-header {
        background: white;
        border-bottom: 1px solid var(--gray-200);
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--gray-900);
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
    }
    
    .app-subtitle {
        font-size: 0.875rem;
        color: var(--gray-600);
        font-weight: 400;
        margin: 0;
    }
    
    /* Tabs Épurés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-bottom: 1px solid var(--gray-200);
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.875rem 1.5rem;
        border: none;
        font-weight: 500;
        font-size: 0.875rem;
        color: var(--gray-600);
        background: transparent;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--gray-900);
        background: var(--gray-50);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom-color: var(--primary);
        background: transparent;
    }
    
    /* Buttons Minimalistes */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 0.625rem 1.25rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.15);
    }
    
    /* Cards Simples */
    .metric-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        padding: 1.25rem;
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-color: var(--gray-300);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--gray-600);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--gray-900);
        line-height: 1;
    }
    
    .metric-unit {
        font-size: 0.875rem;
        color: var(--gray-600);
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    /* Inputs Raffinés */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border: 1px solid var(--gray-200);
        border-radius: 6px;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Slider Minimal */
    .stSlider > div > div > div {
        background: var(--primary);
    }
    
    /* Messages */
    .alert-success {
        background: #ecfdf5;
        border-left: 3px solid var(--success);
        padding: 1rem;
        border-radius: 6px;
        color: #065f46;
        font-size: 0.875rem;
    }
    
    .alert-info {
        background: #eff6ff;
        border-left: 3px solid var(--primary);
        padding: 1rem;
        border-radius: 6px;
        color: #1e40af;
        font-size: 0.875rem;
    }
    
    /* Dataframes */
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid var(--gray-200);
        border-radius: 6px;
        overflow: hidden;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: var(--primary);
        height: 4px;
    }
    
    /* Section Headers */
    h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--gray-900);
        margin: 2rem 0 1rem 0;
        letter-spacing: -0.025em;
    }
    
    h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--gray-900);
        margin: 1.5rem 0 0.75rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    /* Footer */
    .app-footer {
        border-top: 1px solid var(--gray-200);
        padding: 2rem 0 1rem 0;
        margin-top: 4rem;
        text-align: center;
        color: var(--gray-600);
        font-size: 0.875rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .app-title {
            font-size: 1.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================

st.markdown("""
<div class="app-header">
    <div class="app-title">🏭 Évaporation & Cristallisation</div>
    <div class="app-subtitle">
        Université Hassan 1 - FST Settat | PIC 2025-2026 | 
        OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== NAVIGATION ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Accueil",
    "Évaporation", 
    "Cristallisation",
    "Optimisation",
    "Calculateur"
])

# ==================== ACCUEIL ====================

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Présentation")
        
        st.markdown("""
        Cette application permet la **simulation complète** d'une unité 
        de production de sucre cristallisé à partir de jus de canne à sucre.
        
        **Fonctionnalités principales :**
        
        - Évaporation à multiples effets (2-5)
        - Cristallisation batch avec contrôle thermique
        - Analyses d'optimisation technico-économique
        - Calculateurs thermodynamiques
        """)
        
        st.markdown("### Spécifications")
        
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
        st.markdown("### Métriques")
        
        metrics = [
            ("Production", "43 kt/an"),
            ("Économie vapeur", "2.04"),
            ("ROI", "0.08 ans"),
            ("VAN", "274 M€")
        ]
        
        for label, value in metrics:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== ÉVAPORATION ====================

with tab2:
    st.markdown("## Évaporation à Multiples Effets")
    
    with st.expander("⚙️ Paramètres", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n_effets = st.slider("Nombre d'effets", 2, 5, 3)
        with col2:
            P_vapeur = st.number_input("Pression (bar)", 2.0, 5.0, 3.5, 0.1)
        with col3:
            x_final = st.number_input("Concentration (%)", 50.0, 80.0, 65.0, 1.0)
        with col4:
            F_debit = st.number_input("Débit (kg/h)", 10000, 40000, 20000, 1000)
    
    if st.button("Simuler", use_container_width=True):
        with st.spinner("Calcul..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.P_vapeur = P_vapeur
                evap.x_final = x_final / 100
                evap.F = F_debit
                evap.resoudre_bilans()
                
                st.markdown('<div class="alert-success">✓ Simulation réussie</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_data = [
                    ("Vapeur chauffe", f"{evap.S:.0f}", "kg/h", col1),
                    ("Économie", f"{evap.economie_vapeur():.2f}", "ratio", col2),
                    ("Surface", f"{np.sum(evap.A):.0f}", "m²", col3),
                    ("Concentration", f"{evap.x[-1]*100:.1f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics_data:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau
                st.markdown("### Résultats")
                
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
                    vertical_spacing=0.12,
                    horizontal_spacing=0.1
                )
                
                effets = list(range(1, n_effets + 1))
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             line=dict(color='#2563eb', width=2),
                             marker=dict(size=8)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             line=dict(color='#10b981', width=2),
                             marker=dict(size=8)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             line=dict(color='#f59e0b', width=2),
                             marker=dict(size=8)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A, marker=dict(color='#8b5cf6')),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Effet", showgrid=False)
                fig.update_yaxes(title_text="T (°C)", row=1, col=1, showgrid=True, gridcolor='#f3f4f6')
                fig.update_yaxes(title_text="x (%)", row=1, col=2, showgrid=True, gridcolor='#f3f4f6')
                fig.update_yaxes(title_text="P (bar)", row=2, col=1, showgrid=True, gridcolor='#f3f4f6')
                fig.update_yaxes(title_text="A (m²)", row=2, col=2, showgrid=True, gridcolor='#f3f4f6')
                
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12),
                    margin=dict(t=40, b=40, l=40, r=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erreur: {e}")

# ==================== CRISTALLISATION ====================

with tab3:
    st.markdown("## Cristallisation Batch")
    
    with st.expander("⚙️ Paramètres", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            T_initial = st.number_input("T initiale (°C)", 60.0, 80.0, 70.0, 1.0)
        with col2:
            T_final = st.number_input("T finale (°C)", 25.0, 45.0, 35.0, 1.0)
        with col3:
            duree = st.number_input("Durée (h)", 2.0, 8.0, 4.0, 0.5)
        with col4:
            profil = st.selectbox("Profil", ["lineaire", "exponentiel", "optimal"])
    
    if st.button("Simuler ", use_container_width=True, key="crist_btn"):
        with st.spinner("Calcul..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                crist.simuler(profil=profil, n_points=500)
                
                st.markdown('<div class="alert-success">✓ Simulation réussie</div>', unsafe_allow_html=True)
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                
                metrics = [
                    ("Taille moyenne", f"{crist.L_50*1e6:.1f}", "µm", col1),
                    ("CV", f"{crist.CV:.1f}", "%", col2),
                    ("Concentration", f"{crist.concentration[-1]:.2f}", "g/100g", col3)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Graphiques
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Température', 'Sursaturation', 'Concentration', 'Population'),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             line=dict(color='#ef4444', width=2)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             line=dict(color='#2563eb', width=2)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             line=dict(color='#10b981', width=2)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             line=dict(color='#8b5cf6', width=2)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (h)", showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor='#f3f4f6')
                fig.update_yaxes(type="log", row=2, col=2)
                
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12),
                    margin=dict(t=40, b=40, l=40, r=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Dimensionnement
                st.markdown("### Dimensionnement")
                dims = crist.dimensionnement()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Volume", f"{dims['volume']:.2f} m³")
                    st.metric("Diamètre", f"{dims['diametre']:.2f} m")
                with col2:
                    st.metric("Hauteur", f"{dims['hauteur']:.2f} m")
                    st.metric("Puissance", f"{dims['puissance_agitation']:.2f} kW")
                with col3:
                    st.metric("Surface serpentin", f"{dims['surface_serpentin']:.2f} m²")
                
            except Exception as e:
                st.error(f"Erreur: {e}")

# ==================== OPTIMISATION ====================

with tab4:
    st.markdown("## Analyse d'Optimisation")
    
    analyse = st.selectbox(
        "Type d'analyse",
        ["Impact nombre d'effets", "Analyse économique", "Sensibilité pression", "Sensibilité concentration"]
    )
    
    if st.button("Analyser", use_container_width=True):
        with st.spinner("Analyse..."):
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
                            'Surface (m²)': np.sum(evap.A),
                            'Vapeur (kg/h)': evap.S
                        })
                        progress.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Graphique
                    fig = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=('Économie vapeur', 'Surface', 'Consommation')
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Économie'],
                                 mode='lines+markers', line=dict(color='#2563eb', width=2)),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Surface (m²)'],
                                 mode='lines+markers', line=dict(color='#10b981', width=2)),
                        row=1, col=2
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=df['Effets'], y=df['Vapeur (kg/h)'],
                                 mode='lines+markers', line=dict(color='#ef4444', width=2)),
                        row=1, col=3
                    )
                    
                    fig.update_xaxes(title_text="Nombre d'effets", showgrid=False)
                    fig.update_yaxes(showgrid=True, gridcolor='#f3f4f6')
                    
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        template='plotly_white',
                        font=dict(family="Inter", size=12)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif analyse == "Analyse économique":
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
                            'TCI (M€)': TCI/1e6,
                            'OPEX (k€/an)': OPEX['total']/1000,
                            'Coût (€/t)': cout,
                            'Production (t/an)': production
                        })
                        
                        progress.progress((idx + 1) / 4)
                    
                    df = pd.DataFrame(resultats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    meilleur = df.loc[df['Coût (€/t)'].idxmin()]
                    st.markdown(f"""
                    <div class="alert-info">
                        <strong>Configuration optimale: {int(meilleur['Effets'])} effets</strong><br>
                        Coût: {meilleur['Coût (€/t)']:.2f} €/t · 
                        TCI: {meilleur['TCI (M€)']:.2f} M€ · 
                        Production: {meilleur['Production (t/an)']:.0f} t/an
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="alert-success">✓ Analyse terminée</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur: {e}")

# ==================== CALCULATEUR ====================

with tab5:
    st.markdown("## Calculateurs Thermodynamiques")
    
    calc = st.selectbox(
        "Type de calcul",
        ["Propriétés eau/vapeur", "Solubilité saccharose", "EPE", "Économie vapeur"]
    )
    
    thermo = ProprietesThermodynamiques()
    
    if calc == "Propriétés eau/vapeur":
        P = st.slider("Pression (bar)", 0.1, 10.0, 3.5, 0.1)
        
        if st.button("Calculer ", use_container_width=True, key="calc1"):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Température saturation</div>
                    <div class="metric-value">{T_sat:.2f}</div>
                    <div class="metric-unit">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Chaleur latente</div>
                    <div class="metric-value">{lambda_v/1e6:.2f}</div>
                    <div class="metric-unit">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calc == "Solubilité saccharose":
        T = st.slider("Température (°C)", 20, 90, 60)
        C_star = thermo.solubilite_saccharose(T)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Solubilité à {T}°C</div>
            <div class="metric-value">{C_star:.2f}</div>
            <div class="metric-unit">g/100g solution</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Courbe
        T_range = np.linspace(20, 90, 100)
        C_range = [thermo.solubilite_saccharose(t) for t in T_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=T_range, y=C_range, mode='lines',
            line=dict(color='#2563eb', width=2),
            fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.1)'
        ))
        fig.add_vline(x=T, line_dash="dash", line_color='#ef4444')
        
        fig.update_layout(
            xaxis_title="Température (°C)",
            yaxis_title="Solubilité (g/100g)",
            template='plotly_white',
            height=400,
            font=dict(family="Inter", size=12),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER ====================

st.markdown("""
<div class="app-footer">
    Université Hassan 1 - FST Settat | Filière PIC 2025-2026<br>
    <strong>OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE</strong>
</div>
""", unsafe_allow_html=True)