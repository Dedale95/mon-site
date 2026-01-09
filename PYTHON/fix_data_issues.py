#!/usr/bin/env python3
"""
Script de correction des données dans les bases SQLite
- Harmonise les pays (supprime "- France")
- Nettoie les localisations (enlève adresses et noms d'entreprises)
- Normalise les niveaux d'études
"""

import sqlite3
import re
from pathlib import Path
from city_normalizer import normalize_city
from country_normalizer import normalize_country

# Chemins des bases de données
PYTHON_DIR = Path(__file__).parent
CA_DB = PYTHON_DIR / "credit_agricole_jobs.db"
SG_DB = PYTHON_DIR / "societe_generale_jobs.db"
DELOITTE_DB = PYTHON_DIR / "deloitte_jobs.db"

# Mots-clés à détecter comme adresses ou noms d'entreprises
ADDRESS_KEYWORDS = [
    'av.', 'avenue', 'road', 'street', 'boulevard', 'blvd', 'drive', 'lane',
    'floor', 'tower', 'building', '#', 'º', 'th floor', 'gmbh', 'co.', 'kg',
    'leasing', 'factoring', 'merca', 'crédit agricole', 's.a.', 'lilienthalallee'
]

COMPANY_KEYWORDS = [
    'crédit agricole', 'leasing', 'factoring', 'gmbh', 'co.', 's.a.',
    'indosuez', 'amundi', 'caceis', 'lcl', 'bforbank'
]

def clean_location(location_raw):
    """
    Nettoie la localisation pour enlever les adresses et noms d'entreprises
    Retourne None si c'est une adresse/nom d'entreprise, sinon la localisation nettoyée
    """
    if not location_raw:
        return None
    
    location_lower = location_raw.lower()
    
    # Détecter si c'est une adresse complète
    has_address = any(keyword in location_lower for keyword in ADDRESS_KEYWORDS)
    
    # Détecter si c'est un nom d'entreprise
    has_company = any(keyword in location_lower for keyword in COMPANY_KEYWORDS)
    
    if has_address or has_company:
        # Essayer d'extraire la ville/pays si possible
        # Format attendu: "Ville - Pays" ou juste "Ville"
        
        # Si contient " - ", c'est probablement "Ville - Pays"
        if ' - ' in location_raw:
            parts = location_raw.split(' - ')
            city_part = parts[0].strip()
            country_part = parts[1].strip() if len(parts) > 1 else None
            
            # Nettoyer la partie ville
            city_clean = normalize_city(city_part)
            
            # Si la ville nettoyée est vide ou contient encore des mots-clés d'adresse, c'est suspect
            if not city_clean or any(kw in city_clean.lower() for kw in ADDRESS_KEYWORDS + COMPANY_KEYWORDS):
                # Essayer de trouver une vraie ville dans le texte
                # Chercher des mots qui ressemblent à des villes connues
                known_cities = ['paris', 'lyon', 'marseille', 'london', 'luxembourg', 'munich', 
                               'münchen', 'coruña', 'madrid', 'barcelone', 'singapore', 'genève']
                found_city = None
                for city in known_cities:
                    if city in location_lower:
                        found_city = normalize_city(city)
                        break
                
                if found_city:
                    city_clean = found_city
                else:
                    # Si on ne trouve pas de ville valide, retourner None
                    return None
            
            # Nettoyer le pays
            if country_part:
                country_clean = normalize_country(country_part)
                # Supprimer le préfixe "- " si présent
                if country_clean.startswith('- '):
                    country_clean = country_clean[2:].strip()
                if country_clean.lower() == 'france':
                    country_clean = 'France'
            else:
                country_clean = 'France'  # Par défaut si pas de pays
            
            return f"{city_clean} - {country_clean}"
        else:
            # Pas de format "Ville - Pays", essayer de normaliser directement
            city_clean = normalize_city(location_raw)
            if city_clean and not any(kw in city_clean.lower() for kw in ADDRESS_KEYWORDS + COMPANY_KEYWORDS):
                # Déterminer le pays selon la ville
                if city_clean.lower() in ['paris', 'lyon', 'marseille', 'toulouse', 'bordeaux', 'lille', 'nice', 'nantes']:
                    country = 'France'
                elif city_clean.lower() in ['luxembourg']:
                    country = 'Luxembourg'
                elif city_clean.lower() in ['genève', 'zurich', 'lausanne']:
                    country = 'Suisse'
                else:
                    country = 'France'  # Par défaut
                return f"{city_clean} - {country}"
            else:
                return None
    
    # Si pas d'adresse/entreprise détectée, normaliser normalement
    if ' - ' in location_raw:
        parts = location_raw.split(' - ')
        city_part = parts[0].strip()
        country_part = parts[1].strip() if len(parts) > 1 else 'France'
        
        # Supprimer le préfixe "- " du pays
        if country_part.startswith('- '):
            country_part = country_part[2:].strip()
        
        city_clean = normalize_city(city_part)
        country_clean = normalize_country(country_part)
        
        # Harmoniser "France" et "- France"
        if country_clean.lower() == 'france' or country_clean == '- France':
            country_clean = 'France'
        
        return f"{city_clean} - {country_clean}"
    else:
        # Pas de format "Ville - Pays", essayer de deviner
        city_clean = normalize_city(location_raw)
        return f"{city_clean} - France"  # Par défaut France

def normalize_education_level(edu):
    """
    Normalise les niveaux d'études selon les règles :
    - Bac+3 et Bachelor → même niveau
    - Certificat Fédéral de Capacité et Bac → fusionner
    - Inférieur à Bac et Bac → fusionner
    - Master et Bac+5 → fusionner
    """
    if not edu:
        return edu
    
    edu_lower = edu.lower().strip()
    
    # Mapping de normalisation
    education_mapping = {
        # Bachelor → Bac + 3 / L3
        'bachelor': 'Bac + 3 / L3',
        'bac + 3': 'Bac + 3 / L3',
        'bac+3': 'Bac + 3 / L3',
        'licence': 'Bac + 3 / L3',
        'l3': 'Bac + 3 / L3',
        
        # Master → Bac + 5 / M2 et plus
        'master': 'Bac + 5 / M2 et plus',
        'm2': 'Bac + 5 / M2 et plus',
        'mba': 'Bac + 5 / M2 et plus',
        'bac + 5': 'Bac + 5 / M2 et plus',
        'bac+5': 'Bac + 5 / M2 et plus',
        'grande école': 'Bac + 5 / M2 et plus',
        'école d\'ingénieur': 'Bac + 5 / M2 et plus',
        'école de commerce': 'Bac + 5 / M2 et plus',
        
        # Certificat Fédéral de Capacité → Bac
        'certificat fédéral de capacité': 'Bac',
        'cfc': 'Bac',
        'certificat  fédéral de capacité': 'Bac',
        
        # Inférieur à Bac → Bac
        'inférieur à bac': 'Bac',
        'inférieur au bac': 'Bac',
        'sans bac': 'Bac',
        
        # Bac → Bac
        'bac': 'Bac',
        'baccalauréat': 'Bac',
    }
    
    # Vérifier les correspondances exactes d'abord
    for key, value in education_mapping.items():
        if key in edu_lower:
            return value
    
    # Si déjà dans un format standard, le garder
    standard_levels = [
        'Bac', 'Bac + 2 / L2', 'Bac + 3 / L3', 'Bac + 4 / M1',
        'Bac + 5 / M2 et plus'
    ]
    if edu in standard_levels:
        return edu
    
    # Sinon retourner tel quel
    return edu

def fix_database(db_path, db_name):
    """Corrige les données dans une base SQLite"""
    if not db_path.exists():
        print(f"⚠️ Base de données manquante : {db_path}")
        return
    
    print(f"\n📁 Correction de {db_name}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer tous les jobs
    cursor.execute("SELECT job_url, location, education_level FROM jobs WHERE is_valid = 1")
    jobs = cursor.fetchall()
    
    updated_count = 0
    
    for job_url, location, education_level in jobs:
        updated = False
        
        # Corriger la localisation
        if location:
            new_location = clean_location(location)
            if new_location and new_location != location:
                cursor.execute("UPDATE jobs SET location = ? WHERE job_url = ?", (new_location, job_url))
                updated = True
        
        # Corriger le niveau d'études
        if education_level:
            new_education = normalize_education_level(education_level)
            if new_education != education_level:
                cursor.execute("UPDATE jobs SET education_level = ? WHERE job_url = ?", (new_education, job_url))
                updated = True
        
        if updated:
            updated_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"   ✅ {updated_count} offres corrigées sur {len(jobs)}")

def main():
    print("=" * 80)
    print("🔧 CORRECTION DES DONNÉES DANS LES BASES SQLITE")
    print("=" * 80)
    
    # Corriger chaque base
    fix_database(CA_DB, "Crédit Agricole")
    fix_database(SG_DB, "Société Générale")
    fix_database(DELOITTE_DB, "Deloitte")
    
    print("\n" + "=" * 80)
    print("✅ CORRECTIONS TERMINÉES")
    print("=" * 80)
    print("\n💡 N'oubliez pas d'exécuter export_sqlite_to_json.py pour mettre à jour le JSON")

if __name__ == "__main__":
    main()
