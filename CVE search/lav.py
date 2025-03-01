import requests
from datetime import datetime, timedelta

def fetch_mitre_cves(days=7):
    base_url = "https://cveawg.mitre.org/api/cve"
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    params = {
        "time_modified_since": start_date
    }

    try:
        print(f"Fetching vulnerabilities since {start_date}...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("cveItems", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching vulnerabilities: {e}")
        return []

def display_cves(cves):
    if not cves:
        print("No vulnerabilities found.")
        return

    print(f"\n{'ID':<20} {'Description':<60}")
    print("-" * 80)
    for cve in cves:
        cve_id = cve.get("cve", {}).get("CVE_data_meta", {}).get("ID", "N/A")
        description = cve.get("cve", {}).get("description", {}).get("description_data", [{}])[0].get("value", "N/A")
        print(f"{cve_id:<20} {description[:60]}...")
        print("-" * 80)

if __name__ == "__main__":
    days = int(input("Enter the number of days to look back: "))
    cve_data = fetch_mitre_cves(days)
    display_cves(cve_data)
