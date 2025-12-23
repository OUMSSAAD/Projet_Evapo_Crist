@echo off
chcp 65001 >nul
color 0A
cls

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     APPLICATION ÉVAPORATION ^& CRISTALLISATION                 ║
echo ║     Université Hassan 1 - FST Settat                          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.

echo [1/3] Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ Python n'est pas installé !
    echo.
    echo Téléchargez Python sur : https://www.python.org/downloads/
    echo ⚠️  N'oubliez pas de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit
)
echo ✅ Python détecté

echo.
echo [2/3] Installation des dépendances...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ⚠️  Certaines dépendances ont échoué, tentative avec pip3...
    pip3 install -r requirements.txt --quiet
)
echo ✅ Dépendances installées

echo.
echo [3/3] Lancement de l'application...
echo.
echo ┌────────────────────────────────────────────────────────────┐
echo │  L'application va s'ouvrir dans votre navigateur          │
echo │                                                            │
echo │  📱 Pour accéder depuis mobile :                          │
echo │     1. Notez l'adresse IP affichée ci-dessous            │
echo │     2. Ouvrez http://VOTRE_IP:8501 sur votre mobile      │
echo │                                                            │
echo │  🛑 Pour arrêter : Appuyez sur Ctrl+C                     │
echo └────────────────────────────────────────────────────────────┘
echo.

ipconfig | findstr /i "IPv4"
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

streamlit run app.py

pause
