"""
Module Cristallisation
Modélisation de la cinétique de cristallisation et du bilan de population
Auteur: Projet PIC 2024-2025
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from thermodynamique import ProprietesThermodynamiques


class CristalliseurBatch:
    """
    Classe pour simuler un cristalliseur batch avec refroidissement.
    """
    
    def __init__(self):
        """Initialisation du cristalliseur."""
        self.thermo = ProprietesThermodynamiques()
        
        # Paramètres cinétiques
        self.k_b = 1.5e10  # noyaux/(m³·s) - Constante de nucléation
        self.b = 2.5  # Ordre de nucléation
        self.j = 0.5  # Ordre par rapport à la suspension
        
        self.k_g = 2.8e-7  # m/s - Constante de croissance
        self.g = 1.5  # Ordre de croissance
        self.E_g = 45000  # J/mol - Énergie d'activation
        
        # Paramètres du procédé
        self.T_0 = 70  # °C - Température initiale
        self.T_f = 35  # °C - Température finale
        self.duree = 4 * 3600  # s - Durée de batch (4 heures)
        self.C_0 = 75  # g/100g - Concentration initiale
        
        self.masse_batch = 5000  # kg - Masse de sirop
        self.V_cristalliseur = 0  # m³ - Volume (à calculer)
        
        # Résultats
        self.temps = None
        self.temperature = None
        self.concentration = None
        self.sursaturation = None
        self.moments = None
        self.L_50 = 0  # Taille moyenne finale
        self.CV = 0  # Coefficient de variation
        
    def vitesse_nucleation(self, S, m_T):
        """
        Calcule le taux de nucléation.
        
        Args:
            S (float): Sursaturation relative
            m_T (float): Masse de cristaux suspendus (kg/m³)
            
        Returns:
            float: Taux de nucléation B (noyaux/(m³·s))
        """
        if S <= 0:
            return 0
        B = self.k_b * (S ** self.b) * (m_T ** self.j)
        return B
    
    def vitesse_croissance(self, S, T_K):
        """
        Calcule la vitesse de croissance linéaire.
        
        Args:
            S (float): Sursaturation relative
            T_K (float): Température en Kelvin
            
        Returns:
            float: Vitesse de croissance G (m/s)
        """
        if S <= 0:
            return 0
        
        terme_exp = np.exp(-self.E_g / (self.thermo.R * T_K))
        G = self.k_g * (S ** self.g) * terme_exp
        return G
    
    def profil_temperature_lineaire(self, t):
        """
        Profil de température linéaire.
        
        Args:
            t (float): Temps en secondes
            
        Returns:
            float: Température en °C
        """
        alpha = (self.T_0 - self.T_f) / self.duree
        T = self.T_0 - alpha * t
        return T
    
    def profil_temperature_exponentiel(self, t, beta=0.0003):
        """
        Profil de température exponentiel.
        
        Args:
            t (float): Temps en secondes
            beta (float): Constante de temps (s⁻¹)
            
        Returns:
            float: Température en °C
        """
        T = self.T_f + (self.T_0 - self.T_f) * np.exp(-beta * t)
        return T
    
    def profil_temperature_optimal(self, t, S_target=0.05):
        """
        Profil de température maintenant sursaturation constante.
        
        Args:
            t (float): Temps en secondes
            S_target (float): Sursaturation cible
            
        Returns:
            float: Température en °C
        """
        # Simplification: décroissance contrôlée
        # Dans une implémentation réelle, cela nécessiterait un contrôleur
        progression = t / self.duree
        T = self.T_0 - (self.T_0 - self.T_f) * progression**0.8
        return T
    
    def equations_bilan_population(self, y, t, profil_temp='lineaire'):
        """
        Système d'équations différentielles pour le bilan de population.
        
        Args:
            y (array): Vecteur d'état [m0, m1, m2, m3, C]
            t (float): Temps
            profil_temp (str): Type de profil de température
            
        Returns:
            array: Dérivées [dm0/dt, dm1/dt, dm2/dt, dm3/dt, dC/dt]
        """
        m0, m1, m2, m3, C = y
        
        # Température selon le profil choisi
        if profil_temp == 'lineaire':
            T_C = self.profil_temperature_lineaire(t)
        elif profil_temp == 'exponentiel':
            T_C = self.profil_temperature_exponentiel(t)
        else:  # optimal
            T_C = self.profil_temperature_optimal(t)
        
        T_K = T_C + 273.15
        
        # Sursaturation
        S = self.thermo.sursaturation_relative(C, T_C)
        
        # Masse volumique des cristaux (approximation)
        rho_cristaux = 1500  # kg/m³
        m_T = m3 * rho_cristaux if m3 > 0 else 1e-6
        
        # Cinétiques
        B = self.vitesse_nucleation(S, m_T)
        G = self.vitesse_croissance(S, T_K)
        
        # Dérivées des moments
        dm0_dt = B
        dm1_dt = G * m0
        dm2_dt = 2 * G * m1
        dm3_dt = 3 * G * m2
        
        # Bilan de matière sur le saccharose
        # Masse de cristaux formés
        k_v = np.pi / 6  # Facteur de forme (sphères)
        masse_cristaux_kg = k_v * rho_cristaux * m3 * self.V_cristalliseur
        
        # Concentration en solution (simplification)
        masse_solution = self.masse_batch
        C_solution = (C * masse_solution - masse_cristaux_kg * 100) / masse_solution
        dC_dt = -3 * k_v * rho_cristaux * G * m2 / masse_solution * 100
        
        return [dm0_dt, dm1_dt, dm2_dt, dm3_dt, dC_dt]
    
    def simuler(self, profil='lineaire', n_points=1000):
        """
        Simule la cristallisation batch.
        
        Args:
            profil (str): Type de profil ('lineaire', 'exponentiel', 'optimal')
            n_points (int): Nombre de points de temps
        """
        print(f"\nSimulation avec profil {profil}...")
        
        # Estimation du volume du cristalliseur
        rho_sirop = 1300  # kg/m³ (approximation)
        self.V_cristalliseur = self.masse_batch / rho_sirop
        
        # Temps
        self.temps = np.linspace(0, self.duree, n_points)
        
        # Conditions initiales [m0, m1, m2, m3, C]
        # On commence avec quelques germes
        y0 = [1e6, 1e-3, 1e-9, 1e-15, self.C_0]
        
        # Résolution
        solution = odeint(self.equations_bilan_population, y0, self.temps,
                         args=(profil,), rtol=1e-6, atol=1e-8)
        
        self.moments = solution[:, :-1]
        self.concentration = solution[:, -1]
        
        # Calcul de la température et sursaturation
        self.temperature = np.zeros(n_points)
        self.sursaturation = np.zeros(n_points)
        
        for i, t in enumerate(self.temps):
            if profil == 'lineaire':
                self.temperature[i] = self.profil_temperature_lineaire(t)
            elif profil == 'exponentiel':
                self.temperature[i] = self.profil_temperature_exponentiel(t)
            else:
                self.temperature[i] = self.profil_temperature_optimal(t)
            
            self.sursaturation[i] = self.thermo.sursaturation_relative(
                self.concentration[i], self.temperature[i]
            )
        
        # Calcul des caractéristiques finales
        m0_final = self.moments[-1, 0]
        m1_final = self.moments[-1, 1]
        m2_final = self.moments[-1, 2]
        
        if m0_final > 0:
            self.L_50 = m1_final / m0_final  # m
            
            # Calcul du coefficient de variation
            L_mean = self.L_50
            variance = m2_final / m0_final - L_mean**2
            if variance > 0:
                sigma = np.sqrt(variance)
                self.CV = (sigma / L_mean) * 100
            else:
                self.CV = 0
        
        print(f"  Taille moyenne L50: {self.L_50*1e6:.1f} µm")
        print(f"  Coefficient de variation CV: {self.CV:.1f}%")
        print(f"  Concentration finale: {self.concentration[-1]:.2f} g/100g")
    
    def tracer_resultats(self, titre_supplement=''):
        """
        Trace les résultats de la simulation.
        
        Args:
            titre_supplement (str): Complément au titre
        """
        temps_h = self.temps / 3600
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Température
        axes[0, 0].plot(temps_h, self.temperature, linewidth=2, color='red')
        axes[0, 0].set_xlabel('Temps (h)', fontsize=12)
        axes[0, 0].set_ylabel('Température (°C)', fontsize=12)
        axes[0, 0].set_title('Profil de température', fontsize=13, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Sursaturation
        axes[0, 1].plot(temps_h, self.sursaturation, linewidth=2, color='blue')
        axes[0, 1].axhline(y=0.02, color='green', linestyle='--', 
                          label='Zone métastable')
        axes[0, 1].axhline(y=0.10, color='orange', linestyle='--', 
                          label='Nucléation primaire')
        axes[0, 1].set_xlabel('Temps (h)', fontsize=12)
        axes[0, 1].set_ylabel('Sursaturation S', fontsize=12)
        axes[0, 1].set_title('Sursaturation relative', fontsize=13, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Moments
        axes[1, 0].semilogy(temps_h, self.moments[:, 0], label='m₀ (nombre)')
        axes[1, 0].semilogy(temps_h, self.moments[:, 3]*1e15, label='m₃×10¹⁵ (volume)')
        axes[1, 0].set_xlabel('Temps (h)', fontsize=12)
        axes[1, 0].set_ylabel('Moments', fontsize=12)
        axes[1, 0].set_title('Évolution des moments', fontsize=13, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Taille moyenne
        L_mean = np.zeros(len(self.temps))
        for i in range(len(self.temps)):
            if self.moments[i, 0] > 0:
                L_mean[i] = self.moments[i, 1] / self.moments[i, 0] * 1e6  # µm
        
        axes[1, 1].plot(temps_h, L_mean, linewidth=2, color='green')
        axes[1, 1].set_xlabel('Temps (h)', fontsize=12)
        axes[1, 1].set_ylabel('Taille moyenne (µm)', fontsize=12)
        axes[1, 1].set_title('Évolution de la taille moyenne', fontsize=13, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(f'Cristallisation - {titre_supplement}', 
                    fontsize=15, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        nom_fichier = f'cristallisation_{titre_supplement.replace(" ", "_")}.png'
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')
        print(f"\nGraphique sauvegardé: {nom_fichier}")
    
    def dimensionnement(self):
        """
        Dimensionne le cristalliseur.
        """
        print("\n=== DIMENSIONNEMENT DU CRISTALLISEUR ===")
        
        # Volume
        rho_sirop = 1300  # kg/m³
        V = self.masse_batch / rho_sirop
        print(f"Volume requis: {V:.2f} m³")
        
        # Dimensions (cylindrique avec H/D = 1.5)
        H_sur_D = 1.5
        D = (4 * V / (np.pi * H_sur_D)) ** (1/3)
        H = H_sur_D * D
        print(f"Diamètre: {D:.2f} m")
        print(f"Hauteur: {H:.2f} m")
        
        # Puissance d'agitation (corrélation empirique)
        N = 60 / 60  # 60 rpm en Hz
        D_agitateur = D / 3  # Diamètre agitateur = D/3
        Np = 5  # Nombre de puissance (estimation)
        rho = 1300  # kg/m³
        P_agitation = Np * rho * N**3 * D_agitateur**5
        print(f"Puissance d'agitation: {P_agitation/1000:.1f} kW")
        
        # Serpentin de refroidissement
        Q_refroidissement = self.masse_batch * 2300 * (self.T_0 - self.T_f) / self.duree  # W
        U_serpentin = 500  # W/(m²·K) - Coefficient de transfert
        delta_T_ml = 15  # K - Différence de température moyenne logarithmique
        A_serpentin = Q_refroidissement / (U_serpentin * delta_T_ml)
        print(f"Surface serpentin de refroidissement: {A_serpentin:.2f} m²")
        
        # Temps de résidence
        tau = self.duree / 3600  # heures
        print(f"Temps de résidence: {tau:.1f} h")
        
        return {
            'volume': V,
            'diametre': D,
            'hauteur': H,
            'puissance_agitation': P_agitation/1000,
            'surface_serpentin': A_serpentin
        }


def comparer_profils():
    """
    Compare les trois profils de refroidissement.
    """
    print("\n" + "="*70)
    print("COMPARAISON DES PROFILS DE REFROIDISSEMENT")
    print("="*70)
    
    profils = ['lineaire', 'exponentiel', 'optimal']
    resultats = []
    
    for profil in profils:
        crist = CristalliseurBatch()
        crist.simuler(profil=profil, n_points=500)
        crist.tracer_resultats(titre_supplement=f'Profil {profil}')
        
        resultats.append({
            'profil': profil,
            'L50': crist.L_50 * 1e6,  # µm
            'CV': crist.CV,
            'C_finale': crist.concentration[-1]
        })
    
    # Tableau comparatif
    print("\n" + "="*70)
    print(f"{'Profil':<15} {'L50 (µm)':<15} {'CV (%)':<15} {'C finale (g/100g)':<20}")
    print("-"*70)
    for r in resultats:
        print(f"{r['profil']:<15} {r['L50']:<15.1f} {r['CV']:<15.1f} {r['C_finale']:<20.2f}")
    print("="*70)
    
    # Recommandation
    print("\nRECOMMANDATION:")
    meilleur_idx = np.argmin([r['CV'] for r in resultats])
    meilleur = resultats[meilleur_idx]
    print(f"Le profil '{meilleur['profil']}' donne la distribution la plus uniforme")
    print(f"avec CV = {meilleur['CV']:.1f}% et L50 = {meilleur['L50']:.1f} µm")


if __name__ == "__main__":
    # Test avec un profil
    print("=== Test du module cristallisation ===")
    
    crist = CristalliseurBatch()
    crist.simuler(profil='lineaire', n_points=500)
    crist.tracer_resultats(titre_supplement='Profil linéaire')
    crist.dimensionnement()
    
    # Comparaison des profils
    # comparer_profils()
