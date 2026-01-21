import os
import subprocess
import shutil

REQUIRED_OPTIONS = {
    "INTERFACE": "eth0"
}

def execute(options):
    interface = options.get("INTERFACE")

    # --- LOGIKA PATH DINAMIS ---
    # Mendapatkan path absolut ke folder tempat modul ini berada
    module_dir = os.path.dirname(os.path.realpath(__file__))

    # Path internal untuk jeroan Storm-OS
    src_dir = os.path.join(module_dir, "src")
    bin_dir = os.path.join(module_dir, "bin")
    source_c = os.path.join(src_dir, "rtp_sniff.c")
    binary_out = os.path.join(bin_dir, "rtp_sniff")

    # Path output untuk User (Current Working Directory)
    output_pcm = os.path.join(os.getcwd(), "storm_capture.pcm")
    output_wav = os.path.join(os.getcwd(), "storm_capture.wav")

    # 1. Pastikan folder bin ada
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)

    # 2. Cek dependencies
    if not shutil.which("gcc"):
        print("[!] Error: GCC not found. Install it with 'pkg install clang' or 'apt install gcc'")
        return

    # 3. Compile otomatis jika binary belum ada
    if not os.path.exists(binary_out):
        print(f"[*] Compiling C Sniffer engine...")
        compile_cmd = ["gcc", source_c, "-lpcap", "-o", binary_out]
        result = subprocess.run(compile_cmd, capture_output=True)
        if result.returncode != 0:
            print(f"[!] Compilation failed:\n{result.stderr.decode()}")
            return

    # 4. Jalankan Sniffer
    print(f"[*] Sniffing on {interface}...")
    print(f"[*] Output will be saved at: {os.getcwd()}")
    print("[*] Press Ctrl+C to stop.")

    try:
        # Menjalankan binary dengan argumen: interface dan output_path
        subprocess.run(["sudo", binary_out, interface, output_pcm])
    except KeyboardInterrupt:
        print("\n[*] Sniffing stopped by user.")

    # 5. Konversi Otomatis ke WAV
    if os.path.exists(output_pcm):
        if shutil.which("ffmpeg"):
            print("[*] Converting raw PCM to WAV...")
            # G.711 mu-law (standar VoIP)
            conv_cmd = f"ffmpeg -y -f u8 -ar 8000 -ac 1 -i {output_pcm} {output_wav} > /dev/null 2>&1"
            os.system(conv_cmd)

            if os.path.exists(output_wav):
                os.remove(output_pcm) # Hapus file mentah agar bersih
                print(f"[+] Success! Final Audio: {output_wav}")
            else:
                print("[!] Conversion failed. Raw file kept at storm_capture.pcm")
        else:
            print(f"[!] ffmpeg not found. Raw audio saved as: {output_pcm}")
