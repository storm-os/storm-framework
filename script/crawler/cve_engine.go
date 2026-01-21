package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
)

type CVEData struct {
	CVE         string   `json:"cve"`
	Name        string   `json:"name"`
	Severity    string   `json:"severity"`
	Description string   `json:"description"`
	Remediation []string `json:"remediation"`
	URL         []string `json:"URL"`
	Scanner     string   `json:"scanner"`
}

func main() {
	// 1. Ambil argumen dari Python (os.Args[1])
	if len(os.Args) < 2 {
		return // Keluar jika tidak ada input
	}

	limitStr := os.Args[1]
	limit, err := strconv.Atoi(limitStr) // Ubah string ke integer
	if err != nil {
		return
	}

	var results []CVEData

	// 2. Loop sebanyak angka yang diminta
	for i := 1; i <= limit; i++ {
		// Di sini nantinya proses Scraping/API Fetching
		item := CVEData{
			CVE:         fmt.Sprintf("CVE-2026-%d", 1000+i), // Simulasi ID
			Name:        "Vulnerability Sample " + strconv.Itoa(i),
			Severity:    "HIGH",
			Description: "Deskripsi otomatis untuk CVE ke-" + strconv.Itoa(i),
			Remediation: []string{"Update firmware", "Patch system"},
			URL:         []string{"https://nvd.nist.gov"},
			Scanner:     "scanner_sample.py",
		}
		results = append(results, item)
	}

	// 3. Kirim balik semua data dalam satu paket JSON
	output, _ := json.Marshal(results)
	fmt.Println(string(output))
}
