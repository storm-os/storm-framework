# script/md5_crypt.py
import crypt

from app.colors import C
# --- Fungsi Cracker Utama ---
def execute(options):
    """
    Memecahkan hash password MD5-Crypt menggunakan wordlist.
    """

    shadow_entry = options.get("HASH")
    wordlist_file = options.get("PASS")

    # 1. Parsing Hash dari /etc/shadow
    try:
        parts = shadow_entry.split(':')

        # Pastikan entri memiliki setidaknya 2 bagian (user:hash...)
        if len(parts) < 2:
            print(f"{C.ERROR} Input setidaknya (user:hash...)")
            return

        username = parts[0]
        full_hash = parts[1]

        # Ekstrak Salt untuk MD5-Crypt ($1$)
        if full_hash.startswith('$1$'):
            # Memastikan struktur MD5-Crypt memiliki 3 bagian: $1$salt$hash_value
            salt_parts = full_hash.split('$')
            if len(salt_parts) < 3:
                 print(f"{C.ERROR} Struktur hash MD5-Crypt tidak lengkap.")
                 return

            salt_crypt = f"${salt_parts[1]}${salt_parts[2]}" # Format: $1$t7y583it
        else:
            print(f"{C.ERROR} Format hash tidak didukung (Bukan MD5-Crypt $1$).")
            return
    except Exception as e:
        print(f"{C.ERROR} Error parsing hash: {e}")
        return

    print(f"{C.MENU} \n--- PYTHON SHADOW CRACKER (MD5-Crypt) ---")
    print(f"{C.MENU} [*] Target User: {username}")
    print(f"{C.MENU} [*] Hash Type: MD5-Crypt ($1$)")
    print(f"{C.MENU} [*] Salt: {salt_crypt}")
    print(f"{C.MENU} [*] Memuat Wordlist dari: {wordlist_file}")
    # 2. Memulai Cracking
    try:
        with open(wordlist_file, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue

                # Membuat ulang hash MD5-Crypt dengan salt yang sama
                hashed_word = crypt.crypt(word, salt_crypt)

                print(f"{C.MENU}  Mencoba: {word}{C.RESET}", end='\r')
                # Membandingkan hash yang dibuat ulang dengan hash asli
                if hashed_word == full_hash:
                    print(f"{C.SUCCESS} \n[!!!] PW BERHASIL DITEMUKAN: {username}:{word}")
                    print(f"{C.SUCCESS} --------------------------------------------------")
                    return

        print(f"{C.ERROR} \n[-] Gagal menemukan password dalam wordlist.")

    except FileNotFoundError:
        print(f"{C.ERROR} \n[-] ERROR: File wordlist '{wordlist_file}' tidak ditemukan.")
    except Exception as e:
        print(f"{C.ERROR} \n[-] ERROR tak terduga saat cracking: {e}")
