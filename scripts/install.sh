#!/usr/bin/env bash
# ==============================================================================
# AbyssalSkillsD — Universal macOS & Linux Quick Installer
# Standard: POSIX compliant, Zero-Dependency bootstrap
# Usage: curl -fsSL https://raw.githubusercontent.com/Play-with-me/AbyssalSkills-AI/main/scripts/install.sh | bash
# ==============================================================================

set -e

CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================${NC}"
echo -e "${MAGENTA}   🌌 AbyssalSkillsD — Enterprise AI Skill Studio Installer     ${NC}"
echo -e "${CYAN}================================================================${NC}"

OS="$(uname -s)"
ARCH="$(uname -m)"

echo -e "${YELLOW}[*] Detected Environment: ${OS} (${ARCH})${NC}"

# Check for git
if ! command -v git &> /dev/null; then
    echo -e "${RED}[X] Error: git is required. Please install git and re-run this script.${NC}"
    exit 1
fi

INSTALL_DIR="${HOME}/.abyssalskillsd"
REPO_URL="https://github.com/Play-with-me/AbyssalSkills-AI.git"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}[*] Existing installation found at ${INSTALL_DIR}. Updating to latest...${NC}"
    cd "$INSTALL_DIR"
    git pull --ff-only
else
    echo -e "${YELLOW}[*] Cloning AbyssalSkillsD into ${INSTALL_DIR}...${NC}"
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Ensure uv or python3 is available
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}[*] uv not found. Installing Astral uv (ultra-fast Python package manager)...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"
fi

if command -v uv &> /dev/null; then
    echo -e "${GREEN}[+] Syncing virtual environment via uv...${NC}"
    uv sync
else
    echo -e "${YELLOW}[*] Setting up via system python3 venv...${NC}"
    python3 -m venv .venv
    .venv/bin/pip install "pywebview>=5.0" "pydantic>=2.0" "requests>=2.30" "watchdog>=4.0"
fi

# Create desktop launcher / shell shortcut
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/abyssalskillsd"

cat << 'EOF' > "$LAUNCHER"
#!/usr/bin/env bash
DIR="${HOME}/.abyssalskillsd"
cd "$DIR"
if command -v uv &> /dev/null; then
    exec uv run main.py "$@"
else
    exec "$DIR/.venv/bin/python" main.py "$@"
fi
EOF

chmod +x "$LAUNCHER"

# macOS .app or Linux .desktop integration
if [ "$OS" = "Darwin" ]; then
    echo -e "${GREEN}[✓] macOS Launcher ready: ${LAUNCHER}${NC}"
    echo -e "${YELLOW}[*] To launch from anywhere, ensure ~/.local/bin is in your PATH:${NC}"
    echo -e "    export PATH=\"\$HOME/.local/bin:\$PATH\""
elif [ "$OS" = "Linux" ]; then
    DESKTOP_DIR="${HOME}/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    cat << EOF > "$DESKTOP_DIR/abyssalskillsd.desktop"
[Desktop Entry]
Name=AbyssalSkillsD
Comment=Enterprise AI Skill Manager and Local-to-Cloud Marketplace
Exec=$LAUNCHER
Icon=$INSTALL_DIR/app/frontend/assets/logo/icon-dark.svg
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
    echo -e "${GREEN}[✓] Linux Desktop Entry created: ${DESKTOP_DIR}/abyssalskillsd.desktop${NC}"
fi

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}   ✓ AbyssalSkillsD Installation Complete!                      ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "${CYAN}To launch AbyssalSkillsD now, run:${NC}"
echo -e "   ${MAGENTA}abyssalskillsd${NC} (or: cd ~/.abyssalskillsd && uv run main.py)"
echo ""
