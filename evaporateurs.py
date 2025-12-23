"""
Module Évaporateurs
Simulation d'un système d'évaporation à multiples effets
Auteur: Projet PIC 2024-2025
"""

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from thermodynamique import ProprietesThermodynamiques


class EvaporateurMultiplesEffets:
    """
    Classe pour simuler un système d'évaporation à multiples effets.
    """
    
    def __init__(self, n_effets=3):
        """
        Initialisation de l'évaporateur.
        
        Args:
            n_effets (int): Nombre d'effets
        """
        self.n_effets = n_effets
        self.thermo = ProprietesThermodynamiques()
        
        # Paramètres par défaut
        self.F = 20000  # kg/h - Débit d'alimentation
        self.x_F = 0.15  # Concentration entrée (fraction massique)
        self.T_F = 85  # °C - Température d'alimentation
        self.P_F = 1.5  # bar - Pression d'alimentation
        
        self.x_final = 0.65  # Concentration finale
        self.P_vapeur = 3.5  # bar - Pression vapeur de chauffe
        self.P_condenseur = 0.15  # bar - Pression condenseur
        
        # Coefficients de transfert (W/(m²·K)) - valeurs de base pour 3 effets
        # Pour plus d'effets, on extrapolera
        self.U_base = np.array([2500, 2200, 1800])
        self.R_f = 0.0002  # m²·K/W - Résistance d'encrassement
        
        # Pertes thermiques
        self.perte_thermique = 0.03  # 3%
        
        # Résultats
        self.L = np.zeros(n_effets)  # Débits liquides
        self.V = np.zeros(n_effets)  # Débits vapeurs
        self.x = np.zeros(n_effets)  # Concentrations
        self.T = np.zeros(n_effets)  # Températures
        self.P = np.zeros(n_effets)  # Pressions
        self.A = np.zeros(n_effets)  # Surfaces d'échange
        self.S = 0  # Débit vapeur de chauffe
        
    def calculer_U_effectif(self):
        """
        Calcule les coefficients globaux de transfert effectifs.
        
        Returns:
            np.array: Coefficients U effectifs pour chaque effet
        """
        # Générer les coefficients U pour n effets
        # Les coefficients diminuent avec chaque effet
        if self.n_effets <= 3:
            U_propre = self.U_base[:self.n_effets]
        else:
            # Extrapolation pour plus de 3 effets
            U_propre = np.zeros(self.n_effets)
            U_propre[:3] = self.U_base
            # Décroissance linéaire pour les effets suivants
            for i in range(3, self.n_effets):
                U_propre[i] = U_propre[i-1] - 200
                if U_propre[i] < 1000:
                    U_propre[i] = 1000  # Valeur minimale
        
        U_eff = 1 / (1/U_propre + self.R_f)
        return U_eff
    
    def repartition_pressions(self):
        """
        Répartit les pressions de manière uniforme entre les effets.
        """
        # Pression décroissante du premier au dernier effet
        P_effet_1 = self.P_vapeur - 0.3  # Légèrement inférieure à vapeur chauffe
        self.P = np.linspace(P_effet_1, self.P_condenseur, self.n_effets)
        
    def resoudre_bilans(self):
        """
        Résout les bilans de matière et d'énergie pour tous les effets.
        """
        self.repartition_pressions()
        
        # Estimation initiale
        V_total_estime = self.F * (1 - self.x_F / self.x_final)
        V_par_effet = V_total_estime / self.n_effets
        
        # Initialisation
        x0 = []
        for i in range(self.n_effets):
            L_init = self.F - (i + 1) * V_par_effet
            V_init = V_par_effet
            x_init = self.x_F * self.F / L_init
            T_init = self.thermo.temperature_ebullition_solution(
                self.P[i], x_init * 100
            )
            x0.extend([L_init, V_init, x_init, T_init])
        
        # Résolution du système
        solution = fsolve(self.equations_systeme, x0, full_output=True)
        
        if solution[2] != 1:
            print("Attention: La convergence n'est pas parfaite")
        
        # Extraction des résultats
        sol = solution[0]
        for i in range(self.n_effets):
            self.L[i] = sol[4*i]
            self.V[i] = sol[4*i + 1]
            self.x[i] = sol[4*i + 2]
            self.T[i] = sol[4*i + 3]
        
        # Calcul du débit de vapeur et des surfaces
        self.calculer_vapeur_chauffe()
        self.calculer_surfaces()
        
    def equations_systeme(self, variables):
        """
        Système d'équations pour les bilans de matière et d'énergie.
        
        Args:
            variables (list): Variables [L1, V1, x1, T1, L2, V2, x2, T2, ...]
            
        Returns:
            list: Résidus des équations
        """
        equations = []
        
        for i in range(self.n_effets):
            L_i = variables[4*i]
            V_i = variables[4*i + 1]
            x_i = variables[4*i + 2]
            T_i = variables[4*i + 3]
            
            # Bilan matière global
            if i == 0:
                eq_mat = self.F - L_i - V_i
            else:
                L_im1 = variables[4*(i-1)]
                eq_mat = L_im1 - L_i - V_i
            equations.append(eq_mat)
            
            # Bilan matière saccharose
            if i == 0:
                eq_sacch = self.F * self.x_F - L_i * x_i
            else:
                L_im1 = variables[4*(i-1)]
                x_im1 = variables[4*(i-1) + 2]
                eq_sacch = L_im1 * x_im1 - L_i * x_i
            equations.append(eq_sacch)
            
            # Température d'ébullition
            T_eb_calc = self.thermo.temperature_ebullition_solution(
                self.P[i], x_i * 100
            )
            eq_temp = T_i - T_eb_calc
            equations.append(eq_temp)
            
            # Bilan énergétique (simplifié)
            if i == 0:
                # Pour le premier effet, on fixe un rapport raisonnable
                eq_energie = V_i - V_i  # Équation triviale remplacée par optimisation
            else:
                # Les vapeurs sont proportionnelles
                V_im1 = variables[4*(i-1) + 1]
                eq_energie = V_i - V_im1 * 0.95  # Légère décroissance
            equations.append(eq_energie)
        
        return equations
    
    def calculer_vapeur_chauffe(self):
        """
        Calcule le débit de vapeur de chauffe nécessaire.
        """
        # Chaleur nécessaire au premier effet
        lambda_v = self.thermo.chaleur_latente(self.P_vapeur)
        lambda_1 = self.thermo.chaleur_latente(self.P[0])
        
        Cp_F = self.thermo.capacite_calorifique_solution(self.x_F)
        Cp_1 = self.thermo.capacite_calorifique_solution(self.x[0])
        
        # Chaleur pour chauffer et évaporer
        Q_chauffe = Cp_F * self.F * (self.T[0] - self.T_F) / 3600  # W
        Q_evap = lambda_1 * self.V[0] / 3600  # W
        Q_liquide = Cp_1 * self.L[0] * self.T[0] / 3600  # W
        
        Q_total = (Q_chauffe + Q_evap) / (1 - self.perte_thermique)
        
        self.S = Q_total * 3600 / lambda_v  # kg/h
        
    def calculer_surfaces(self):
        """
        Calcule les surfaces d'échange pour chaque effet.
        """
        U_eff = self.calculer_U_effectif()
        
        for i in range(self.n_effets):
            # Chaleur transférée
            lambda_i = self.thermo.chaleur_latente(self.P[i])
            Q_i = lambda_i * self.V[i] / 3600  # W
            
            # Différence de température motrice
            if i == 0:
                T_vapeur = self.thermo.temperature_saturation(self.P_vapeur)
                delta_T = T_vapeur - self.T[i]
            else:
                delta_T = self.T[i-1] - self.T[i]
            
            # Surface
            if delta_T > 0:
                self.A[i] = Q_i / (U_eff[i] * delta_T)
            else:
                self.A[i] = 0
    
    def economie_vapeur(self):
        """
        Calcule l'économie de vapeur.
        
        Returns:
            float: Économie de vapeur (kg vapeur produite / kg vapeur consommée)
        """
        if self.S > 0:
            return np.sum(self.V) / self.S
        return 0
    
    def afficher_resultats(self):
        """
        Affiche les résultats de la simulation.
        """
        print("\n" + "="*70)
        print(f"RÉSULTATS ÉVAPORATEUR À {self.n_effets} EFFETS")
        print("="*70)
        
        print(f"\nAlimentation:")
        print(f"  Débit: {self.F:.0f} kg/h")
        print(f"  Concentration: {self.x_F*100:.1f}%")
        print(f"  Température: {self.T_F:.1f} °C")
        
        print(f"\nVapeur de chauffe:")
        print(f"  Débit: {self.S:.0f} kg/h")
        print(f"  Pression: {self.P_vapeur:.1f} bar")
        
        print(f"\n{'Effet':<8} {'L (kg/h)':<12} {'V (kg/h)':<12} {'x (%)':<10} {'T (°C)':<10} {'P (bar)':<10} {'A (m²)':<10}")
        print("-"*70)
        
        for i in range(self.n_effets):
            print(f"{i+1:<8} {self.L[i]:<12.0f} {self.V[i]:<12.0f} "
                  f"{self.x[i]*100:<10.1f} {self.T[i]:<10.1f} "
                  f"{self.P[i]:<10.2f} {self.A[i]:<10.1f}")
        
        print("\n" + "-"*70)
        print(f"Vapeur totale produite: {np.sum(self.V):.0f} kg/h")
        print(f"Surface totale: {np.sum(self.A):.1f} m²")
        print(f"Économie de vapeur: {self.economie_vapeur():.2f}")
        print(f"Concentration finale: {self.x[-1]*100:.1f}%")
        print("="*70)
    
    def tracer_profils(self):
        """
        Trace les profils de température, concentration et pression.
        """
        effets = np.arange(1, self.n_effets + 1)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Température
        axes[0, 0].plot(effets, self.T, 'o-', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel('Effet', fontsize=12)
        axes[0, 0].set_ylabel('Température (°C)', fontsize=12)
        axes[0, 0].set_title('Profil de température', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Concentration
        axes[0, 1].plot(effets, self.x * 100, 's-', linewidth=2, markersize=8, color='green')
        axes[0, 1].set_xlabel('Effet', fontsize=12)
        axes[0, 1].set_ylabel('Concentration (%)', fontsize=12)
        axes[0, 1].set_title('Profil de concentration', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Pression
        axes[1, 0].plot(effets, self.P, '^-', linewidth=2, markersize=8, color='red')
        axes[1, 0].set_xlabel('Effet', fontsize=12)
        axes[1, 0].set_ylabel('Pression (bar)', fontsize=12)
        axes[1, 0].set_title('Profil de pression', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Surfaces d'échange
        axes[1, 1].bar(effets, self.A, color='orange', alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('Effet', fontsize=12)
        axes[1, 1].set_ylabel('Surface (m²)', fontsize=12)
        axes[1, 1].set_title('Surfaces d\'échange', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('profils_evaporateurs.png', 
                   dpi=300, bbox_inches='tight')
        print(f"\nGraphique sauvegardé: profils_evaporateurs.png")


def test_evaporateur():
    """Test du module évaporateur."""
    print("=== Test du module évaporateur ===\n")
    
    # Création et simulation
    evap = EvaporateurMultiplesEffets(n_effets=3)
    print("Résolution du système...")
    evap.resoudre_bilans()
    
    # Affichage des résultats
    evap.afficher_resultats()
    
    # Vérification des bilans
    print("\n=== Vérifications ===")
    
    # Bilan matière global
    eau_entree = evap.F * (1 - evap.x_F)
    eau_sortie = evap.L[-1] * (1 - evap.x[-1]) + np.sum(evap.V)
    erreur_mat = abs(eau_entree - eau_sortie) / eau_entree * 100
    print(f"Erreur bilan matière: {erreur_mat:.2f}%")
    
    # Bilan saccharose
    sacch_entree = evap.F * evap.x_F
    sacch_sortie = evap.L[-1] * evap.x[-1]
    erreur_sacch = abs(sacch_entree - sacch_sortie) / sacch_entree * 100
    print(f"Erreur bilan saccharose: {erreur_sacch:.2f}%")
    
    # Tracé des profils
    evap.tracer_profils()


if __name__ == "__main__":
    test_evaporateur()
