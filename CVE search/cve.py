import requests
import json

class CVESearchTool:
    def __init__(self, api_key):
        self.api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "apiKey": self.api_key
        }

    def search_cves(self, query, start_index=0, results_per_page=10):
        params = {
            "keyword": query,
            "startIndex": start_index,
            "resultsPerPage": results_per_page,
        }
        response = requests.get(self.api_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve data:", response.status_code, response.text)
            return None

    def display_results(self, cve_data):
        if not cve_data or "vulnerabilities" not in cve_data:
            print("No results found.")
            return
        
        for item in cve_data["vulnerabilities"]:
            cve_id = item["cve"]["id"]
            description = item["cve"]["descriptions"][0]["value"]
            published_date = item["cve"]["published"]
            last_modified = item["cve"]["lastModified"]

            print("="*60)
            print(f"CVE ID: {cve_id}")
            print(f"Description: {description}")
            print(f"Published Date: {published_date}")
            print(f"Last Modified: {last_modified}")
            print("="*60 + "\n")

    def run(self):
        query = input("Enter search query (keyword, CVE ID, or product): ").strip()
        cve_data = self.search_cves(query)
        self.display_results(cve_data)

if __name__ == "__main__":
    api_key = "ece1515f-aae2-49b0-9791-2e9984c91846"  # Replace with your NVD API key
    cve_search_tool = CVESearchTool(api_key)
    cve_search_tool.run()
