"""
Module Thermodynamique
Calcul des propriétés physico-chimiques pour l'évaporation et la cristallisation
Auteur: Projet PIC 2024-2025
"""

import numpy as np
from CoolProp.CoolProp import PropsSI


class ProprietesThermodynamiques:
    """
    Classe pour calculer les propriétés thermodynamiques de l'eau, 
    de la vapeur et des solutions de saccharose.
    """
    
    def __init__(self):
        """Initialisation avec constantes physiques."""
        self.R = 8.314  # J/(mol·K)
        self.Cp_eau = 4180.0  # J/(kg·K)
        self.Cp_saccharose = 1250.0  # J/(kg·K)
        
    def temperature_saturation(self, P_bar):
        """
        Calcule la température de saturation de l'eau pure.
        
        Args:
            P_bar (float): Pression en bar
            
        Returns:
            float: Température de saturation en °C
            
        Example:
            >>> thermo = ProprietesThermodynamiques()
            >>> T = thermo.temperature_saturation(3.5)
            >>> print(f"T_sat = {T:.2f} °C")
        """
        try:
            P_Pa = P_bar * 1e5
            T_K = PropsSI('T', 'P', P_Pa, 'Q', 0, 'Water')
            T_C = T_K - 273.15
            return T_C
        except Exception as e:
            raise ValueError(f"Erreur calcul température saturation: {e}")
    
    def chaleur_latente(self, P_bar):
        """
        Calcule la chaleur latente de vaporisation.
        
        Args:
            P_bar (float): Pression en bar
            
        Returns:
            float: Chaleur latente en J/kg
        """
        try:
            P_Pa = P_bar * 1e5
            h_vap = PropsSI('H', 'P', P_Pa, 'Q', 1, 'Water')
            h_liq = PropsSI('H', 'P', P_Pa, 'Q', 0, 'Water')
            lambda_vap = h_vap - h_liq
            return lambda_vap
        except Exception as e:
            raise ValueError(f"Erreur calcul chaleur latente: {e}")
    
    def enthalpie_liquide(self, T_C, P_bar):
        """
        Calcule l'enthalpie du liquide.
        
        Args:
            T_C (float): Température en °C
            P_bar (float): Pression en bar
            
        Returns:
            float: Enthalpie en J/kg
        """
        try:
            T_K = T_C + 273.15
            P_Pa = P_bar * 1e5
            h = PropsSI('H', 'T', T_K, 'P', P_Pa, 'Water')
            return h
        except Exception as e:
            raise ValueError(f"Erreur calcul enthalpie liquide: {e}")
    
    def enthalpie_vapeur(self, T_C, P_bar):
        """
        Calcule l'enthalpie de la vapeur saturée.
        
        Args:
            T_C (float): Température en °C
            P_bar (float): Pression en bar
            
        Returns:
            float: Enthalpie en J/kg
        """
        try:
            P_Pa = P_bar * 1e5
            h = PropsSI('H', 'P', P_Pa, 'Q', 1, 'Water')
            return h
        except Exception as e:
            raise ValueError(f"Erreur calcul enthalpie vapeur: {e}")
    
    def EPE_saccharose(self, x_percent):
        """
        Calcule l'élévation du point d'ébullition (EPE) selon Dühring.
        
        Args:
            x_percent (float): Concentration en saccharose (% massique)
            
        Returns:
            float: EPE en °C
            
        Example:
            >>> thermo = ProprietesThermodynamiques()
            >>> EPE = thermo.EPE_saccharose(65)
            >>> print(f"EPE = {EPE:.2f} °C")
        """
        if x_percent < 50:
            A = 0.03
            B = 0.00015
        else:
            A = 0.045
            B = 0.0003
        
        EPE = A * x_percent + B * x_percent**2
        return EPE
    
    def temperature_ebullition_solution(self, P_bar, x_percent):
        """
        Calcule la température d'ébullition de la solution de saccharose.
        
        Args:
            P_bar (float): Pression en bar
            x_percent (float): Concentration en saccharose (% massique)
            
        Returns:
            float: Température d'ébullition en °C
        """
        T_sat = self.temperature_saturation(P_bar)
        EPE = self.EPE_saccharose(x_percent)
        T_eb = T_sat + EPE
        return T_eb
    
    def capacite_calorifique_solution(self, x_massique):
        """
        Calcule la capacité calorifique d'une solution de saccharose.
        
        Args:
            x_massique (float): Fraction massique de saccharose (0-1)
            
        Returns:
            float: Capacité calorifique en J/(kg·K)
        """
        Cp = (1 - x_massique) * self.Cp_eau + x_massique * self.Cp_saccharose
        return Cp
    
    def masse_volumique_solution(self, x_massique, T_C):
        """
        Calcule la masse volumique d'une solution de saccharose.
        
        Args:
            x_massique (float): Fraction massique de saccharose (0-1)
            T_C (float): Température en °C
            
        Returns:
            float: Masse volumique en kg/m³
        """
        rho = 1000 + 400 * x_massique - 0.3 * T_C
        return rho
    
    def solubilite_saccharose(self, T_C):
        """
        Calcule la solubilité du saccharose selon corrélation polynomiale.
        
        Args:
            T_C (float): Température en °C
            
        Returns:
            float: Solubilité C* en g saccharose/100g solution
        """
        C_star = (64.18 + 
                  0.1337 * T_C + 
                  5.52e-3 * T_C**2 - 
                  9.73e-6 * T_C**3)
        return C_star
    
    def sursaturation_relative(self, C, T_C):
        """
        Calcule la sursaturation relative.
        
        Args:
            C (float): Concentration en g/100g solution
            T_C (float): Température en °C
            
        Returns:
            float: Sursaturation relative S (sans dimension)
        """
        C_star = self.solubilite_saccharose(T_C)
        S = (C - C_star) / C_star
        return S


def test_thermodynamique():
    """Tests unitaires du module thermodynamique."""
    thermo = ProprietesThermodynamiques()
    
    print("=== Tests du module thermodynamique ===\n")
    
    # Test 1: Température de saturation
    print("Test 1: Température de saturation")
    T_sat = thermo.temperature_saturation(3.5)
    print(f"T_sat(3.5 bar) = {T_sat:.2f} °C (attendu: ~138.9 °C)")
    assert abs(T_sat - 138.9) < 1.0, "Erreur température saturation"
    
    # Test 2: Chaleur latente
    print("\nTest 2: Chaleur latente")
    lambda_vap = thermo.chaleur_latente(3.5)
    print(f"λ(3.5 bar) = {lambda_vap/1e6:.2f} MJ/kg (attendu: ~2.15 MJ/kg)")
    
    # Test 3: EPE
    print("\nTest 3: Élévation du point d'ébullition")
    EPE = thermo.EPE_saccharose(65)
    print(f"EPE(65%) = {EPE:.2f} °C (attendu: ~4.2 °C)")
    
    # Test 4: Solubilité
    print("\nTest 4: Solubilité du saccharose")
    C_star = thermo.solubilite_saccharose(60)
    print(f"C*(60°C) = {C_star:.2f} g/100g")
    
    # Test 5: Capacité calorifique
    print("\nTest 5: Capacité calorifique")
    Cp = thermo.capacite_calorifique_solution(0.65)
    print(f"Cp(65%) = {Cp:.1f} J/(kg·K)")
    
    print("\n=== Tous les tests passés avec succès ===")


if __name__ == "__main__":
    test_thermodynamique()
