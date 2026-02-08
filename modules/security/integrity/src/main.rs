use sha2::{Sha256, Digest};
use std::fs;
use std::io;
use std::collections::{HashMap, HashSet};
use std::path::Path;
use walkdir::WalkDir;
use serde::Deserialize; // Tambahkan ini

// 1. Definisikan struktur sesuai isi JSON bertingkat kamu
#[derive(Deserialize)]
struct FileInfo {
    sha256: String,
    #[allow(dead_code)]
    size_bytes: u64,
}

// Fungsi untuk menghitung Hash SHA256 dari sebuah file
fn calculate_hash(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

fn main() {
    let db_path = "tests/database/signed_manifest.json";

    // Daftar folder dan file yang wajib diabaikan
    let ignored_items = [
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".github",
        "storm.db",
        "signed_manifest.json",
        "script/integrity",
        "target" // Tambahkan target agar tidak men-scan hasil compile sendiri
    ];

    // 1. Load Database JSON
    let data = match fs::read_to_string(db_path) {
        Ok(content) => content,
        Err(_) => {
            println!("[-] ERROR: Manifest file not found in {}", db_path);
            return;
        }
    };

    // 2. Gunakan HashMap<String, FileInfo> karena JSON kamu bertingkat
    let database: HashMap<String, FileInfo> = match serde_json::from_str(&data) {
        Ok(map) => map,
        Err(_) => {
            println!("[-] ERROR: JSON format in {} damaged or incompatible!", db_path);
            return;
        }
    };

    let mut verified_count = 0;
    let mut untracked_files = Vec::new();
    let mut modified_files = Vec::new();
    let mut found_in_disk = HashSet::new();

    println!("[*] Starting Integrity Deep Scan...");

    // 3. Scan Seluruh Penjuru Tools (Rekursif)
    for entry in WalkDir::new(".").into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let path_str = path.to_str().unwrap_or("");

        // Cek filter pengabaian
        if ignored_items.iter().any(|&ignored| path_str.contains(ignored)) {
            continue;
        }

        if path.is_file() {
            let clean_path = path_str.strip_prefix("./").unwrap_or(path_str);
            found_in_disk.insert(clean_path.to_string());

            match database.get(clean_path) {
                Some(info) => {
                    let current_hash = calculate_hash(path).unwrap_or_default();
                    // Bandingkan dengan field sha256 di dalam objek JSON
                    if current_hash == info.sha256 {
                        verified_count += 1;
                    } else {
                        modified_files.push(clean_path.to_string());
                    }
                }
                None => {
                    untracked_files.push(clean_path.to_string());
                }
            }
        }
    }

    // 4. Output Hasil Audit (Sudah diperbaiki dengan & agar tidak error move)
    if !modified_files.is_empty() {
        println!("\n[!] WARNING: The Following Files Have Been Modified!");
        for f in &modified_files { println!("    -> {}", f); }
    }

    if !untracked_files.is_empty() {
        println!("\n[?] INFO: Illegal/Unknown Files Found!");
        for f in &untracked_files { println!("    -> {}", f); }
    }

    let mut missing_files = Vec::new();
    for (json_path, _) in &database {
        if !found_in_disk.contains(json_path) {
            missing_files.push(json_path);
        }
    }

    if !missing_files.is_empty() {
        println!("\n[!] WARNING: Files Listed But Missing on Disk!");
        for f in &missing_files { println!("    -> {}", f); }
    }

    println!("\n[*] Audit Completed.");
    println!("[*] Verified: {} | Modified: {} | Untracked: {}",
             verified_count,
             modified_files.len(),
             untracked_files.len());
  }

