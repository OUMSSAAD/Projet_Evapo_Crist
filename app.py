"""
Application Web - Évaporation et Cristallisation
Version Ultra-Professionnelle - Design Premium
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

# ==================== PALETTE PREMIUM ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Palette Premium Inspirée de Stripe/Linear */
    :root {
        /* Primaire - Bleu profond élégant */
        --primary: #0066FF;
        --primary-hover: #0052CC;
        --primary-light: #E6F0FF;
        --primary-dark: #003D99;
        
        /* Secondaire - Violet sophistiqué */
        --secondary: #6366F1;
        --secondary-light: #EEF2FF;
        
        /* Accent - Cyan moderne */
        --accent: #06B6D4;
        --accent-light: #CFFAFE;
        
        /* Succès */
        --success: #10B981;
        --success-light: #D1FAE5;
        
        /* Warning */
        --warning: #F59E0B;
        --warning-light: #FEF3C7;
        
        /* Danger */
        --danger: #EF4444;
        --danger-light: #FEE2E2;
        
        /* Neutres - Échelle grise sophistiquée */
        --gray-50: #F9FAFB;
        --gray-100: #F3F4F6;
        --gray-200: #E5E7EB;
        --gray-300: #D1D5DB;
        --gray-400: #9CA3AF;
        --gray-500: #6B7280;
        --gray-600: #4B5563;
        --gray-700: #374151;
        --gray-800: #1F2937;
        --gray-900: #111827;
        
        /* Blanc pur et noir profond */
        --white: #FFFFFF;
        --black: #000000;
        
        /* Backgrounds */
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --bg-tertiary: #F3F4F6;
        
        /* Bordures */
        --border: #E5E7EB;
        --border-hover: #D1D5DB;
        
        /* Ombres */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Reset Global */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        background: var(--bg-secondary);
    }
    
    /* Header Premium avec Glassmorphism */
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
        pointer-events: none;
        animation: float 6s ease-in-out infinite;
    }
    
    .premium-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.4;
        pointer-events: none;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    .premium-header h1 {
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0 0 0.75rem 0;
        letter-spacing: -0.025em;
        position: relative;
        z-index: 1;
    }
    
    .premium-header .subtitle {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.95;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .premium-header .badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Tabs Premium avec Glassmorphism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 0.75rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.875rem 1.75rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9375rem;
        color: var(--gray-600);
        background: transparent;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: translateX(-50%);
        transition: width 0.3s ease;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.08);
        color: #667eea;
    }
    
    .stTabs [data-baseweb="tab"]:hover::after {
        width: 60%;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [aria-selected="true"]::after {
        width: 0;
    }
    
    /* Cards Premium avec effet 3D */
    .premium-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 20px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15), 0 10px 20px rgba(118, 75, 162, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .premium-card:hover::before {
        transform: scaleX(1);
    }
    
    /* Metric Card Premium avec Glassmorphism */
    .metric-premium {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 2rem 1.75rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    
    .metric-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    .metric-premium::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
        pointer-events: none;
    }
    
    .metric-premium:hover {
        transform: translateY(-4px);
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2), 0 8px 24px rgba(118, 75, 162, 0.15);
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
        margin: 0.25rem 0;
        animation: shimmer 3s linear infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    .metric-unit {
        font-size: 0.875rem;
        color: var(--gray-500);
        font-weight: 500;
    }
    
    /* Buttons Premium avec animations */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3), 0 4px 12px rgba(118, 75, 162, 0.2);
        letter-spacing: 0.02em;
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
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.4), 0 10px 25px rgba(118, 75, 162, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Inputs Premium */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border: 1.5px solid var(--border);
        border-radius: 8px;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
        background: var(--white);
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-light);
    }
    
    /* Slider Premium */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    .stSlider > div > div > div > div {
        background: var(--white);
        border: 3px solid var(--primary);
        box-shadow: var(--shadow-md);
    }
    
    /* Alerts Premium avec gradient borders */
    .alert-success {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        padding: 1.5rem;
        border-radius: 14px;
        color: #065F46;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
    }
    
    .alert-success::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 14px;
        padding: 2px;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        padding: 1.5rem;
        border-radius: 14px;
        color: #1E40AF;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
    }
    
    .alert-info::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 14px;
        padding: 2px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        padding: 1.5rem;
        border-radius: 14px;
        color: #92400E;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.15);
    }
    
    .alert-warning::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 14px;
        padding: 2px;
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    /* Dataframe Premium */
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    /* Progress Bar Premium */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        height: 6px;
        border-radius: 10px;
    }
    
    /* Expander Premium */
    .streamlit-expanderHeader {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9375rem;
        padding: 1rem 1.25rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--primary-light);
        border-color: var(--primary);
    }
    
    /* Headers */
    h2 {
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--gray-900);
        margin: 2.5rem 0 1.25rem 0;
        letter-spacing: -0.025em;
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-800);
        margin: 1.75rem 0 1rem 0;
    }
    
    /* Section Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.025em;
    }
    
    .badge-primary {
        background: var(--primary-light);
        color: var(--primary-dark);
    }
    
    .badge-success {
        background: var(--success-light);
        color: #065F46;
    }
    
    /* Footer Premium */
    .premium-footer {
        border-top: 1px solid var(--border);
        padding: 2.5rem 0 1.5rem 0;
        margin-top: 4rem;
        text-align: center;
    }
    
    .premium-footer-content {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary-light) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .premium-footer p {
        color: var(--gray-600);
        font-size: 0.9375rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .premium-footer strong {
        color: var(--gray-900);
        font-weight: 700;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .premium-header h1 {
            font-size: 1.75rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .premium-card, .metric-premium {
        animation: fadeInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER PREMIUM ====================

st.markdown("""
<div class="premium-header">
    <h1>🏭 Évaporation & Cristallisation</h1>
    <div class="subtitle">
        Conception d'une Unité Intégrée de Production de Sucre
    </div>
    <div class="badge">Université Hassan 1 - FST Settat | PIC 2025-2026</div>
    <div class="badge">OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE</div>
</div>
""", unsafe_allow_html=True)

# ==================== NAVIGATION ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Accueil",
    "💧 Évaporation", 
    "💎 Cristallisation",
    "📊 Optimisation",
    "🧮 Calculateur"
])

# ==================== ACCUEIL ====================

with tab1:
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("## 📋 Présentation du Projet")
        
        st.markdown("""
        <div class="premium-card">
            <h3 style="color: var(--primary); margin-top: 0;">🎯 Contexte Industriel</h3>
            <p style="line-height: 1.8; color: var(--gray-700);">
                Application de <strong>simulation avancée</strong> pour la conception d'une unité 
                complète de production de sucre cristallisé à partir de jus de canne à sucre.
            </p>
            <p style="line-height: 1.8; color: var(--gray-700); margin-bottom: 0;">
                <strong>Le système intègre :</strong>
            </p>
            <ul style="line-height: 2; color: var(--gray-700);">
                <li>✅ Évaporation à multiples effets (2-5 configurations)</li>
                <li>✅ Cristallisation batch avec contrôle thermique avancé</li>
                <li>✅ Optimisation énergétique et récupération de chaleur</li>
                <li>✅ Analyse technico-économique complète</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Spécifications Techniques")
        
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
            ],
            'Statut': [
                '✓ Nominal',
                '✓ Optimal',
                '✓ Cible',
                '✓ Standard',
                '✓ Efficace'
            ]
        })
        
        st.dataframe(specs, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📈 Métriques Clés")
        
        metrics_data = [
            ("Production Annuelle", "43", "kt/an", "success"),
            ("Économie Vapeur", "2.04", "ratio", "primary"),
            ("Retour Investissement", "0.08", "ans", "warning"),
            ("Valeur Actuelle Nette", "274", "M€", "success")
        ]
        
        for label, value, unit, color in metrics_data:
            st.markdown(f"""
            <div class="metric-premium">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== ÉVAPORATION ====================

with tab2:
    st.markdown("## 💧 Simulation d'Évaporation à Multiples Effets")
    
    with st.expander("⚙️ Configuration des Paramètres", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n_effets = st.slider("Nombre d'effets", 2, 5, 3, help="Plus d'effets = meilleure économie")
        with col2:
            P_vapeur = st.number_input("Pression vapeur (bar)", 2.0, 5.0, 3.5, 0.1)
        with col3:
            x_final = st.number_input("Concentration (%)", 50.0, 80.0, 65.0, 1.0)
        with col4:
            F_debit = st.number_input("Débit (kg/h)", 10000, 40000, 20000, 1000)
    
    if st.button("▶️  Lancer la Simulation", use_container_width=True):
        with st.spinner("⏳ Calcul en cours..."):
            try:
                evap = EvaporateurMultiplesEffets(n_effets=n_effets)
                evap.P_vapeur = P_vapeur
                evap.x_final = x_final / 100
                evap.F = F_debit
                evap.resoudre_bilans()
                
                st.markdown('<div class="alert-success"><strong>✓ Simulation réussie !</strong> Les résultats sont maintenant disponibles ci-dessous.</div>', unsafe_allow_html=True)
                
                # Métriques
                st.markdown("### 📊 Résultats Principaux")
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    ("Vapeur de Chauffe", f"{evap.S:.0f}", "kg/h", col1),
                    ("Économie Vapeur", f"{evap.economie_vapeur():.2f}", "ratio", col2),
                    ("Surface Totale", f"{np.sum(evap.A):.0f}", "m²", col3),
                    ("Concentration Finale", f"{evap.x[-1]*100:.1f}", "%", col4)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-premium">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tableau
                st.markdown("### 📋 Détails par Effet")
                
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
                
                # Graphiques Plotly
                st.markdown("### 📈 Visualisations")
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Température', 'Concentration', 'Pression', 'Surface'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
                
                effets = list(range(1, n_effets + 1))
                
                # Couleurs premium
                color_temp = '#0066FF'
                color_conc = '#10B981'
                color_press = '#F59E0B'
                color_surf = '#6366F1'
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.T, mode='lines+markers',
                             line=dict(color=color_temp, width=3),
                             marker=dict(size=10, line=dict(color='white', width=2))),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.x * 100, mode='lines+markers',
                             line=dict(color=color_conc, width=3),
                             marker=dict(size=10, line=dict(color='white', width=2))),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=effets, y=evap.P, mode='lines+markers',
                             line=dict(color=color_press, width=3),
                             marker=dict(size=10, line=dict(color='white', width=2))),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=effets, y=evap.A, marker=dict(color=color_surf, line=dict(color='white', width=1))),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Effet", showgrid=False, title_font=dict(size=13, family='Inter'))
                fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6', title_font=dict(size=13, family='Inter'))
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12, color='#374151'),
                    margin=dict(t=50, b=40, l=40, r=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la simulation: {e}")

# ==================== CRISTALLISATION ====================

with tab3:
    st.markdown("## 💎 Cristallisation Batch")
    
    with st.expander("⚙️ Configuration des Paramètres", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            T_initial = st.number_input("T initiale (°C)", 60.0, 80.0, 70.0, 1.0)
        with col2:
            T_final = st.number_input("T finale (°C)", 25.0, 45.0, 35.0, 1.0)
        with col3:
            duree = st.number_input("Durée (h)", 2.0, 8.0, 4.0, 0.5)
        with col4:
            profil = st.selectbox("Profil", ["lineaire", "exponentiel", "optimal"])
    
    if st.button("▶️  Lancer la Simulation ", use_container_width=True, key="crist"):
        with st.spinner("⏳ Simulation en cours..."):
            try:
                crist = CristalliseurBatch()
                crist.T_0 = T_initial
                crist.T_f = T_final
                crist.duree = duree * 3600
                crist.simuler(profil=profil, n_points=500)
                
                st.markdown('<div class="alert-success"><strong>✓ Simulation terminée !</strong> Analyse complète disponible.</div>', unsafe_allow_html=True)
                
                # Métriques
                st.markdown("### 📊 Résultats de Cristallisation")
                col1, col2, col3 = st.columns(3)
                
                metrics = [
                    ("Taille Moyenne", f"{crist.L_50*1e6:.1f}", "µm", col1),
                    ("Coeff. Variation", f"{crist.CV:.1f}", "%", col2),
                    ("Concentration Finale", f"{crist.concentration[-1]:.2f}", "g/100g", col3)
                ]
                
                for label, value, unit, col in metrics:
                    with col:
                        st.markdown(f"""
                        <div class="metric-premium">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-unit">{unit}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Graphiques
                st.markdown("### 📈 Évolution Temporelle")
                
                temps_h = crist.temps / 3600
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('🌡️ Température', '📊 Sursaturation', '💧 Concentration', '📈 Population'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.temperature, mode='lines',
                             line=dict(color='#EF4444', width=3), fill='tozeroy',
                             fillcolor='rgba(239, 68, 68, 0.1)'),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.sursaturation, mode='lines',
                             line=dict(color='#0066FF', width=3)),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.concentration, mode='lines',
                             line=dict(color='#10B981', width=3)),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=temps_h, y=crist.moments[:, 0], mode='lines',
                             line=dict(color='#6366F1', width=3)),
                    row=2, col=2
                )
                
                fig.update_xaxes(title_text="Temps (h)", showgrid=False, title_font=dict(family='Inter'))
                fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6', title_font=dict(family='Inter'))
                fig.update_yaxes(type="log", row=2, col=2)
                
                fig.update_layout(
                    height=650,
                    showlegend=False,
                    template='plotly_white',
                    font=dict(family="Inter", size=12, color='#374151'),
                    margin=dict(t=50, b=40, l=40, r=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Dimensionnement
                st.markdown("### 📐 Dimensionnement du Cristalliseur")
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
                st.error(f"❌ Erreur: {e}")

# ==================== OPTIMISATION ====================

with tab4:
    st.markdown("## 📊 Analyses d'Optimisation")
    
    analyse = st.selectbox(
        "Sélectionnez le type d'analyse",
        ["Impact du nombre d'effets", "Analyse économique", "Sensibilité pression vapeur", "Sensibilité concentration"]
    )
    
    if st.button("▶️  Démarrer l'Analyse", use_container_width=True):
        with st.spinner("⏳ Analyse en cours..."):
            try:
                if analyse == "Impact du nombre d'effets":
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
                    
                    # Graphiques
                    fig = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=('Économie de vapeur', 'Surface d\'échange', 'Consommation vapeur')
                    )
                    
                    colors = ['#0066FF', '#10B981', '#EF4444']
                    
                    for idx, (col, color) in enumerate(zip(['Économie', 'Surface (m²)', 'Vapeur (kg/h)'], colors)):
                        fig.add_trace(
                            go.Scatter(x=df['Effets'], y=df[col],
                                     mode='lines+markers', line=dict(color=color, width=3),
                                     marker=dict(size=12, line=dict(color='white', width=2))),
                            row=1, col=idx+1
                        )
                    
                    fig.update_xaxes(title_text="Nombre d'effets", showgrid=False, title_font=dict(family='Inter'))
                    fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6', title_font=dict(family='Inter'))
                    
                    fig.update_layout(
                        height=450,
                        showlegend=False,
                        template='plotly_white',
                        font=dict(family="Inter", size=12, color='#374151')
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
                        <strong>✓ Configuration Optimale: {int(meilleur['Effets'])} effets</strong><br><br>
                        <strong>Coût production:</strong> {meilleur['Coût (€/t)']:.2f} €/tonne<br>
                        <strong>Investissement:</strong> {meilleur['TCI (M€)']:.2f} M€<br>
                        <strong>Production annuelle:</strong> {meilleur['Production (t/an)']:.0f} tonnes/an
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="alert-success"><strong>✓ Analyse terminée avec succès !</strong></div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# ==================== CALCULATEUR ====================

with tab5:
    st.markdown("## 🧮 Calculateurs Thermodynamiques")
    
    calc = st.selectbox(
        "Type de calcul",
        ["Propriétés eau/vapeur", "Solubilité saccharose", "EPE", "Économie vapeur"]
    )
    
    thermo = ProprietesThermodynamiques()
    
    if calc == "Propriétés eau/vapeur":
        P = st.slider("Pression (bar)", 0.1, 10.0, 3.5, 0.1)
        
        if st.button("🔍 Calculer", use_container_width=True, key="c1"):
            T_sat = thermo.temperature_saturation(P)
            lambda_v = thermo.chaleur_latente(P)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-premium">
                    <div class="metric-label">Température de Saturation</div>
                    <div class="metric-value">{T_sat:.2f}</div>
                    <div class="metric-unit">°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-premium">
                    <div class="metric-label">Chaleur Latente</div>
                    <div class="metric-value">{lambda_v/1e6:.2f}</div>
                    <div class="metric-unit">MJ/kg</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif calc == "Solubilité saccharose":
        T = st.slider("Température (°C)", 20, 90, 60)
        C_star = thermo.solubilite_saccharose(T)
        
        st.markdown(f"""
        <div class="metric-premium">
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
            line=dict(color='#0066FF', width=3),
            fill='tozeroy', fillcolor='rgba(0, 102, 255, 0.1)'
        ))
        fig.add_vline(x=T, line_dash="dash", line_color='#EF4444', line_width=2)
        
        fig.update_layout(
            xaxis_title="Température (°C)",
            yaxis_title="Solubilité (g/100g)",
            template='plotly_white',
            height=450,
            font=dict(family="Inter", size=12, color='#374151'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER PREMIUM ====================

st.markdown("""
<div class="premium-footer">
    <div class="premium-footer-content">
        <p style="font-size: 1.125rem; font-weight: 700; color: #0066FF; margin-bottom: 0.75rem;">
            🏭 Application Évaporation & Cristallisation
        </p>
        <p>
            <strong>Université Hassan 1 - Faculté des Sciences et Techniques Settat</strong><br>
            Filière Procédés et Ingénierie Chimique (PIC) | Année Universitaire 2025-2026
        </p>
        <p style="margin-top: 1rem;">
            <strong>Réalisé par:</strong> OUMSSAAD EL GHAZI · KOLMAN GOD WIN TETE<br>
            <strong>Encadré par:</strong> Pr. BAKHER Zineelabidine
        </p>
    </div>
    <p style="font-size: 0.875rem; color: #6B7280;">
        © 2025-2026 - Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)