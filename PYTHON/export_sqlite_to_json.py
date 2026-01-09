#!/usr/bin/env python3
"""
Script pour exporter les données SQLite vers JSON
Utilisé par les fichiers HTML pour charger les données
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Configuration des chemins
PYTHON_DIR = Path(__file__).parent
HTML_DIR = PYTHON_DIR.parent / "HTML"
OUTPUT_JSON = HTML_DIR / "scraped_jobs.json"

# Chemins des bases de données SQLite
CA_DB = PYTHON_DIR / "credit_agricole_jobs.db"
SG_DB = PYTHON_DIR / "societe_generale_jobs.db"
DELOITTE_DB = PYTHON_DIR / "deloitte_jobs.db"

def read_from_db(db_path, company_name):
    """Lit les offres depuis une base SQLite"""
    if not db_path.exists():
        print(f"⚠️ Base de données manquante : {db_path}")
        return []
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        cursor = conn.execute("""
            SELECT 
                job_id, job_title, contract_type, publication_date, location,
                job_family, duration, management_position, status,
                education_level, experience_level, training_specialization,
                technical_skills, behavioral_skills, tools, languages,
                job_description, company_name, company_description, job_url,
                first_seen, last_updated
            FROM jobs 
            WHERE is_valid = 1
            ORDER BY last_updated DESC
        """)
        
        jobs = []
        for row in cursor.fetchall():
            job = dict(row)
            
            # Convertir les JSON strings en listes pour technical_skills et behavioral_skills
            for col in ['technical_skills', 'behavioral_skills']:
                if job.get(col) and isinstance(job[col], str):
                    try:
                        if job[col].startswith('['):
                            # C'est déjà du JSON
                            parsed = json.loads(job[col])
                            job[col] = ', '.join(parsed) if isinstance(parsed, list) else job[col]
                        elif job[col].startswith("['"):
                            # C'est une string Python, essayer de l'évaluer (attention sécurité)
                            # Mais on va plutôt essayer de parser manuellement
                            job[col] = job[col]  # Garder tel quel pour l'instant
                    except:
                        pass  # Garder la valeur originale si le parsing échoue
            
            jobs.append(job)
        
        conn.close()
        return jobs
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture de {db_path}: {e}")
        return []

def main():
    print("=" * 80)
    print("🔄 EXPORT DES DONNÉES SQLITE VERS JSON")
    print("=" * 80)
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_jobs = []
    
    sources_info = [
        ("Crédit Agricole", CA_DB),
        ("Société Générale", SG_DB),
        ("Deloitte", DELOITTE_DB)
    ]
    
    for name, db_path in sources_info:
        print(f"📁 Lecture de {name} depuis {db_path.name}...")
        jobs = read_from_db(db_path, name)
        
        if jobs:
            all_jobs.extend(jobs)
            print(f"   ✅ {len(jobs)} offres lues")
        else:
            print(f"   ⚠️ Aucune offre trouvée dans {db_path.name}")
    
    if all_jobs:
        # Sauvegarder en JSON (version complète)
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"✅ Export terminé : {len(all_jobs)} jobs sauvegardés dans {OUTPUT_JSON}")
        
        # Créer une version allégée avec seulement les offres Live (pour GitHub Pages)
        live_jobs = [job for job in all_jobs if job.get('status') == 'Live']
        OUTPUT_JSON_LIVE = HTML_DIR / "scraped_jobs_live.json"
        with open(OUTPUT_JSON_LIVE, 'w', encoding='utf-8') as f:
            json.dump(live_jobs, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Version allégée créée : {len(live_jobs)} offres Live dans {OUTPUT_JSON_LIVE.name}")
        
        # Afficher la répartition par entreprise
        companies = {}
        for job in all_jobs:
            company = job.get('company_name', 'Unknown')
            companies[company] = companies.get(company, 0) + 1
        
        print("\n📊 Répartition par entreprise:")
        for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {company}: {count} offres")
        
        # Afficher la répartition par statut
        statuses = {}
        for job in all_jobs:
            status = job.get('status', 'Unknown')
            statuses[status] = statuses.get(status, 0) + 1
        
        print("\n📊 Répartition par statut:")
        for status, count in sorted(statuses.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {status}: {count} offres")
    else:
        print("❌ Aucun job à exporter !")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
