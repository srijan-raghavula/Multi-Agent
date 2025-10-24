package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// We have implemented an 'airtel customer service platform' for the prototype, to demonstrate a mock implementation

type QueryRequest struct {
	Query string `json:"query"`
}

// The Customer type holds the basic info required for this implementation
type Customer struct {
	Number   string `json:"number"`
	Plan     string `json:"plan"`
	Balance  string `json:"balance,omitempty"`
	Validity string `json:"validity,omitempty"`
	BillDue  string `json:"bill_due,omitempty"`
	DueDate  string `json:"due_date,omitempty"`
}

// Since this is mock, we have the user data stored in memory instead of a real database
var customers = map[string]Customer{
	"ravi": {
		Number:   "9876543210",
		Plan:     "Prepaid",
		Balance:  "₹245",
		Validity: "12 days",
	},
	"priya": {
		Number:  "9123456780",
		Plan:    "Postpaid",
		BillDue: "₹799",
		DueDate: "25 Oct",
	},
}

// this is the main handler function to find keywords within queries and send back the appropriate information via http
func handleL3(w http.ResponseWriter, r *http.Request) {
	// we reject any other type of requests other than post cuz we are sending in some data first and only post is the valid method here
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// we decode the query and store it in `req`
	var req QueryRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	query := req.Query
	lower := make([]byte, len(query))
	copy(lower, []byte(query))
	q := string(lower)
	q = fmt.Sprintf("%v", query)
	resp := map[string]any{}

	// we are looking for keywords to look up. Right now, we look for `account` and `info` in the query
	switch {
	case contains(q, []string{"account", "info"}):
		for name, c := range customers {
			if contains(q, []string{name}) {
				resp = map[string]any{
					"tool":     "fetch_account_info",
					"customer": name,
					"details":  c,
				}
				respondJSON(w, resp)
				return
			}
		}
		resp = map[string]any{
			"tool":     "fetch_account_info",
			"response": "customer not found",
		}

	case contains(q, []string{"adjust", "billing", "refund"}):
		resp = map[string]any{
			"tool":    "adjust_billing",
			"status":  "success",
			"message": "Billing adjustment of ₹50 processed for the mentioned account.",
		}

	default:
		resp = map[string]any{
			"tool":     "default",
			"response": "No matching MCP tool found for this query.",
		}
	}

	respondJSON(w, resp)
}

// this is a helper function to encode the struct into json to send back through response
func respondJSON(w http.ResponseWriter, data any) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func contains(s string, keys []string) bool {
	for _, k := range keys {
		if len(k) > 0 && (containsWord(s, k)) {
			return true
		}
	}
	return false
}

// more helper funcitons for string processing
func containsWord(s, sub string) bool {
	return len(sub) > 0 && (len(s) >= len(sub)) && (stringContainsInsensitive(s, sub))
}

func stringContainsInsensitive(s, sub string) bool {
	return len(s) >= len(sub) && (indexInsensitive(s, sub) >= 0)
}

func indexInsensitive(s, sub string) int {
	for i := 0; i+len(sub) <= len(s); i++ {
		match := true
		for j := 0; j < len(sub); j++ {
			a := s[i+j]
			b := sub[j]
			if a >= 'A' && a <= 'Z' {
				a += 'a' - 'A'
			}
			if b >= 'A' && b <= 'Z' {
				b += 'a' - 'A'
			}
			if a != b {
				match = false
				break
			}
		}
		if match {
			return i
		}
	}
	return -1
}

// Right now, we have one end point `/handle_l3` through which we operate
func main() {
	http.HandleFunc("/handle_l3", handleL3)
	fmt.Println("MCP server running on :8080")
	http.ListenAndServe(":8080", nil)
}
