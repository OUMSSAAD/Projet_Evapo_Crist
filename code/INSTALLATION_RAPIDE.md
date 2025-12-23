# 🚀 INSTALLATION RAPIDE - Projet Évaporation & Cristallisation

## ✅ Ce qui a été corrigé

Tous les chemins de fichiers ont été corrigés pour fonctionner sur **Windows, Mac et Linux** !

---

## 📦 Contenu du Package

```
code/
├── app.py                    ⭐ NOUVELLE APPLICATION WEB
├── main.py                   ✅ Script principal (corrigé)
├── thermodynamique.py        ✅ Propriétés physiques
├── evaporateurs.py           ✅ Simulation évaporation (corrigé)
├── cristallisation.py        ✅ Simulation cristallisation (corrigé)
├── optimisation.py           ✅ Analyses (corrigé)
├── requirements.txt          ✅ Dépendances (+ Streamlit)
├── README.md                 📖 Documentation complète
└── GUIDE_STREAMLIT.md        📱 Guide application web
```

---

## ⚡ Installation Ultra-Rapide

### 1️⃣ Installer Python (si nécessaire)

Téléchargez Python 3.8+ sur [python.org](https://www.python.org/downloads/)

**⚠️ Important:** Cochez "Add Python to PATH" lors de l'installation !

### 2️⃣ Installer les dépendances

Ouvrez le terminal dans le dossier `code/` et exécutez :

```bash
pip install -r requirements.txt
```

**Problème ?** Essayez :
```bash
python -m pip install -r requirements.txt
```

### 3️⃣ Lancer l'Application Web 🌐

```bash
streamlit run app.py
```

**🎉 C'est tout !** L'application s'ouvre dans votre navigateur.

---

## 📱 Utiliser sur Smartphone

### Option 1 : Même réseau WiFi

1. **Sur votre PC**, trouvez votre adresse IP :
   
   **Windows (PowerShell):**
   ```powershell
   ipconfig
   ```
   Cherchez "Adresse IPv4" (ex: `192.168.1.50`)
   
   **Mac/Linux:**
   ```bash
   ifconfig | grep inet
   ```

2. **Lancez l'app :**
   ```bash
   streamlit run app.py
   ```

3. **Sur votre smartphone :**
   - Ouvrez le navigateur (Chrome, Safari, etc.)
   - Tapez : `http://192.168.1.50:8501`
   - (Remplacez par votre IP)

### Option 2 : Via Internet (ngrok)

```bash
# Téléchargez ngrok : https://ngrok.com/download

# Lancez l'app
streamlit run app.py

# Dans un AUTRE terminal
ngrok http 8501
```

Utilisez l'URL fournie par ngrok depuis n'importe où !

---

## 🖥️ Exécution Ligne de Commande (Alternative)

Si vous préférez le mode terminal :

```bash
python main.py
```

Cela génère :
- ✅ Tous les graphiques (PNG)
- ✅ Fichier Excel avec résultats
- ✅ Rapport complet dans le terminal

---

## 🎯 Démarrage Rapide - Windows

**Créez un fichier `LANCER_APP.bat` :**

```batch
@echo off
echo ========================================
echo   Application Evaporation-Cristallisation
echo ========================================
echo.
echo Installation des dependances...
pip install -r requirements.txt
echo.
echo Lancement de l'application...
streamlit run app.py
pause
```

**Double-cliquez dessus** pour tout lancer automatiquement !

---

## 🎯 Démarrage Rapide - Mac/Linux

**Créez un fichier `lancer_app.sh` :**

```bash
#!/bin/bash
echo "========================================"
echo "  Application Évaporation-Cristallisation"
echo "========================================"
echo ""
echo "Installation des dépendances..."
pip3 install -r requirements.txt
echo ""
echo "Lancement de l'application..."
streamlit run app.py
```

**Rendez-le exécutable :**
```bash
chmod +x lancer_app.sh
./lancer_app.sh
```

---

## 🔧 Résolution de Problèmes

### Erreur : "pip not found"

```bash
# Windows
python -m ensurepip --upgrade

# Mac
python3 -m ensurepip --upgrade
```

### Erreur : "streamlit not found"

```bash
pip install streamlit
# ou
python -m pip install streamlit
```

### Erreur : "No module named 'CoolProp'"

```bash
pip install CoolProp numpy scipy matplotlib pandas
```

### L'application ne démarre pas

1. **Vérifiez Python :**
   ```bash
   python --version
   ```
   Doit être ≥ 3.8

2. **Réinstallez tout :**
   ```bash
   pip uninstall -y streamlit numpy scipy matplotlib pandas CoolProp
   pip install -r requirements.txt
   ```

3. **Utilisez un autre port :**
   ```bash
   streamlit run app.py --server.port=8502
   ```

### Problème avec les chemins de fichiers

✅ **Déjà corrigé !** Tous les fichiers utilisent maintenant des chemins relatifs.

Si problème persiste, vérifiez que vous êtes bien dans le dossier `code/` :

```bash
cd chemin/vers/code/
streamlit run app.py
```

---

## 📊 Fonctionnalités de l'Application

### 🏠 Accueil
- Vue d'ensemble du projet
- Spécifications techniques

### 💧 Évaporation
- Simulation 2-5 effets
- Paramètres ajustables
- Graphiques temps réel
- Export résultats

### 💎 Cristallisation
- 3 profils de refroidissement
- Dimensionnement auto
- Visualisation évolution

### 📊 Optimisation
- Analyses économiques
- Comparaisons configs
- Recommandations

### 🧮 Calculateur
- Propriétés thermo
- Solubilité
- EPE
- Courbes interactives

---

## 💡 Conseils d'Utilisation

### Pour Mobile 📱
- Interface **responsive** (s'adapte automatiquement)
- Utilisez les **onglets** pour naviguer
- **Pincez** pour zoomer sur les graphiques
- Mode **paysage** recommandé pour les graphiques

### Pour Desktop 💻
- **F11** pour plein écran
- **Ctrl + molette** pour zoom
- **R** pour recharger
- **C** pour effacer le cache

---

## 🎓 Utilisation Académique

### Pour Présentation
1. Lancez l'app **avant** la présentation
2. Préparez les paramètres à l'avance
3. Mode plein écran (F11)
4. Naviguez avec les onglets

### Pour Rapport
1. Capturez les graphiques (clic droit)
2. Exportez les données (copier tableaux)
3. Documentez les paramètres

---

## 📈 Performances

**Temps de calcul moyens :**
- Évaporation : ~2 secondes
- Cristallisation : ~5 secondes  
- Optimisation : ~10 secondes

**Optimisations :**
- ✅ Cache activé
- ✅ Calculs optimisés
- ✅ Graphiques légers

---

## 🎉 C'est Parti !

**Méthode 1 - Application Web (Recommandé) :**
```bash
streamlit run app.py
```

**Méthode 2 - Ligne de commande :**
```bash
python main.py
```

---

## 📞 Support

**En cas de problème :**
1. Lisez `GUIDE_STREAMLIT.md` pour plus de détails
2. Consultez `README.md` pour la documentation
3. Vérifiez que Python 3.8+ est installé
4. Réinstallez les dépendances

---

## 📝 Versions

**v2.0 - Avec Application Web**
- ✅ Tous les chemins corrigés (Windows/Mac/Linux)
- ✅ Application Streamlit ajoutée
- ✅ Interface mobile-friendly
- ✅ Documentation complète

**v1.0 - Version Originale**
- Modules Python de base
- Script main.py

---

*Projet PIC 2024-2025*  
*Université Hassan 1 - FST Settat*

**🚀 Bon travail !**
