# 🚀 Guide de Lancement - Application Streamlit

## 📱 Application Web Évaporation & Cristallisation

Application web interactive optimisée pour **Desktop** et **Mobile** !

---

## 🎯 Installation Rapide

### 1. Installer les dépendances

```bash
pip install streamlit numpy scipy matplotlib pandas CoolProp openpyxl
```

Ou avec le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer l'Application

### Méthode 1 : Commande Simple

```bash
streamlit run app.py
```

### Méthode 2 : Avec Options

```bash
# Ouvrir automatiquement dans le navigateur
streamlit run app.py --server.headless=false

# Spécifier un port
streamlit run app.py --server.port=8502

# Mode développement (rechargement auto)
streamlit run app.py --server.runOnSave=true
```

---

## 📱 Accéder depuis Mobile

### Sur le même réseau WiFi :

1. **Trouver l'adresse IP de votre PC :**

   **Windows:**
   ```bash
   ipconfig
   ```
   Cherchez "Adresse IPv4" (ex: 192.168.1.100)

   **Mac/Linux:**
   ```bash
   ifconfig | grep inet
   ```

2. **Lancer l'application :**
   ```bash
   streamlit run app.py
   ```

3. **Sur votre smartphone :**
   - Ouvrez le navigateur
   - Tapez : `http://192.168.1.100:8501`
   - (Remplacez par votre IP)

### Via Tunnel Internet (accès partout) :

```bash
# Installer ngrok
# https://ngrok.com/download

# Lancer l'app
streamlit run app.py

# Dans un autre terminal
ngrok http 8501
```

L'URL ngrok peut être utilisée depuis n'importe où !

---

## 🎨 Fonctionnalités de l'Application

### 🏠 **Onglet Accueil**
- Présentation du projet
- Spécifications techniques
- Navigation intuitive

### 💧 **Onglet Évaporation**
- Simulation interactive à 2-5 effets
- Paramètres ajustables :
  - Nombre d'effets
  - Pression vapeur
  - Concentration finale
  - Débit alimentation
- Résultats en temps réel
- Graphiques interactifs
- Tableau détaillé par effet

### 💎 **Onglet Cristallisation**
- Simulation batch
- 3 profils de refroidissement :
  - Linéaire
  - Exponentiel
  - Optimal (sursaturation constante)
- Paramètres ajustables :
  - Températures initiale/finale
  - Durée du batch
- Dimensionnement automatique
- Visualisation de l'évolution

### 📊 **Onglet Optimisation**
- Impact du nombre d'effets
- Analyse économique comparative
- Analyses de sensibilité
- Recommandations automatiques

### 🧮 **Onglet Calculateur**
- Propriétés thermodynamiques
- Solubilité du saccharose
- EPE (Élévation Point Ébullition)
- Économie de vapeur
- Courbes interactives

---

## 💡 Astuces d'Utilisation

### Sur Mobile 📱

1. **Navigation :** Utilisez les onglets en haut
2. **Paramètres :** Cliquez sur "⚙️ Paramètres" pour les options
3. **Zoom :** Pincez pour zoomer sur les graphiques
4. **Orientation :** Le mode paysage offre plus d'espace

### Sur Desktop 💻

1. **Plein écran :** F11 pour mode immersif
2. **Sidebar :** Cliquez sur ">" pour ouvrir/fermer
3. **Zoom :** Ctrl + molette pour ajuster la taille
4. **Raccourcis :**
   - R : Relancer l'app
   - C : Effacer le cache

---

## 🎨 Personnalisation

### Modifier le Thème

Créez un fichier `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Changer le Port

```bash
streamlit run app.py --server.port=8080
```

### Désactiver les Notifications

```bash
streamlit run app.py --global.developmentMode=false
```

---

## 🔧 Résolution de Problèmes

### Erreur : "streamlit not found"
```bash
pip install streamlit
# ou
pip3 install streamlit
```

### Erreur : "Port already in use"
```bash
# Utiliser un autre port
streamlit run app.py --server.port=8502
```

### Erreur : "No module named 'CoolProp'"
```bash
pip install CoolProp
```

### L'application ne se charge pas
1. Vérifiez que tous les fichiers .py sont dans le même dossier
2. Relancez avec : `streamlit run app.py --server.runOnSave=false`
3. Videz le cache : supprimez le dossier `.streamlit/`

### Graphiques ne s'affichent pas
```bash
# Réinstaller matplotlib
pip uninstall matplotlib
pip install matplotlib
```

---

## 📊 Captures d'Écran

L'application inclut :
- ✅ Interface responsive (s'adapte à l'écran)
- ✅ Graphiques haute résolution
- ✅ Tableaux interactifs
- ✅ Export des résultats
- ✅ Calculs en temps réel

---

## 🌐 Déploiement en Ligne (Optionnel)

### Streamlit Cloud (Gratuit)

1. Créez un compte sur [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connectez votre dépôt GitHub
3. Sélectionnez `app.py`
4. Déployez !

Votre app sera accessible 24/7 depuis n'importe où !

---

## 📝 Structure des Fichiers

```
votre_dossier/
├── app.py                    ← Application Streamlit
├── main.py                   ← Script ligne de commande
├── thermodynamique.py        ← Module propriétés
├── evaporateurs.py           ← Module évaporation
├── cristallisation.py        ← Module cristallisation
├── optimisation.py           ← Module optimisation
├── requirements.txt          ← Dépendances
└── README.md                 ← Documentation
```

---

## 🎓 Utilisation Académique

### Pour une Présentation

1. **Lancez l'app avant la présentation**
2. **Mode présentation :**
   ```bash
   streamlit run app.py --server.headless=false --browser.gatherUsageStats=false
   ```
3. **Préparez les paramètres à l'avance**
4. **Utilisez F11 pour le plein écran**

### Pour un Rapport

1. **Capturez les graphiques** (clic droit > Enregistrer)
2. **Exportez les tableaux** (copier-coller dans Excel)
3. **Documentez les paramètres** utilisés

---

## ⚡ Performances

### Optimisation

- **Cache activé** : Les calculs sont mis en cache
- **Calculs parallèles** : Utilisation optimale du CPU
- **Graphiques légers** : PNG optimisés

### Temps de Calcul Moyens

- Évaporation (3 effets) : ~2 secondes
- Cristallisation : ~5 secondes
- Optimisation (4 configs) : ~10 secondes

---

## 💬 Support

En cas de problème :
1. Vérifiez que Python 3.8+ est installé
2. Réinstallez les dépendances
3. Consultez la documentation Streamlit : [docs.streamlit.io](https://docs.streamlit.io)

---

## 🎉 Félicitations !

Vous êtes prêt à utiliser l'application !

```bash
streamlit run app.py
```

**Bon travail ! 🚀**

---

*Application créée pour le Projet PIC 2024-2025*  
*Université Hassan 1 - FST Settat*
