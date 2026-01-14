#!/usr/bin/env python3
"""
Script pour déployer automatiquement sur Render.com via l'API
Version 2 avec serviceDetails
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

service_data = {
    "type": "web_service",
    "name": "taleos-connection-tester",
    "ownerId": OWNER_ID,
    "repo": "https://github.com/Dedale95/mon-site.git",
    "rootDir": "taleos-backend",
    "region": "frankfurt",
    "planId": "render-free",
    "serviceDetails": {
        "env": "python",
        "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium",
        "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"
    }
}

print("🚀 Création du service sur Render.com...")
print(f"📦 Service: {service_data['name']}")
print(f"📁 Repository: {service_data['repo']}")
print(f"📂 Root Directory: {service_data['rootDir']}")
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
