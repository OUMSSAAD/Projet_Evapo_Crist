# Projet Évaporation et Cristallisation

## Description du Projet

Conception et simulation d'une unité intégrée d'évaporation à multiples effets et de cristallisation pour la production de sucre cristallisé à partir de jus de canne à sucre.

**Université Hassan 1 - FST Settat**  
**Filière: Procédés et Ingénierie Chimique (PIC)**  
**Année Universitaire 2024-2025**

---

## Structure du Projet

```
projet_evaporation_cristallisation/
├── code/
│   ├── main.py                  # Script principal
│   ├── thermodynamique.py       # Module propriétés thermodynamiques
│   ├── evaporateurs.py          # Module évaporation multiples effets
│   ├── cristallisation.py       # Module cristallisation batch
│   ├── optimisation.py          # Module analyses et optimisation
│   └── requirements.txt         # Dépendances Python
├── resultats_calculs.xlsx       # Résultats numériques
└── *.png                        # Graphiques générés
```

---

## Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
cd code/
pip install -r requirements.txt
```

### 3. Vérification de l'installation

```bash
python -c "import CoolProp; print('CoolProp OK')"
```

---

## Utilisation

### Exécution complète du projet

```bash
python main.py
```

Cette commande exécute:
- Partie 1: Évaporation à multiples effets
- Partie 2: Cristallisation
- Partie 3: Intégration et optimisation globale

### Exécution des modules individuels

**Test du module thermodynamique:**
```bash
python thermodynamique.py
```

**Test du module évaporateurs:**
```bash
python evaporateurs.py
```

**Test du module cristallisation:**
```bash
python cristallisation.py
```

**Test du module optimisation:**
```bash
python optimisation.py
```

---

## Modules

### 1. thermodynamique.py

**Fonctionnalités:**
- Calcul des propriétés de l'eau et de la vapeur (CoolProp)
- Élévation du point d'ébullition (EPE) selon Dühring
- Propriétés des solutions de saccharose
- Solubilité et sursaturation

**Classe principale:** `ProprietesThermodynamiques`

**Exemple d'utilisation:**
```python
from thermodynamique import ProprietesThermodynamiques

thermo = ProprietesThermodynamiques()
T_sat = thermo.temperature_saturation(3.5)  # bar
EPE = thermo.EPE_saccharose(65)  # %
```

### 2. evaporateurs.py

**Fonctionnalités:**
- Simulation évaporateur à n effets (2-5)
- Bilans de matière et d'énergie
- Calcul des surfaces d'échange
- Économie de vapeur

**Classe principale:** `EvaporateurMultiplesEffets`

**Exemple d'utilisation:**
```python
from evaporateurs import EvaporateurMultiplesEffets

evap = EvaporateurMultiplesEffets(n_effets=3)
evap.resoudre_bilans()
evap.afficher_resultats()
evap.tracer_profils()
```

### 3. cristallisation.py

**Fonctionnalités:**
- Cinétique de nucléation et croissance
- Bilan de population (moments)
- Profils de refroidissement (linéaire, exponentiel, optimal)
- Dimensionnement du cristalliseur

**Classe principale:** `CristalliseurBatch`

**Exemple d'utilisation:**
```python
from cristallisation import CristalliseurBatch

crist = CristalliseurBatch()
crist.simuler(profil='lineaire')
crist.tracer_resultats()
dims = crist.dimensionnement()
```

### 4. optimisation.py

**Fonctionnalités:**
- Analyses de sensibilité paramétriques
- Analyse technico-économique
- Comparaison de configurations
- Calcul TCI, OPEX, VAN, ROI

**Classes principales:** `AnalyseSensibilite`, `AnalyseEconomique`

**Exemple d'utilisation:**
```python
from optimisation import AnalyseSensibilite, AnalyseEconomique

# Analyse de sensibilité
analyse = AnalyseSensibilite()
analyse.analyse_nombre_effets()

# Analyse économique
eco = AnalyseEconomique()
eco.comparer_configurations()
```

---

## Résultats

### Fichiers générés

1. **Graphiques (PNG):**
   - `profils_evaporateurs.png` - Profils T, x, P, A
   - `cristallisation_*.png` - Évolution cristallisation
   - `analyse_nombre_effets.png` - Impact nombre d'effets
   - `analyse_pression_vapeur.png` - Impact pression vapeur
   - `analyse_concentration.png` - Impact concentration
   - `analyse_debit.png` - Impact débit alimentation
   - `comparaison_economique.png` - Analyse économique

2. **Données (XLSX):**
   - `resultats_calculs.xlsx` - Résultats numériques détaillés

---

## Méthodologie

### Partie 1: Évaporation (40 points)

1. **Modélisation thermodynamique (15 points)**
   - Bilans de matière global et par composant
   - Bilans énergétiques avec pertes thermiques
   - Calcul des surfaces d'échange avec encrassement

2. **Optimisation énergétique (10 points)**
   - Économie de vapeur
   - Impact du nombre d'effets (2-5)
   - Configuration optimale

3. **Analyse de sensibilité (15 points)**
   - Pression de vapeur (2.5-4.5 bar)
   - Concentration finale (60-70%)
   - Débit d'alimentation (±20%)
   - Température d'alimentation

### Partie 2: Cristallisation (40 points)

1. **Modélisation cinétique (20 points)**
   - Solubilité du saccharose
   - Cinétique de nucléation (loi de puissance)
   - Cinétique de croissance (loi d'Arrhenius)
   - Bilan de population (méthode des moments)

2. **Stratégie de refroidissement (10 points)**
   - Profil linéaire
   - Profil exponentiel
   - Profil optimal (sursaturation constante)
   - Comparaison DTG, L50, CV

3. **Dimensionnement (10 points)**
   - Volume cristalliseur
   - Puissance agitation
   - Surface serpentin refroidissement
   - Temps de résidence

### Partie 3: Intégration (20 points)

1. **Intégration énergétique (10 points)**
   - Récupération chaleur condensats
   - Utilisation vapeurs dernier effet
   - Calcul économie énergétique

2. **Analyse technico-économique (10 points)**
   - TCI (Total Capital Investment)
   - OPEX (Operating Expenses)
   - Coût de production unitaire
   - VAN, ROI

---

## Hypothèses et Simplifications

### Évaporateurs

- Régime stationnaire
- Pas d'accumulation
- Pertes thermiques: 3%
- Résistance d'encrassement: 0.0002 m²·K/W
- Configuration co-courant

### Cristalliseur

- Batch idéal (parfaitement agité)
- Cristaux sphériques (k_v = π/6)
- Pas de brisure ni agglomération
- Densité cristaux: 1500 kg/m³
- Nucléation secondaire uniquement

### Économique

- Durée de vie: 15 ans
- Taux d'actualisation: 8%
- Fonctionnement: 8000 h/an
- Prix vapeur: 25 €/tonne
- Prix électricité: 0.12 €/kWh

---

## Validation des Résultats

### Vérifications automatiques

Le code inclut des vérifications de:
- Conservation de la matière (< 1% erreur)
- Conservation du saccharose (< 1% erreur)
- Cohérence des températures (décroissantes)
- Ordres de grandeur physiques

### Ordres de grandeur attendus

**Évaporateurs:**
- Économie de vapeur (3 effets): 2.5-2.8
- Surfaces: 50-200 m² par effet
- Températures: décroissantes de ~140°C à ~50°C

**Cristallisation:**
- Taille moyenne: 100-1000 µm
- CV: 20-50%
- Sursaturation: 0.02-0.10

---

## Références

### Ouvrages

1. Perry's Chemical Engineers' Handbook (8th ed.)
2. Mullin, J.W. - Crystallization (4th ed.)
3. Geankoplis, C.J. - Transport Processes

### Logiciels

- CoolProp: http://www.coolprop.org
- NumPy: https://numpy.org
- SciPy: https://scipy.org
- Matplotlib: https://matplotlib.org

---

## Auteurs

**Projet PIC 2024-2025**  
Université Hassan 1 - FST Settat

---

## License

Ce projet est réalisé dans un cadre pédagogique.

---

## Support

Pour toute question:
- Consulter la documentation dans les docstrings
- Lire le guide d'équations fourni
- Contacter le responsable de module

---

## Notes Importantes

⚠️ **Avant de lancer le code:**
1. Vérifier que CoolProp est bien installé
2. Vérifier que tous les modules sont dans le même répertoire
3. Les calculs peuvent prendre quelques minutes

✅ **Critères de qualité:**
- Code documenté (docstrings)
- Gestion des erreurs
- Tests unitaires inclus
- Résultats vérifiés

📊 **Livrables attendus:**
- Code Python fonctionnel
- Rapport LaTeX
- Présentation PowerPoint
- Fichiers de résultats
