#!/bin/bash

# --- KONFIGURASI ---
TOOL_NAME="pentest"
REPO_NAME="El-Cyber-Pentest"
GITHUB_REPO="https://github.com/Proot9/$REPO_NAME.git"
INSTALL_DIR="/opt/$REPO_NAME"

# Warna
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# --- DETEKSI LINGKUNGAN OTOMATIS ---
if [ -d "/data/data/com.termux" ]; then
    # Lingkungan Termux
    echo -e "${GREEN}[INFO] Lingkungan terdeteksi: Termux${NC}"
    # Path untuk executable Termux
    BIN_DIR="/data/data/com.termux/files/usr/bin"
    # Shebang untuk script wrapper Termux
    SHEBANG_PATH="#!/data/data/com.termux/files/usr/bin/bash"
    # Perintah Python di Termux
    PYTHON_CMD="python"
    # Memastikan tool Python terinstal di Termux
    pkg install -y python git
else
    # Lingkungan Linux Standar (Kali, Ubuntu, Debian, dll.)
    echo -e "${GREEN}[INFO] Lingkungan terdeteksi: Standard Linux${NC}"
    # Path untuk executable global (memerlukan hak akses root)
    BIN_DIR="/usr/local/bin"
    # Shebang standar Linux
    SHEBANG_PATH="#!/bin/bash"
    # Menggunakan python3 untuk kompatibilitas yang lebih baik
    PYTHON_CMD="python3"
    # Memastikan paket yang diperlukan terinstal
    sudo apt update && sudo apt install -y python3 python3-pip git
fi

# -----------------------------------------------------------------------------

echo -e "${GREEN}### Memulai Instalasi ${REPO_NAME} ###${NC}"

# 1. Cek Python dan Git (Diperlukan di semua lingkungan)
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git tidak ditemukan. Instal Git terlebih dahulu.${NC}"
    exit 1
fi
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo -e "${RED}Error: Python tidak ditemukan. Pastikan $PYTHON_CMD terinstal.${NC}"
    exit 1
fi

# 2. Persiapan Direktori Instalasi
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${RED}[!] Menghapus instalasi lama di $INSTALL_DIR...${NC}"
    rm -rf "$INSTALL_DIR"
fi

echo -e "${GREEN}[+] Membuat direktori instalasi di $INSTALL_DIR${NC}"
# Membuat direktori instalasi (memerlukan sudo di Linux standar)
if [ "$SHEBANG_PATH" = "#!/bin/bash" ]; then
    sudo mkdir -p "$INSTALL_DIR"
    # Menginstalasi dari GitHub (Menggunakan sudo untuk akses write ke /opt)
    sudo git clone "$GITHUB_REPO" "$INSTALL_DIR"
else
    mkdir -p "$INSTALL_DIR"
    git clone "$GITHUB_REPO" "$INSTALL_DIR"
fi


if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Gagal mengkloning repository. Cek URL GitHub.${NC}"
    rm -rf "$INSTALL_DIR"
    exit 1
fi

# 3. Instal Dependensi Python
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    echo -e "${GREEN}[+] Menginstal dependensi Python...${NC}"

    # Menggunakan sudo jika ini adalah instalasi global di Linux
    if [ "$SHEBANG_PATH" = "#!/bin/bash" ]; then
        sudo "$PYTHON_CMD" -m pip install -r "$INSTALL_DIR/requirements.txt"
    else
        "$PYTHON_CMD" -m pip install -r "$INSTALL_DIR/requirements.txt"
    fi

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Gagal menginstal dependensi Python.${NC}"
        exit 1
    fi
fi

# 4. Membuat Script Wrapper Dinamis
WRAPPER_SRC="$INSTALL_DIR/$TOOL_NAME"
WRAPPER_DST="$BIN_DIR/$TOOL_NAME"

echo -e "${GREEN}[+] Membuat script wrapper ${TOOL_NAME} (${SHEBANG_PATH})...${NC}"

# Membuat script wrapper menggunakan SHEBANG_PATH dan PYTHON_CMD yang dinamis
cat << EOF > "$WRAPPER_SRC"
$SHEBANG_PATH

PROJECT_DIR="$INSTALL_DIR"
cd "\$PROJECT_DIR" || { echo "Error: Gagal mengakses source code tools."; exit 1; }
$PYTHON_CMD main.py "\$@"
EOF

# 5. Memasang Wrapper ke $PATH (Menggunakan sudo jika perlu)
chmod +x "$WRAPPER_SRC"

if [ -f "$WRAPPER_DST" ]; then
    echo -e "[!] Wrapper lama ditemukan, mengganti..."
    if [ "$SHEBANG_PATH" = "#!/bin/bash" ]; then sudo rm "$WRAPPER_DST"; else rm "$WRAPPER_DST"; fi
fi

echo -e "${GREEN}[+] Memasang wrapper ke ${BIN_DIR} (Akses Global)...${NC}"
if [ "$SHEBANG_PATH" = "#!/bin/bash" ]; then
    sudo cp "$WRAPPER_SRC" "$WRAPPER_DST"
    sudo chmod +x "$WRAPPER_DST"
else
    cp "$WRAPPER_SRC" "$WRAPPER_DST"
    chmod +x "$WRAPPER_DST"
fi

echo -e "${GREEN}####################################################${NC}"
echo -e "${GREEN}INSTALASI SELESAI!${NC}"
echo -e "${GREEN}Jalankan tools dengan mengetik:${NC}"
echo -e "${GREEN}>> ${TOOL_NAME}${NC}"
echo -e "${GREEN}####################################################${NC}"
