#!/usr/bin/env python3
"""
Script principal pour mettre à jour toutes les offres d'emploi
- Scrape Crédit Agricole
- Scrape Société Générale
- Fusionne dans scraped_jobs.csv
"""

import subprocess
import sys
import csv
from datetime import datetime

print("=" * 80)
print("🚀 MISE À JOUR DES OFFRES D'EMPLOI")
print("=" * 80)
print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. Scraper Crédit Agricole
print("1️⃣ Lancement du scraper Crédit Agricole...")
try:
    result = subprocess.run([sys.executable, "credit_agricole_scraper.py"], 
                          capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        print("✅ Scraper CA terminé avec succès")
    else:
        print(f"⚠️ Scraper CA a retourné un code d'erreur: {result.returncode}")
except Exception as e:
    print(f"❌ Erreur lors du scraping CA: {e}")

print()

# 2. Scraper Société Générale
print("2️⃣ Lancement du scraper Société Générale...")
try:
    result = subprocess.run([sys.executable, "societe_generale_scraper_improved.py"],
                          capture_output=True, text=True, timeout=900)
    if result.returncode == 0:
        print("✅ Scraper SG terminé avec succès")
    else:
        print(f"⚠️ Scraper SG a retourné un code d'erreur: {result.returncode}")
except Exception as e:
    print(f"❌ Erreur lors du scraping SG: {e}")

print()

# 3. Fusion des données
print("3️⃣ Fusion des données dans scraped_jobs.csv...")
# TODO: Implémenter la logique de fusion
print("⚠️ Fusion manuelle nécessaire pour le moment")

print()
print("=" * 80)
print("✅ MISE À JOUR TERMINÉE")
print("=" * 80)

