#!/bin/bash
# ========================================
# SETUP Thouv'Run - Installation automatique
# Linux / macOS
# ========================================

set -e

echo ""
echo "========================================"
echo "  SETUP - Thouv'Run Multi-Joueur"
echo "========================================"
echo ""

# Detecter l'OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    *)          PLATFORM="UNKNOWN";;
esac

echo "[*] Systeme detecte: $PLATFORM"
echo ""

# ========================================
# INSTALLATION DE PYTHON
# ========================================
install_python() {
    echo "[*] Installation de Python..."
    
    if [ "$PLATFORM" = "Linux" ]; then
        # Detecter le gestionnaire de paquets
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python python-pip
        else
            echo "[ERREUR] Gestionnaire de paquets non supporte"
            echo "Installez Python 3.12+ manuellement: https://www.python.org/downloads/"
            exit 1
        fi
    elif [ "$PLATFORM" = "Mac" ]; then
        # Utiliser Homebrew
        if command -v brew &> /dev/null; then
            brew install python3
        else
            echo "[!] Homebrew non installe. Installation..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install python3
        fi
    fi
}

# ========================================
# VERIFICATION DE PYTHON
# ========================================
echo "[*] Verification de Python..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[!] Python non installe, installation automatique..."
    install_python
    PYTHON_CMD="python3"
fi

# Verifier la version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "[OK] Python trouve: $($PYTHON_CMD --version)"
echo ""

# ========================================
# VERIFICATION DE PIP
# ========================================
echo "[*] Verification de pip..."

if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "[!] pip non detecte, installation..."
    
    if [ "$PLATFORM" = "Linux" ]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-pip
        else
            $PYTHON_CMD -m ensurepip --upgrade
        fi
    else
        $PYTHON_CMD -m ensurepip --upgrade
    fi
fi

echo "[OK] pip disponible"
echo ""

# ========================================
# INSTALLATION DES DEPENDANCES
# ========================================
echo "[*] Installation des dependances..."
echo "    - pygame (graphique)"
echo "    - flask (API serveur)"
echo "    - flask-cors (API)"
echo "    - requests (sync scores)"
echo ""

# Creer requirements pour Linux/Mac (sans windows-curses)
cat > /tmp/requirements-unix.txt << EOF
pygame>=2.5.0
flask>=3.0.0
flask-cors>=4.0.0
requests>=2.31.0
EOF

$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r /tmp/requirements-unix.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] Impossible d'installer les dependances"
    echo ""
    echo "Solutions:"
    echo "1. Verifiez votre connexion internet"
    echo "2. Essayez: $PYTHON_CMD -m pip install pygame flask flask-cors requests"
    exit 1
fi

echo "[OK] Dependances installees!"
echo ""

# ========================================
# RENDRE LES SCRIPTS EXECUTABLES
# ========================================
chmod +x src/*.py 2>/dev/null || true
chmod +x server/*.py 2>/dev/null || true

echo ""
echo "========================================"
echo "[OK] INSTALLATION REUSSIE!"
echo "========================================"
echo ""
echo "Tu peux maintenant lancer:"
echo "  $PYTHON_CMD src/main_graphique.py  (jeu pygame)"
echo "  $PYTHON_CMD src/main_terminal.py   (jeu terminal)"
echo "  $PYTHON_CMD server/api_server.py   (serveur API)"
echo ""
