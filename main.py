
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys

# Imports des modules du projet
from thermodynamique import ProprietesThermodynamiques
from evaporateurs import EvaporateurMultiplesEffets
from cristallisation import CristalliseurBatch, comparer_profils
from optimisation import AnalyseSensibilite, AnalyseEconomique


def afficher_en_tete():
    """Affiche l'en-tête du programme."""
    print("\n" + "="*80)
    print("║" + " "*78 + "║")
    print("║" + "PROJET: ÉVAPORATION ET CRISTALLISATION".center(78) + "║")
    print("║" + "Conception d'une Unité Intégrée de Production de Sucre".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "Université Hassan 1 - FST Settat".center(78) + "║")
    print("║" + "Filière: Procédés et Ingénierie Chimique (PIC)".center(78) + "║")
    print("║" + "Année Universitaire 2024-2025".center(78) + "║")
    print("║" + " "*78 + "║")
    print("="*80)
    print(f"Date d'exécution: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")


def partie1_evaporation():
    """
    PARTIE 1: Évaporation à Multiples Effets (40 points)
    """
    print("\n" + "█"*80)
    print("█ PARTIE 1: ÉVAPORATION À MULTIPLES EFFETS")
    print("█"*80)
    
    # 1.1 Modélisation Thermodynamique (15 points)
    print("\n1.1 - MODÉLISATION THERMODYNAMIQUE")
    print("-" * 60)
    
    evap = EvaporateurMultiplesEffets(n_effets=3)
    print("Configuration: Triple effet en co-courant")
    print(f"Alimentation: {evap.F} kg/h à {evap.x_F*100}%")
    print(f"Concentration visée: {evap.x_final*100}%")
    
    print("\nRésolution des bilans de matière et d'énergie...")
    evap.resoudre_bilans()
    
    evap.afficher_resultats()
    evap.tracer_profils()
    
    # 1.2 Optimisation Énergétique (10 points)
    print("\n1.2 - OPTIMISATION ÉNERGÉTIQUE")
    print("-" * 60)
    
    analyse = AnalyseSensibilite()
    analyse.analyse_nombre_effets(n_min=2, n_max=5)
    
    # 1.3 Analyse de Sensibilité (15 points)
    print("\n1.3 - ANALYSE DE SENSIBILITÉ")
    print("-" * 60)
    
    print("\nAnalyse 1: Impact de la pression de vapeur")
    analyse.analyse_pression_vapeur(P_min=2.5, P_max=4.5, n_points=15)
    
    print("\nAnalyse 2: Impact de la concentration finale")
    analyse.analyse_concentration_finale(x_min=60, x_max=70, n_points=15)
    
    print("\nAnalyse 3: Impact du débit d'alimentation")
    analyse.analyse_debit_alimentation(variation=0.20, n_points=15)
    
    return evap


def partie2_cristallisation():
    """
    PARTIE 2: Cristallisation (40 points)
    """
    print("\n" + "█"*80)
    print("█ PARTIE 2: CRISTALLISATION")
    print("█"*80)
    
    # 2.1 Modélisation de la Cinétique (20 points)
    print("\n2.1 - MODÉLISATION DE LA CINÉTIQUE")
    print("-" * 60)
    
    crist = CristalliseurBatch()
    print(f"Configuration: Batch refroidi")
    print(f"Température: {crist.T_0}°C → {crist.T_f}°C")
    print(f"Durée: {crist.duree/3600} heures")
    print(f"Masse de sirop: {crist.masse_batch} kg")
    
    # 2.2 Stratégie de Refroidissement (10 points)
    print("\n2.2 - COMPARAISON DES PROFILS DE REFROIDISSEMENT")
    print("-" * 60)
    
    comparer_profils()
    
    # 2.3 Dimensionnement du Cristalliseur (10 points)
    print("\n2.3 - DIMENSIONNEMENT DU CRISTALLISEUR")
    print("-" * 60)
    
    crist_dims = crist.dimensionnement()
    
    return crist, crist_dims


def partie3_integration_optimisation(evap, crist_dims):
    """
    PARTIE 3: Intégration et Optimisation Globale (20 points)
    """
    print("\n" + "█"*80)
    print("█ PARTIE 3: INTÉGRATION ET OPTIMISATION GLOBALE")
    print("█"*80)
    
    # 3.1 Intégration Énergétique (10 points)
    print("\n3.1 - INTÉGRATION ÉNERGÉTIQUE")
    print("-" * 60)
    
    print("\nStratégies de récupération d'énergie:")
    print("1. Récupération chaleur des condensats pour préchauffer l'alimentation")
    print("2. Utilisation vapeurs du dernier effet pour préchauffer le sirop")
    print("3. Intégration thermique entre évaporation et cristallisation")
    
    # Calcul de l'économie énergétique
    lambda_vap = 2.15e6  # J/kg
    chaleur_condensats = evap.S * lambda_vap / 3600  # W
    
    # Préchauffage alimentation
    thermo = ProprietesThermodynamiques()
    Cp_F = thermo.capacite_calorifique_solution(evap.x_F)
    delta_T_prechauffe = 20  # °C
    chaleur_prechauffe = evap.F * Cp_F * delta_T_prechauffe / 3600  # W
    
    taux_recuperation = min(chaleur_prechauffe / chaleur_condensats * 100, 80)
    
    print(f"\nChaleur disponible (condensats): {chaleur_condensats/1000:.1f} kW")
    print(f"Besoin préchauffage: {chaleur_prechauffe/1000:.1f} kW")
    print(f"Taux de récupération potentiel: {taux_recuperation:.1f}%")
    
    economie_vapeur = chaleur_prechauffe * taux_recuperation / 100 * 3600 / lambda_vap
    print(f"Économie de vapeur: {economie_vapeur:.0f} kg/h ({economie_vapeur/evap.S*100:.1f}%)")
    
    # 3.2 Analyse Technico-Économique (10 points)
    print("\n3.2 - ANALYSE TECHNICO-ÉCONOMIQUE")
    print("-" * 60)
    
    eco = AnalyseEconomique()
    
    # Analyse pour la configuration choisie
    resultats = eco.analyser_projet(n_effets=3)
    
    # Comparaison de configurations
    print("\n" + "-" * 60)
    print("COMPARAISON DES CONFIGURATIONS")
    print("-" * 60)
    eco.comparer_configurations()


def generer_rapport_synthese(evap, crist_dims, resultats_eco):
    """
    Génère un rapport de synthèse des résultats.
    """
    print("\n" + "="*80)
    print("RAPPORT DE SYNTHÈSE")
    print("="*80)
    
    print("\n1. ÉVAPORATEURS")
    print("-" * 60)
    print(f"  Configuration: {evap.n_effets} effets")
    print(f"  Vapeur de chauffe: {evap.S:.0f} kg/h")
    print(f"  Économie de vapeur: {evap.economie_vapeur():.2f}")
    print(f"  Surface totale: {np.sum(evap.A):.1f} m²")
    print(f"  Concentration finale: {evap.x[-1]*100:.1f}%")
    
    print("\n2. CRISTALLISEUR")
    print("-" * 60)
    print(f"  Volume: {crist_dims['volume']:.2f} m³")
    print(f"  Diamètre: {crist_dims['diametre']:.2f} m")
    print(f"  Hauteur: {crist_dims['hauteur']:.2f} m")
    print(f"  Puissance agitation: {crist_dims['puissance_agitation']:.1f} kW")
    print(f"  Surface serpentin: {crist_dims['surface_serpentin']:.2f} m²")
    
    print("\n3. PERFORMANCES")
    print("-" * 60)
    production = evap.L[-1] * 8000 / 1000
    print(f"  Production annuelle: {production:,.0f} tonnes/an")
    print(f"  Consommation vapeur: {evap.S * 8000 / 1000:,.0f} tonnes/an")
    print(f"  Consommation électrique: ~150 kW")
    
    print("\n4. ÉCONOMIQUE")
    print("-" * 60)
    # Les résultats économiques seraient ici si disponibles
    
    print("\n5. RECOMMANDATIONS")
    print("-" * 60)
    print("  • Configuration optimale: 3 effets")
    print("  • Profil de refroidissement: Contrôlé (sursaturation constante)")
    print("  • Intégration thermique recommandée pour économie d'énergie")
    print("  • Instrumentation et contrôle avancé pour qualité cristaux")
    
    print("\n" + "="*80)


def sauvegarder_resultats(evap, crist_dims):
    """
    Sauvegarde les résultats dans des fichiers Excel.
    """
    print("\n📊 Sauvegarde des résultats...")
    
    # Résultats évaporateurs
    df_evap = pd.DataFrame({
        'Effet': range(1, evap.n_effets + 1),
        'L (kg/h)': evap.L,
        'V (kg/h)': evap.V,
        'x (%)': evap.x * 100,
        'T (°C)': evap.T,
        'P (bar)': evap.P,
        'A (m²)': evap.A
    })
    
    # Résultats cristalliseur
    df_crist = pd.DataFrame({
        'Paramètre': list(crist_dims.keys()),
        'Valeur': list(crist_dims.values()),
        'Unité': ['m³', 'm', 'm', 'kW', 'm²']
    })
    
    # Sauvegarde
    with pd.ExcelWriter('resultats_calculs.xlsx') as writer:
        df_evap.to_excel(writer, sheet_name='Évaporateurs', index=False)
        df_crist.to_excel(writer, sheet_name='Cristalliseur', index=False)
    
    print("✓ Résultats sauvegardés: resultats_calculs.xlsx")


def main():
    """
    Fonction principale - Exécution complète du projet.
    """
    try:
        # En-tête
        afficher_en_tete()
        
        # Partie 1: Évaporation
        evap = partie1_evaporation()
        
        # Partie 2: Cristallisation
        crist, crist_dims = partie2_cristallisation()
        
        # Partie 3: Intégration et optimisation
        resultats_eco = partie3_integration_optimisation(evap, crist_dims)
        
        # Rapport de synthèse
        generer_rapport_synthese(evap, crist_dims, resultats_eco)
        
        # Sauvegarde des résultats
        sauvegarder_resultats(evap, crist_dims)
        
        # Message de fin
        print("\n" + "="*80)
        print("✓ PROJET COMPLÉTÉ AVEC SUCCÈS")
        print("="*80)
        print("\nFichiers générés:")
        print("  • profils_evaporateurs.png")
        print("  • cristallisation_*.png")
        print("  • analyse_*.png")
        print("  • comparaison_economique.png")
        print("  • resultats_calculs.xlsx")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
