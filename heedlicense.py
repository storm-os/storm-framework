import os

# Definisikan Header Dasar
AUTHOR = "2026 Storm Framework"
LICENSE_INFO = "Licensed under the MIT License.\n\nSee LICENSE file in the project root for full license information."

def get_header(ext):
    """Mengembalikan format header sesuai ekstensi file"""
    if ext in ['.py', '.sh']:
        return f"# Copyright (c) {AUTHOR}\n\n# {LICENSE_INFO}\n\n"

    if ext in ['.rs', '.go', '.c', '.cpp', '.h']:
        return f"// Copyright (c) {AUTHOR}\n// {LICENSE_INFO}\n\n"

    return None

def stamp_storm_project(root_dir):
    supported_extensions = ['.py', '.sh', '.rs', '.go', '.c', '.cpp', '.h']

    for root, dirs, files in os.walk(root_dir):
        if any(x in root for x in ["vendor", "target", "cache", "node_modules", ".git"]):
            continue

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in supported_extensions:
                file_path = os.path.join(root, file)
                header = get_header(ext)

                if header:
                    with open(file_path, "r") as f:
                        lines = f.readlines()

                    if not lines: continue

                    # Cek apakah sudah ada lisensi
                    content_str = "".join(lines)
                    if "Storm Framework" in content_str[:150]:
                        continue

                    print(f"[+] Stamping {ext}: {file_path}")
                    if lines[0].startswith("#!"):
                        new_content = lines[0] + header + "".join(lines[1:])
                    else:
                        new_content = header + content_str

                    with open(file_path, "w") as f:
                        f.write(new_content)

if __name__ == "__main__":
    stamp_storm_project(".")
    print("\n[✓] Semua bahasa tersertifikasi storm!")
