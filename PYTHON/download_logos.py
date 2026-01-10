#!/usr/bin/env python3
"""
Script pour télécharger les logos d'entreprises depuis Clearbit Logo API
et les sauvegarder localement dans HTML/images/logos/
"""

import requests
import os
from pathlib import Path
from typing import Dict, List, Optional
import time

# Configuration
BASE_DIR = Path(__file__).parent.parent
LOGOS_DIR = BASE_DIR / "HTML" / "images" / "logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)

# Mapping des noms d'entreprises vers leurs domaines pour Clearbit
COMPANY_DOMAINS = {
    # Crédit Agricole et filiales
    "credit_agricole": "credit-agricole.fr",
    "credit_agricole_cib": "ca-cib.com",
    "credit_agricole_assurances": "ca-assurances.fr",
    "credit_agricole_immobilier": "credit-agricole-immobilier.fr",
    "credit_agricole_payment_services": "credit-agricole-payment-services.fr",
    "credit_agricole_group": "credit-agricole.fr",
    
    # Société Générale
    "societe_generale": "societegenerale.com",
    
    # Deloitte
    "deloitte": "deloitte.com",
    "deloitte_france": "deloitte.com",
    
    # Autres entreprises
    "caceis": "caceis.com",
    "lcl": "lcl.fr",
    "credit_lyonnais": "lcl.fr",
    "amundi": "amundi.com",
    "bbforbank": "bforbank.com",
    "bforbank": "bforbank.com",
    "indosuez_wealth_management": "indosuez.com",
    "indosuez": "indosuez.com",
    "uptevia": "uptevia.com",
    "idia_capital_investissement": "idia-invest.com",
    "idia": "idia-invest.com",
}

# Noms de fichiers à générer (basés sur la normalisation du code JavaScript)
COMPANY_LOGOS_TO_DOWNLOAD = [
    "credit_agricole",
    "societe_generale",
    "deloitte",
    "deloitte_france",
    "caceis",
    "lcl",
    "amundi",
    "bforbank",
    "indosuez",
    "uptevia",
    "idia",
]


def download_logo(domain: str, filename: str, size: int = 128) -> bool:
    """
    Télécharge un logo depuis Clearbit Logo API
    
    Args:
        domain: Le domaine de l'entreprise (ex: "credit-agricole.fr")
        filename: Le nom du fichier de sortie (sans extension)
        size: La taille du logo (par défaut 128px)
    
    Returns:
        True si le téléchargement a réussi, False sinon
    """
    url = f"https://logo.clearbit.com/{domain}"
    
    try:
        print(f"📥 Téléchargement de {domain}...", end=" ", flush=True)
        
        # Télécharger avec une taille spécifique
        response = requests.get(url, params={"size": size}, timeout=10)
        
        if response.status_code == 200 and response.content:
            # Vérifier que c'est bien une image
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                # Sauvegarder en PNG
                output_path = LOGOS_DIR / f"{filename}.png"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Vérifier que le fichier n'est pas vide
                if output_path.stat().st_size > 0:
                    print(f"✅ Sauvegardé : {output_path.name} ({output_path.stat().st_size} bytes)")
                    return True
                else:
                    print(f"❌ Fichier vide")
                    output_path.unlink()
                    return False
            else:
                print(f"❌ Pas une image (content-type: {content_type})")
                return False
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False


def normalize_company_name(name: str) -> str:
    """
    Normalise le nom d'une entreprise pour correspondre à la logique JavaScript
    """
    normalized = name.lower().strip()
    
    # Supprimer les accents (simplifié)
    replacements = {
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    # Supprimer les suffixes juridiques
    import re
    normalized = re.sub(r'\s*\(s\.a\.?\)\s*', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*s\.a\.?\s*$', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*sas\s*$', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*sarl\s*$', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*sa\s*$', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*group\s*$', '', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\s*groupe\s*$', '', normalized, flags=re.IGNORECASE)
    
    # Remplacer les caractères spéciaux par des underscores
    normalized = re.sub(r'[^a-z0-9\s-]', '', normalized)
    normalized = re.sub(r'\s+', '_', normalized)
    normalized = re.sub(r'_+', '_', normalized)
    normalized = normalized.strip('_')
    
    return normalized


def main():
    """Télécharge tous les logos nécessaires"""
    print("🚀 Début du téléchargement des logos d'entreprises\n")
    print(f"📁 Dossier de destination : {LOGOS_DIR}\n")
    
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    for logo_name in COMPANY_LOGOS_TO_DOWNLOAD:
        # Vérifier si le fichier existe déjà
        logo_path = LOGOS_DIR / f"{logo_name}.png"
        if logo_path.exists() and logo_path.stat().st_size > 0:
            print(f"⏭️  {logo_name}.png existe déjà ({logo_path.stat().st_size} bytes)")
            skipped_count += 1
            continue
        
        # Obtenir le domaine correspondant
        domain = COMPANY_DOMAINS.get(logo_name)
        if not domain:
            # Essayer de trouver le domaine par nom similaire
            domain = COMPANY_DOMAINS.get(logo_name.split('_')[0])
        
        if not domain:
            print(f"⚠️  {logo_name} : aucun domaine trouvé dans le mapping")
            failed_count += 1
            continue
        
        # Télécharger le logo
        if download_logo(domain, logo_name, size=128):
            success_count += 1
        else:
            failed_count += 1
        
        # Petit délai pour ne pas surcharger l'API
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"📊 Résumé du téléchargement :")
    print(f"   ✅ Succès : {success_count}")
    print(f"   ⏭️  Ignorés (déjà existants) : {skipped_count}")
    print(f"   ❌ Échecs : {failed_count}")
    print(f"{'='*60}\n")
    
    if success_count > 0:
        print(f"✨ {success_count} logo(s) téléchargé(s) avec succès dans {LOGOS_DIR}")
    
    if failed_count > 0:
        print(f"⚠️  {failed_count} logo(s) n'ont pas pu être téléchargé(s)")


if __name__ == "__main__":
    main()
