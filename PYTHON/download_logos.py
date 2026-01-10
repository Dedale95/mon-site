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
    Télécharge un logo depuis Clearbit Logo API avec plusieurs tentatives et méthodes alternatives
    
    Args:
        domain: Le domaine de l'entreprise (ex: "credit-agricole.fr")
        filename: Le nom du fichier de sortie (sans extension)
        size: La taille du logo (par défaut 128px)
    
    Returns:
        True si le téléchargement a réussi, False sinon
    """
    # Essayer plusieurs services alternatifs (Clearbit a été discontinué le 1er décembre 2025)
    # Brandfetch offre un endpoint gratuit sans clé API
    urls_to_try = [
        # Brandfetch - Endpoint gratuit sans authentification
        f"https://cdn.brandfetch.io/{domain}/logo?transparent=true",
        f"https://cdn.brandfetch.io/{domain}/logo",
        # Logo.dev (nécessite clé API - on essaie quand même au cas où)
        f"https://img.logo.dev/{domain}?token=free",
        # Ancien Clearbit (discontinué mais on essaie au cas où)
        f"https://logo.clearbit.com/{domain}?size={size}",
        f"https://logo.clearbit.com/{domain}",
    ]
    
    for url in urls_to_try:
        try:
            print(f"📥 Tentative {domain} ({url[:50]}...)...", end=" ", flush=True)
            
            # Configuration avec retry automatique et headers
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            adapter = requests.adapters.HTTPAdapter(max_retries=3)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            # Télécharger avec timeout plus long et retry
            response = session.get(url, timeout=20, allow_redirects=True, verify=True)
            
            if response.status_code == 200 and response.content:
                # Vérifier que c'est bien une image
                content_type = response.headers.get('content-type', '')
                # Accepter les types image ou SVG
                if 'image' in content_type or 'svg' in content_type or len(response.content) > 100:
                    # Vérifier la signature du fichier (magic bytes)
                    is_image = (
                        response.content.startswith(b'\x89PNG') or  # PNG
                        response.content.startswith(b'\xff\xd8\xff') or  # JPEG
                        response.content.startswith(b'GIF') or  # GIF
                        response.content.startswith(b'<svg') or  # SVG
                        b'<?xml' in response.content[:100]  # XML/SVG
                    )
                    
                    if is_image:
                        # Sauvegarder en PNG (ou conserver le format original)
                        output_path = LOGOS_DIR / f"{filename}.png"
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        
                        # Vérifier que le fichier n'est pas vide
                        file_size = output_path.stat().st_size
                        if file_size > 100:  # Au moins 100 bytes
                            print(f"✅ Sauvegardé : {output_path.name} ({file_size} bytes)")
                            return True
                        else:
                            print(f"❌ Fichier trop petit ({file_size} bytes)")
                            if output_path.exists():
                                output_path.unlink()
                            continue
                    else:
                        print(f"⚠️ Pas une image valide")
                        continue
                else:
                    print(f"⚠️ Content-type: {content_type}")
                    continue
            elif response.status_code == 404:
                print(f"⚠️ Logo non trouvé (404)")
                continue
            else:
                print(f"⚠️ HTTP {response.status_code}")
                continue
                
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout")
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Erreur connexion : {str(e)[:50]}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur : {str(e)[:50]}")
            continue
        except Exception as e:
            print(f"❌ Erreur inattendue : {str(e)[:50]}")
            continue
    
    print(f"❌ Toutes les tentatives ont échoué")
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
