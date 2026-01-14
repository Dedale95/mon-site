#!/usr/bin/env python3
"""
Script pour déployer sur Render.com via l'API
Usage: python deploy_render_api.py
"""

import requests
import json
import sys

# Configuration
RENDER_API_KEY = "rnd_ZG9AMLoiaXln0KtAlhElCQLrqnAL"
API_BASE_URL = "https://api.render.com/v1"

# Configuration du service
SERVICE_CONFIG = {
    "type": "web_service",
    "name": "taleos-connection-tester",
    "repo": "https://github.com/Dedale95/mon-site.git",
    "rootDir": "taleos-backend",
    "region": "frankfurt",
    "planId": "render-free",
    "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium",
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120",
    "envVars": []
}

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def get_owners():
    """Récupère la liste des owners (comptes/organisations)"""
    try:
        response = requests.get(f"{API_BASE_URL}/owners", headers=headers)
        response.raise_for_status()
        owners = response.json()
        return owners
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des owners: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Réponse: {e.response.text}")
        return None


def create_service(owner_id):
    """Crée un nouveau service sur Render"""
    service_data = SERVICE_CONFIG.copy()
    service_data["ownerId"] = owner_id
    
    try:
        print(f"🚀 Création du service '{SERVICE_CONFIG['name']}'...")
        response = requests.post(
            f"{API_BASE_URL}/services",
            headers=headers,
            json=service_data
        )
        response.raise_for_status()
        service = response.json()
        print(f"✅ Service créé avec succès!")
        print(f"   ID: {service.get('service', {}).get('id')}")
        print(f"   Nom: {service.get('service', {}).get('name')}")
        return service
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la création du service: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Réponse: {e.response.text}")
        return None


def main():
    print("=" * 60)
    print("🚀 Déploiement automatique sur Render.com")
    print("=" * 60)
    print()
    
    # Vérifier l'API key
    print("📋 Étape 1: Vérification de l'API key...")
    owners = get_owners()
    if not owners:
        print("❌ Impossible de récupérer les owners. Vérifiez votre API key.")
        sys.exit(1)
    
    print(f"✅ API key valide")
    print(f"   Nombre d'owners trouvés: {len(owners)}")
    
    # Afficher les owners
    if owners:
        print("\n📋 Owners disponibles:")
        for i, owner in enumerate(owners):
            owner_type = owner.get('type', 'unknown')
            owner_name = owner.get('name', owner.get('slug', 'unknown'))
            owner_id = owner.get('id', 'unknown')
            print(f"   {i+1}. {owner_name} ({owner_type}) - ID: {owner_id}")
        
        # Utiliser le premier owner (ou demander)
        if len(owners) == 1:
            owner_id = owners[0].get('id')
            print(f"\n✅ Utilisation de l'owner: {owners[0].get('name', owners[0].get('slug'))}")
        else:
            print("\n⚠️  Plusieurs owners trouvés. Utilisation du premier.")
            owner_id = owners[0].get('id')
    else:
        print("❌ Aucun owner trouvé")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("⚠️  IMPORTANT")
    print("=" * 60)
    print()
    print("Le déploiement via API nécessite que:")
    print("1. Le repository GitHub soit déjà connecté à Render")
    print("2. Vous ayez les permissions nécessaires")
    print()
    print("💡 RECOMMANDATION: Utilisez l'interface web de Render.com:")
    print("   1. Allez sur https://dashboard.render.com")
    print("   2. Cliquez sur 'New +' → 'Web Service'")
    print("   3. Connectez votre repo GitHub")
    print("   4. Render détectera automatiquement render.yaml")
    print("   5. Cliquez sur 'Create Web Service'")
    print()
    print("C'est beaucoup plus simple et Render gère tout automatiquement!")
    print()
    
    # Demander confirmation
    response = input("Voulez-vous quand même essayer de créer le service via API? (o/N): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("✅ Déploiement via API annulé. Utilisez l'interface web recommandée.")
        sys.exit(0)
    
    print()
    print("📋 Étape 2: Création du service...")
    service = create_service(owner_id)
    
    if service:
        print()
        print("=" * 60)
        print("✅ Déploiement initié!")
        print("=" * 60)
        print()
        print("Vérifiez le statut sur: https://dashboard.render.com")
        print()
        service_data = service.get('service', {})
        if service_data.get('serviceDetails', {}).get('url'):
            url = service_data['serviceDetails']['url']
            print(f"URL du service: {url}")
        else:
            print("L'URL sera disponible une fois le déploiement terminé.")
    else:
        print()
        print("❌ Échec de la création du service")
        print("💡 Utilisez l'interface web de Render.com pour déployer manuellement.")


if __name__ == "__main__":
    main()
