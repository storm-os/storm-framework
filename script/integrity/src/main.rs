use sha2::{Sha256, Digest};
use std::fs;
use std::io;
use std::collections::{HashMap, HashSet};
use std::path::Path;
use walkdir::WalkDir;
use serde_json;

// Fungsi untuk menghitung Hash SHA256 dari sebuah file
fn calculate_hash(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

fn main() {
    // Path database sesuai permintaanmu (hardcoded)
    let db_path = "tests/database/signed_manifest.json";
    
    // Daftar folder dan file yang wajib diabaikan agar tidak bentrok
    let ignored_items = [
        ".git", 
        "__pycache__", 
        ".pytest_cache", 
        ".github", 
        "storm.db", 
        "tests", 
        "script/integrity"
    ];

    // 1. Load Database JSON
    let data = match fs::read_to_string(db_path) {
        Ok(content) => content,
        Err(_) => {
            println!("[-] ERROR: Manifest file not found in {}", db_path);
            return;
        }
    };

    let database: HashMap<String, String> = match serde_json::from_str(&data) {
        Ok(map) => map,
        Err(_) => {
            println!("[-] ERROR: JSON format in {} damaged!", db_path);
            return;
        }
    };

    let mut verified_count = 0;
    let mut untracked_files = Vec::new();
    let mut modified_files = Vec::new();
    let mut found_in_disk = HashSet::new();

    // 2. Scan Seluruh Penjuru Tools (Rekursif)
    for entry in WalkDir::new(".").into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let path_str = path.to_str().unwrap_or("");

        // Cek filter pengabaian
        if ignored_items.iter().any(|&ignored| path_str.contains(ignored)) {
            continue;
        }

        if path.is_file() {
            // Normalisasi path agar sinkron dengan JSON (hapus ./ di depan)
            let clean_path = path_str.strip_prefix("./").unwrap_or(path_str);
            
            // Simpan track file yang ditemukan di disk
            found_in_disk.insert(clean_path.to_string());

            match database.get(clean_path) {
                Some(saved_hash) => {
                    // File terdaftar, cek integritas hash-nya
                    let current_hash = calculate_hash(path).unwrap_or_default();
                    if &current_hash == saved_hash {
                        verified_count += 1;
                    } else {
                        modified_files.push(clean_path.to_string());
                    }
                }
                None => {
                    // File ada di folder tapi tidak ada di JSON
                    untracked_files.push(clean_path.to_string());
                }
            }
        }
    }

    // 3. Output Hasil Audit
    if !modified_files.is_empty() {
        println!("\n[!] WARNING: The Following Files Have Been Modified!");
        for f in &modified_files { println!("    -> {}", f); }
    }

    if !untracked_files.is_empty() {
        println!("\n[?] INFO: Illegal/Unknown Files Found!");
        for f in &untracked_files { println!("    -> {}", f); }
    }

    // 4. Cek apakah ada file yang terdaftar di JSON tapi fisiknya hilang
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
    println!("[*] Synchronous: {} file | Modification: {} | Illegal: {}", 
             verified_count, 
             database.len() as i32 - verified_count as i32, 
             untracked_files.len());
}
