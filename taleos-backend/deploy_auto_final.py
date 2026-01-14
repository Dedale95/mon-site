#!/usr/bin/env python3
"""
Script pour déployer automatiquement sur Render.com via l'API
⚠️ IMPORTANT: L'API Render ne supporte PAS les services gratuits (free tier)
Pour un service gratuit, utilisez l'interface web: https://dashboard.render.com
"""
import requests
import json

API_KEY = "rnd_ZG9AMLoiaXln0KtAlhElCQLrqnAL"
API_BASE = "https://api.render.com/v1"
OWNER_ID = "tea-d5jf8nogjchc739csr7g"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Structure complète selon la documentation Render API
service_data = {
    "type": "web_service",
    "name": "taleos-connection-tester",
    "ownerId": OWNER_ID,
    "repo": "https://github.com/Dedale95/mon-site.git",
    "rootDir": "taleos-backend",
    "autoDeploy": True,
    "serviceDetails": {
        "env": "python",
        "region": "frankfurt",
        "plan": "starter",  # Note: "render-free" n'est pas supporté par l'API
        "envSpecificDetails": {
            "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium",
            "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"
        },
        "numInstances": 1
    }
}

print("=" * 60)
print("⚠️  LIMITATION IMPORTANTE")
print("=" * 60)
print()
print("L'API Render.com ne supporte PAS la création de services gratuits.")
print("Pour créer un service gratuit, vous DEVEZ utiliser l'interface web:")
print()
print("  1. Allez sur https://dashboard.render.com")
print("  2. Cliquez sur 'New +' → 'Web Service'")
print("  3. Connectez votre repo GitHub")
print("  4. Render détectera automatiquement render.yaml")
print("  5. Cliquez sur 'Create Web Service'")
print()
print("=" * 60)
print()
print("💡 Si vous voulez quand même utiliser l'API, vous devez:")
print("   - Changer le plan pour 'starter' ou supérieur (payant)")
print("   - Ce script créerait alors un service payant")
print()
print("Voulez-vous continuer? (cela créera un service PAYANT)")
print("Tapez 'OUI' pour continuer, ou appuyez sur Entrée pour annuler: ", end='')

try:
    response = input()
    if response.upper() != "OUI":
        print("✅ Annulé. Utilisez l'interface web pour un service gratuit.")
        exit(0)
except:
    print("✅ Annulé. Utilisez l'interface web pour un service gratuit.")
    exit(0)

print()
print("🚀 Création du service sur Render.com...")
print(f"📦 Service: {service_data['name']}")
print(f"📁 Repository: {service_data['repo']}")
print(f"📂 Root Directory: {service_data['rootDir']}")
print(f"💰 Plan: {service_data['serviceDetails']['plan']} (PAYANT)")
print()

try:
    response = requests.post(
        f"{API_BASE}/services",
        headers=headers,
        json=service_data
    )
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Service créé avec succès!")
        print()
        print(json.dumps(result, indent=2))
        
        service = result.get('service', {})
        if service.get('serviceDetails', {}).get('url'):
            url = service['serviceDetails']['url']
            print()
            print("=" * 60)
            print(f"🌐 URL du service: {url}")
            print("=" * 60)
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
