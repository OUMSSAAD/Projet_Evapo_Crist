"""
Module Optimisation
Analyses de sensibilité et optimisation technico-économique
Auteur: Projet PIC 2024-2025
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from evaporateurs import EvaporateurMultiplesEffets
from cristallisation import CristalliseurBatch


class AnalyseSensibilite:
    """
    Classe pour réaliser des analyses de sensibilité paramétriques.
    """
    
    def __init__(self):
        """Initialisation."""
        self.resultats = {}
        
    def analyse_nombre_effets(self, n_min=2, n_max=5):
        """
        Analyse l'impact du nombre d'effets.
        
        Args:
            n_min (int): Nombre minimum d'effets
            n_max (int): Nombre maximum d'effets
        """
        print("\n=== ANALYSE: Impact du nombre d'effets ===")
        
        n_effets_range = range(n_min, n_max + 1)
        economies = []
        surfaces_totales = []
        vapeurs_consommees = []
        
        for n in n_effets_range:
            print(f"\nSimulation avec {n} effets...")
            evap = EvaporateurMultiplesEffets(n_effets=n)
            evap.resoudre_bilans()
            
            economies.append(evap.economie_vapeur())
            surfaces_totales.append(np.sum(evap.A))
            vapeurs_consommees.append(evap.S)
        
        # Sauvegarde des résultats
        self.resultats['nombre_effets'] = {
            'n_effets': list(n_effets_range),
            'economie': economies,
            'surface_totale': surfaces_totales,
            'vapeur_consommee': vapeurs_consommees
        }
        
        # Visualisation
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        axes[0].plot(n_effets_range, economies, 'o-', linewidth=2, markersize=10)
        axes[0].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[0].set_ylabel('Économie de vapeur', fontsize=12)
        axes[0].set_title('Économie de vapeur', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(n_effets_range, surfaces_totales, 's-', linewidth=2, 
                    markersize=10, color='green')
        axes[1].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[1].set_ylabel('Surface totale (m²)', fontsize=12)
        axes[1].set_title('Surface d\'échange totale', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(n_effets_range, vapeurs_consommees, '^-', linewidth=2, 
                    markersize=10, color='red')
        axes[2].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[2].set_ylabel('Vapeur consommée (kg/h)', fontsize=12)
        axes[2].set_title('Consommation de vapeur', fontsize=13, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analyse_nombre_effets.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGraphique sauvegardé: analyse_nombre_effets.png")
        
        # Résultats tabulaires
        df = pd.DataFrame(self.resultats['nombre_effets'])
        print("\n" + df.to_string(index=False))
    
    def analyse_pression_vapeur(self, P_min=2.5, P_max=4.5, n_points=10):
        """
        Analyse l'impact de la pression de vapeur de chauffe.
        
        Args:
            P_min (float): Pression minimale (bar)
            P_max (float): Pression maximale (bar)
            n_points (int): Nombre de points
        """
        print("\n=== ANALYSE: Impact de la pression de vapeur ===")
        
        P_range = np.linspace(P_min, P_max, n_points)
        economies = []
        surfaces = []
        temperatures = []
        
        for P in P_range:
            evap = EvaporateurMultiplesEffets(n_effets=3)
            evap.P_vapeur = P
            evap.resoudre_bilans()
            
            economies.append(evap.economie_vapeur())
            surfaces.append(np.sum(evap.A))
            temperatures.append(evap.T[0])  # Température premier effet
        
        # Sauvegarde
        self.resultats['pression_vapeur'] = {
            'pression': P_range,
            'economie': economies,
            'surface': surfaces,
            'temperature_effet1': temperatures
        }
        
        # Visualisation
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        axes[0].plot(P_range, economies, linewidth=2, color='blue')
        axes[0].set_xlabel('Pression vapeur (bar)', fontsize=12)
        axes[0].set_ylabel('Économie de vapeur', fontsize=12)
        axes[0].set_title('Impact sur l\'économie', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(P_range, surfaces, linewidth=2, color='green')
        axes[1].set_xlabel('Pression vapeur (bar)', fontsize=12)
        axes[1].set_ylabel('Surface totale (m²)', fontsize=12)
        axes[1].set_title('Impact sur les surfaces', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(P_range, temperatures, linewidth=2, color='red')
        axes[2].set_xlabel('Pression vapeur (bar)', fontsize=12)
        axes[2].set_ylabel('Température effet 1 (°C)', fontsize=12)
        axes[2].set_title('Impact sur la température', fontsize=13, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analyse_pression_vapeur.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGraphique sauvegardé: analyse_pression_vapeur.png")
    
    def analyse_concentration_finale(self, x_min=60, x_max=70, n_points=10):
        """
        Analyse l'impact de la concentration finale visée.
        
        Args:
            x_min (float): Concentration minimale (%)
            x_max (float): Concentration maximale (%)
            n_points (int): Nombre de points
        """
        print("\n=== ANALYSE: Impact de la concentration finale ===")
        
        x_range = np.linspace(x_min, x_max, n_points)
        vapeurs_totales = []
        surfaces = []
        vapeurs_chauffe = []
        
        for x_final in x_range:
            evap = EvaporateurMultiplesEffets(n_effets=3)
            evap.x_final = x_final / 100  # Conversion en fraction
            evap.resoudre_bilans()
            
            vapeurs_totales.append(np.sum(evap.V))
            surfaces.append(np.sum(evap.A))
            vapeurs_chauffe.append(evap.S)
        
        # Visualisation
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        axes[0].plot(x_range, vapeurs_totales, linewidth=2, color='blue')
        axes[0].set_xlabel('Concentration finale (%)', fontsize=12)
        axes[0].set_ylabel('Vapeur totale produite (kg/h)', fontsize=12)
        axes[0].set_title('Production de vapeur', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(x_range, surfaces, linewidth=2, color='green')
        axes[1].set_xlabel('Concentration finale (%)', fontsize=12)
        axes[1].set_ylabel('Surface totale (m²)', fontsize=12)
        axes[1].set_title('Surfaces d\'échange', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(x_range, vapeurs_chauffe, linewidth=2, color='red')
        axes[2].set_xlabel('Concentration finale (%)', fontsize=12)
        axes[2].set_ylabel('Vapeur de chauffe (kg/h)', fontsize=12)
        axes[2].set_title('Consommation de vapeur', fontsize=13, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analyse_concentration.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGraphique sauvegardé: analyse_concentration.png")
    
    def analyse_debit_alimentation(self, variation=0.20, n_points=10):
        """
        Analyse l'impact du débit d'alimentation (±variation).
        
        Args:
            variation (float): Variation relative (0.20 = ±20%)
            n_points (int): Nombre de points
        """
        print("\n=== ANALYSE: Impact du débit d'alimentation ===")
        
        F_nominal = 20000
        F_range = np.linspace(F_nominal * (1 - variation), 
                            F_nominal * (1 + variation), 
                            n_points)
        
        vapeurs_chauffe = []
        surfaces = []
        economies = []
        
        for F in F_range:
            evap = EvaporateurMultiplesEffets(n_effets=3)
            evap.F = F
            evap.resoudre_bilans()
            
            vapeurs_chauffe.append(evap.S)
            surfaces.append(np.sum(evap.A))
            economies.append(evap.economie_vapeur())
        
        # Visualisation
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        variation_pct = (F_range / F_nominal - 1) * 100
        
        axes[0].plot(variation_pct, vapeurs_chauffe, linewidth=2, color='blue')
        axes[0].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        axes[0].set_xlabel('Variation débit (%)', fontsize=12)
        axes[0].set_ylabel('Vapeur de chauffe (kg/h)', fontsize=12)
        axes[0].set_title('Consommation de vapeur', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(variation_pct, surfaces, linewidth=2, color='green')
        axes[1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        axes[1].set_xlabel('Variation débit (%)', fontsize=12)
        axes[1].set_ylabel('Surface totale (m²)', fontsize=12)
        axes[1].set_title('Surfaces d\'échange', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(variation_pct, economies, linewidth=2, color='red')
        axes[2].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        axes[2].set_xlabel('Variation débit (%)', fontsize=12)
        axes[2].set_ylabel('Économie de vapeur', fontsize=12)
        axes[2].set_title('Économie de vapeur', fontsize=13, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analyse_debit.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGraphique sauvegardé: analyse_debit.png")


class AnalyseEconomique:
    """
    Classe pour l'analyse technico-économique.
    """
    
    def __init__(self):
        """Initialisation avec paramètres économiques."""
        # Coûts d'exploitation
        self.prix_vapeur = 25  # €/tonne
        self.prix_eau = 0.15  # €/m³
        self.prix_electricite = 0.12  # €/kWh
        self.salaire_operateur = 35  # €/h
        
        # Paramètres généraux
        self.heures_fonctionnement = 8000  # h/an
        self.duree_vie = 15  # ans
        self.taux_actualisation = 0.08  # 8%
        
    def cout_investissement_evaporateurs(self, surfaces):
        """
        Calcule le coût d'investissement des évaporateurs.
        
        Args:
            surfaces (array): Surfaces d'échange (m²) pour chaque effet
            
        Returns:
            float: Coût total (€)
        """
        cout_total = 0
        for A in surfaces:
            cout_total += 15000 * (A ** 0.65)
        return cout_total
    
    def cout_investissement_cristalliseur(self, volume):
        """
        Calcule le coût d'investissement du cristalliseur.
        
        Args:
            volume (float): Volume (m³)
            
        Returns:
            float: Coût (€)
        """
        return 25000 * (volume ** 0.6)
    
    def cout_investissement_echangeurs(self, surface):
        """
        Calcule le coût des échangeurs de récupération.
        
        Args:
            surface (float): Surface d'échange (m²)
            
        Returns:
            float: Coût (€)
        """
        return 8000 * (surface ** 0.7)
    
    def TCI(self, evap, crist_dims):
        """
        Calcule le coût total d'investissement (TCI).
        
        Args:
            evap: Instance de EvaporateurMultiplesEffets
            crist_dims: Dictionnaire avec dimensions cristalliseur
            
        Returns:
            float: TCI (€)
        """
        # Coût des équipements
        C_evap = self.cout_investissement_evaporateurs(evap.A)
        C_crist = self.cout_investissement_cristalliseur(crist_dims['volume'])
        C_ech = self.cout_investissement_echangeurs(50)  # Estimation
        
        C_equipements = C_evap + C_crist + C_ech
        
        # Facteurs d'installation
        TCI = C_equipements * 1.55  # +15% instru, +40% install
        
        return TCI
    
    def OPEX_annuel(self, evap, crist_dims):
        """
        Calcule les coûts d'exploitation annuels.
        
        Args:
            evap: Instance de EvaporateurMultiplesEffets
            crist_dims: Dictionnaire avec dimensions cristalliseur
            
        Returns:
            dict: Détail des coûts (€/an)
        """
        # Vapeur
        cout_vapeur = (evap.S * self.heures_fonctionnement * 
                      self.prix_vapeur / 1000)
        
        # Électricité (pompes + agitation)
        P_elec_total = 100 + crist_dims['puissance_agitation']  # kW
        cout_electricite = (P_elec_total * self.heures_fonctionnement * 
                           self.prix_electricite)
        
        # Eau de refroidissement (estimation)
        cout_eau = 10000  # €/an (estimation forfaitaire)
        
        # Main d'œuvre (2 opérateurs par poste, 3 postes)
        cout_MO = self.salaire_operateur * self.heures_fonctionnement * 2
        
        OPEX = {
            'vapeur': cout_vapeur,
            'electricite': cout_electricite,
            'eau': cout_eau,
            'main_oeuvre': cout_MO,
            'total': cout_vapeur + cout_electricite + cout_eau + cout_MO
        }
        
        return OPEX
    
    def analyser_projet(self, n_effets=3):
        """
        Analyse économique complète du projet.
        
        Args:
            n_effets (int): Nombre d'effets
        """
        print("\n" + "="*70)
        print(f"ANALYSE TECHNICO-ÉCONOMIQUE - {n_effets} EFFETS")
        print("="*70)
        
        # Simulation évaporateur
        evap = EvaporateurMultiplesEffets(n_effets=n_effets)
        evap.resoudre_bilans()
        
        # Simulation cristalliseur
        crist = CristalliseurBatch()
        crist_dims = crist.dimensionnement()
        
        # Investissement
        TCI_total = self.TCI(evap, crist_dims)
        print(f"\nINVESTISSEMENT:")
        print(f"  Évaporateurs: {self.cout_investissement_evaporateurs(evap.A):,.0f} €")
        print(f"  Cristalliseur: {self.cout_investissement_cristalliseur(crist_dims['volume']):,.0f} €")
        print(f"  Échangeurs: {self.cout_investissement_echangeurs(50):,.0f} €")
        print(f"  TCI total: {TCI_total:,.0f} €")
        
        # Exploitation
        OPEX = self.OPEX_annuel(evap, crist_dims)
        print(f"\nEXPLOITATION ANNUELLE:")
        print(f"  Vapeur: {OPEX['vapeur']:,.0f} €/an")
        print(f"  Électricité: {OPEX['electricite']:,.0f} €/an")
        print(f"  Eau: {OPEX['eau']:,.0f} €/an")
        print(f"  Main d'œuvre: {OPEX['main_oeuvre']:,.0f} €/an")
        print(f"  OPEX total: {OPEX['total']:,.0f} €/an")
        
        # Maintenance
        maintenance = 0.03 * TCI_total
        print(f"  Maintenance (3% TCI): {maintenance:,.0f} €/an")
        
        # Production
        production_annuelle = evap.L[-1] * self.heures_fonctionnement / 1000  # tonnes/an
        print(f"\nPRODUCTION:")
        print(f"  Production annuelle: {production_annuelle:,.0f} tonnes/an")
        
        # Coût unitaire
        amortissement = TCI_total / self.duree_vie
        cout_total_annuel = OPEX['total'] + maintenance + amortissement
        cout_unitaire = cout_total_annuel / production_annuelle
        print(f"  Coût de production: {cout_unitaire:.2f} €/tonne")
        
        # ROI simplifié (hypothèse prix de vente)
        prix_vente = 800  # €/tonne (hypothèse)
        profit_annuel = (prix_vente - cout_unitaire) * production_annuelle
        ROI = TCI_total / profit_annuel
        print(f"\nRENTABILITÉ:")
        print(f"  Prix de vente (hypothèse): {prix_vente} €/tonne")
        print(f"  Profit annuel: {profit_annuel:,.0f} €/an")
        print(f"  ROI simple: {ROI:.2f} ans")
        
        # VAN
        VAN = self.calculer_VAN(TCI_total, profit_annuel)
        print(f"  VAN (15 ans, 8%): {VAN:,.0f} €")
        
        if VAN > 0:
            print(f"\n✓ Projet RENTABLE (VAN > 0)")
        else:
            print(f"\n✗ Projet NON RENTABLE (VAN < 0)")
        
        print("="*70)
        
        return {
            'TCI': TCI_total,
            'OPEX': OPEX['total'],
            'production': production_annuelle,
            'cout_unitaire': cout_unitaire,
            'ROI': ROI,
            'VAN': VAN
        }
    
    def calculer_VAN(self, TCI, flux_annuel):
        """
        Calcule la valeur actuelle nette.
        
        Args:
            TCI (float): Investissement initial
            flux_annuel (float): Flux de trésorerie annuel
            
        Returns:
            float: VAN (€)
        """
        VAN = -TCI
        for i in range(1, self.duree_vie + 1):
            VAN += flux_annuel / ((1 + self.taux_actualisation) ** i)
        return VAN
    
    def comparer_configurations(self):
        """
        Compare différentes configurations (nombre d'effets).
        """
        print("\n" + "="*70)
        print("COMPARAISON DES CONFIGURATIONS")
        print("="*70)
        
        resultats = []
        for n in [2, 3, 4, 5]:
            res = self.analyser_projet(n_effets=n)
            res['n_effets'] = n
            resultats.append(res)
        
        # Tableau récapitulatif
        df = pd.DataFrame(resultats)
        df = df[['n_effets', 'TCI', 'OPEX', 'cout_unitaire', 'ROI', 'VAN']]
        
        print("\n" + df.to_string(index=False))
        
        # Visualisation
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        axes[0].bar(df['n_effets'], df['TCI']/1e6, color='steelblue', edgecolor='black')
        axes[0].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[0].set_ylabel('TCI (M€)', fontsize=12)
        axes[0].set_title('Investissement', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        
        axes[1].plot(df['n_effets'], df['cout_unitaire'], 'o-', 
                    linewidth=2, markersize=10, color='green')
        axes[1].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[1].set_ylabel('Coût (€/tonne)', fontsize=12)
        axes[1].set_title('Coût de production unitaire', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        axes[2].bar(df['n_effets'], df['VAN']/1e6, color='orange', edgecolor='black')
        axes[2].set_xlabel('Nombre d\'effets', fontsize=12)
        axes[2].set_ylabel('VAN (M€)', fontsize=12)
        axes[2].set_title('Valeur actuelle nette', fontsize=13, fontweight='bold')
        axes[2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('comparaison_economique.png', 
                   dpi=300, bbox_inches='tight')
        print("\nGraphique sauvegardé: comparaison_economique.png")
        
        # Recommandation
        meilleur_idx = df['VAN'].idxmax()
        meilleur = df.loc[meilleur_idx]
        print(f"\nCONFIGURATION OPTIMALE: {int(meilleur['n_effets'])} effets")
        print(f"  VAN: {meilleur['VAN']:,.0f} €")
        print(f"  ROI: {meilleur['ROI']:.2f} ans")


if __name__ == "__main__":
    # Tests
    print("=== Module Optimisation ===")
    
    # Analyse de sensibilité
    analyse = AnalyseSensibilite()
    analyse.analyse_nombre_effets()
    # analyse.analyse_pression_vapeur()
    # analyse.analyse_concentration_finale()
    # analyse.analyse_debit_alimentation()
    
    # Analyse économique
    # eco = AnalyseEconomique()
    # eco.comparer_configurations()
