#!/bin/bash
# --- KONFIGURASI ---
TOOL_NAME="pentest"
REPO_NAME="El-Cyber_Pentest"
GITHUB_REPO="https://github.com/Proot9/$REPO_NAME.git"
VERSION=$(< version.txt)

# Warna
GREEN='\033[92m'
RED='\033[91m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# --- DETEKSI LINGKUNGAN OTOMATIS & KONFIGURASI PATH ---
# -----------------------------------------------------------------------------
if [ -d "/data/data/com.termux" ]; then
    # Lingkungan Termux
    echo -e "${GREEN}[INFO] Lingkungan terdeteksi: Termux${NC}"

    BIN_DIR="$PREFIX/bin"
    SHEBANG_PATH="#!$PREFIX/bin/bash"
    PYTHON_CMD="python"
    INSTALL_DIR="$PREFIX/share/$REPO_NAME"

    NEEDS_SUDO=false
    pkg install -y python git
else
    # Lingkungan Linux Standar
    echo -e "${GREEN}[INFO] Lingkungan terdeteksi: Standard Linux${NC}"

    BIN_DIR="/usr/local/bin"
    SHEBANG_PATH="#!/bin/bash"
    PYTHON_CMD="python3"
    INSTALL_DIR="/opt/$REPO_NAME"

    NEEDS_SUDO=true
    sudo apt update && sudo apt install -y python3 python3-pip git
fi

# -----------------------------------------------------------------------------

echo -e "${GREEN}[!] Mulai Instalasi ${REPO_NAME} [!] ${NC}"

# 1. Cek Python dan Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}[x] Error: Git tidak ditemukan. Instal Git terlebih dahulu.${NC}"
    exit 1
fi
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo -e "${RED}[x] Error: Python tidak ditemukan. Pastikan $PYTHON_CMD terinstal.${NC}"
    exit 1
fi

# 2. Persiapan Direktori Instalasi
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${GREEN}[-] Menghapus instalasi lama...${NC}"
    cd ~
    if $NEEDS_SUDO; then sudo rm -rf "$INSTALL_DIR"; else rm -rf "$INSTALL_DIR"; fi
fi

echo -e "${GREEN}[+] Membuat direktori instalasi{NC}"

# Membuat direktori dan kloning repositori (menggunakan sudo jika perlu)
if $NEEDS_SUDO; then
    sudo mkdir -p "$INSTALL_DIR"
    sudo git clone "$GITHUB_REPO" "$INSTALL_DIR"
else
    mkdir -p "$INSTALL_DIR"
    git clone "$GITHUB_REPO" "$INSTALL_DIR"
fi


if [ $? -ne 0 ]; then
    echo -e "${RED}[x] Error: Gagal mengkloning repository. Cek URL GitHub.${NC}"
    if $NEEDS_SUDO; then sudo rm -rf "$INSTALL_DIR"; else rm -rf "$INSTALL_DIR"; fi
    exit 1
fi

# 3. Instal Dependensi Python
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    echo -e "${GREEN}[+] Menginstal dependensi Python...${NC}"

    if $NEEDS_SUDO; then
        # Di Ubuntu/Kali, kita tambahkan flag --break-system-packages
        sudo "$PYTHON_CMD" -m pip install -r "$INSTALL_DIR/requirements.txt" --break-system-packages
    else
        # Di Termux, pip biasanya tidak butuh flag tambahan
        "$PYTHON_CMD" -m pip install -r "$INSTALL_DIR/requirements.txt"
    fi

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Gagal menginstal dependensi Python.${NC}"
        # Opsional: Jangan langsung exit jika gagal, beri peringatan saja
        # exit 1 
    fi
fi

# 4. Membuat Script Wrapper Dinamis
WRAPPER_SRC="$INSTALL_DIR/$TOOL_NAME"
WRAPPER_DST="$BIN_DIR/$TOOL_NAME"

echo -e "${GREEN}[+] Membuat script wrapper ${TOOL_NAME}...${NC}"

# Membuat konten wrapper dalam variabel agar mudah dikelola
CREATE_WRAPPER="cat << 'EOF' > $WRAPPER_SRC
$SHEBANG_PATH
PROJECT_DIR=\"$INSTALL_DIR\"
cd \"\$PROJECT_DIR\" || { echo \"Error: Gagal mengakses direktori proyek.\"; exit 1; }
$PYTHON_CMD main.py \"\$@\"
EOF"

# Eksekusi pembuatan file berdasarkan hak akses (Sudo vs User)
if $NEEDS_SUDO; then
    sudo bash -c "$CREATE_WRAPPER"
    sudo chmod +x "$WRAPPER_SRC"
    sudo cp "$WRAPPER_SRC" "$WRAPPER_DST"
    sudo chmod +x "$WRAPPER_DST"
else
    # Untuk Termux (Tanpa Sudo)
    bash -c "$CREATE_WRAPPER"
    chmod +x "$WRAPPER_SRC"
    cp "$WRAPPER_SRC" "$WRAPPER_DST"
    chmod +x "$WRAPPER_DST"
fi

echo -e "${GREEN}####################################################${NC}"
echo -e "${GREEN}[✓] Tools terinstal di: $INSTALL_DIR${NC}"
echo -e "${GREEN}[✓] Memasang wrapper ke: ${BIN_DIR}${NC}"
echo -e "${GREEN}[✓] INSTALASI SELESAI VERSION: ${VERSION}${NC}"
echo -e "${GREEN}####################################################${NC}"
