import sqlite3
import re
from pathlib import Path
from city_normalizer import normalize_city
from country_normalizer import normalize_country

def normalize_location(location: str) -> str:
    """Same logic as in the updated scraper"""
    if not location:
        return ""

    location = location.strip().strip('"').strip()
    location = re.sub(r'\s+', ' ', location)
    location = re.sub(r'^Lieu\s*:\s*', '', location, flags=re.IGNORECASE)

    city_raw = ""
    country_raw = ""

    if " - " in location:
        parts = [p.strip() for p in location.split(" - ")]
        if len(parts) >= 2:
            city_raw = parts[0]
            country_raw = parts[-1]
        else:
            city_raw = parts[0]
    else:
        # 1. Détection par parenthèses
        paren_match = re.search(r'\((.*?)\)', location)
        if paren_match:
            country_candidate = paren_match.group(1).strip()
            city_raw = re.sub(r'\(.*?\)', '', location).strip()
            country_raw = country_candidate
        else:
            # 2. Détection par mots-clés
            known_countries = [
                "France", "Italie", "Allemagne", "Luxembourg", "Suisse", "Pays-Bas", 
                "États-Unis", "Canada", "Singapour", "Japon", "Royaume-Uni", "United Kingdom",
                "Maroc", "Tunisie", "Algérie", "Belgique", "Espagne", "Portugal", "Irlande", "Cameroun", "Bénin", "Côte D'Ivoire", "Congo"
            ]
            found_country = None
            for c in known_countries:
                if c.lower() in location.lower():
                    found_country = c
                    break
            
            if found_country:
                country_raw = found_country
                city_raw = location.replace(found_country, "").strip()
            else:
                city_raw = location
                country_raw = "France"

    city = normalize_city(city_raw)
    country = normalize_country(country_raw)

    if not city:
        return f"{country} - {country}"
    
    return f"{city} - {country}"

def main():
    db_path = Path(__file__).parent / "credit_agricole_jobs.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT job_url, location FROM jobs")
    rows = cursor.fetchall()

    print(f"Processing {len(rows)} jobs...")
    updates = []
    for url, loc in rows:
        new_loc = normalize_location(loc)
        if new_loc != loc:
            updates.append((new_loc, url))

    print(f"Found {len(updates)} locations to update.")
    
    if updates:
        cursor.executemany("UPDATE jobs SET location = ? WHERE job_url = ?", updates)
        conn.commit()
        print("Database updated.")

    conn.close()

if __name__ == "__main__":
    main()
