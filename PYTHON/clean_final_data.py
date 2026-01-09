
import csv
import re
from pathlib import Path
from city_normalizer import normalize_city
from country_normalizer import normalize_country

HTML_DIR = Path('/Users/thibault/Documents/Projet TALEOS/Antigravity/HTML')
INPUT_CSV = HTML_DIR / 'scraped_jobs.csv'
OUTPUT_CSV = HTML_DIR / 'scraped_jobs_cleaned.csv'

# Keywords that indicate it's an address or company, not a city/region
JUNK_KEYWORDS = [
    'Av.', 'Avenue', 'Rue', 'Boulevard', 'Bd.', 'Allée', 'Allee', 'Floor', 'Th Floor', 
    'Street', 'St.', 'Chaussee', 'Chaussée', 'Place', 'Square', 'Route', 'Chemin',
    'Crédit Agricole', 'Leasing', 'Factoring', 'S.A.', 'Gmbh', 'Co. Kg', 'Consumer Finance',
    'Linares Rivas', 'Miguel Bombarda'
]

def is_junk_region(region):
    if not region:
        return False
    # Check for junk keywords
    if any(k.lower() in region.lower() for k in JUNK_KEYWORDS):
        return True
    # Check if it starts with a number (like street number) but is not a postal code (5 digits)
    # Actually, postal codes are usually fine if mapped, but "2 Central Blvd" starts with digit
    if re.match(r'^\d{1,4}\s', region):
        return True
    return False

def clean_row(row):
    location = row.get('location', '')
    if not location or ' - ' not in location:
        return row

    parts = location.split(' - ')
    raw_city = parts[0].strip()
    raw_country = parts[1].strip()

    # 1. Clean Country
    # Handle leading hyphen case "- France" -> "France"
    if raw_country.startswith('- '):
        raw_country = raw_country[2:]
    
    clean_country = normalize_country(raw_country)
    if not clean_country:
        clean_country = raw_country # Fallback

    # 2. Clean Region/City
    clean_region = raw_city
    
    # If junk detected
    if is_junk_region(raw_city):
        # If it's junk, we try to salvage or default to Country
        # Strategy: If France, try to find a valid city in the string? 
        # Or just invalidate it.
        # For now, if junk, we assume it's lost and set region = clean_country (so it shows as "France - France")
        clean_region = clean_country

    # Special rule: If France, Region MUST be a region (handled by frontend city mapping) 
    # OR we can pre-normalize here? 
    # The frontend does `cityToRegion`, so we just need a valid City name.
    # If "France", we want strictly valid cities.
    
    if clean_country == 'France':
        if clean_region == 'France':
            pass # "France - France" is generic
        else:
            # Maybe check if it's a known city?
            # For now relying on junk filter is good first step.
            pass

    # Reconstruct location
    row['location'] = f"{clean_region} - {clean_country}"
    return row

def main():
    print(f"Reading {INPUT_CSV}...")
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    cleaned_rows = []
    junk_count = 0
    
    for row in rows:
        old_loc = row.get('location', '')
        new_row = clean_row(row)
        if new_row['location'] != old_loc:
            # print(f"Fixed: '{old_loc}' -> '{new_row['location']}'")
            if is_junk_region(old_loc.split(' - ')[0]):
                junk_count += 1
        cleaned_rows.append(new_row)

    print(f"Cleaned {len(cleaned_rows)} rows.")
    print(f"Removed junk regions from {junk_count} rows.")

    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"Saved to {OUTPUT_CSV}")
    
    # Verify "- France"
    check_countries = set()
    for r in cleaned_rows:
        loc = r.get('location', '')
        if ' - ' in loc:
            check_countries.add(loc.split(' - ')[1])
    
    print("Remaining Countries:", sorted(list(check_countries))[:20])

if __name__ == '__main__':
    main()
