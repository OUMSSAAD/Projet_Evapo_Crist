#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║     APPLICATION ÉVAPORATION & CRISTALLISATION                  ║${NC}"
echo -e "${BLUE}║     Université Hassan 1 - FST Settat                           ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1/3] Vérification de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé !${NC}"
    echo ""
    echo "Installation sur Mac : brew install python3"
    echo "Installation sur Ubuntu/Debian : sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Python3 détecté${NC}"
python3 --version

echo ""
echo -e "${YELLOW}[2/3] Installation des dépendances...${NC}"
python3 -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>&1 | grep -v "Requirement already satisfied"
echo -e "${GREEN}✅ Dépendances installées${NC}"

echo ""
echo -e "${YELLOW}[3/3] Lancement de l'application...${NC}"
echo ""
echo -e "${BLUE}┌────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  L'application va s'ouvrir dans votre navigateur          │${NC}"
echo -e "${BLUE}│                                                            │${NC}"
echo -e "${BLUE}│  📱 Pour accéder depuis mobile :                          │${NC}"
echo -e "${BLUE}│     1. Notez l'adresse IP affichée ci-dessous             │${NC}"
echo -e "${BLUE}│     2. Ouvrez http://VOTRE_IP:8501 sur votre mobile       │${NC}"
echo -e "${BLUE}│                                                            │${NC}"
echo -e "${BLUE}│  🛑 Pour arrêter : Appuy
ez sur Ctrl+C                     │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────────────────────┘${NC}"
echo ""

echo -e "${YELLOW}Votre adresse IP locale :${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac
    ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "Non détectée"
else
    # Linux
    hostname -I | awk '{print $1}'
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

streamlit run app.py

read -p "Appuyez sur Entrée pour fermer..."
