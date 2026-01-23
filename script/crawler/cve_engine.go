package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 2 { return }
	limit, _ := strconv.Atoi(os.Args[1])

	//  (Example API public)
	resp, err := http.Get("https://api.github.com/advisories?per_page=" + os.Args[1])
	if err != nil { return }
	defer resp.Body.Close()

	var rawData []map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&rawData)

	var results []map[string]interface{}
	for i := 0; i < len(rawData) && i < limit; i++ {
		item := map[string]interface{}{
			"cve":         rawData[i]["cve_id"],
			"name":        rawData[i]["summary"],
			"severity":    rawData[i]["severity"],
			"description": rawData[i]["description"],
			"remediation": []string{"Check official advisory for patch details"},
			"URL":         []string{fmt.Sprintf("https://github.com/advisories/%s", rawData[i]["ghsa_id"])},
			"scanner":     "generic_check.py",
		}
		results = append(results, item)
	}

	output, _ := json.Marshal(results)
	fmt.Println(string(output))
}
