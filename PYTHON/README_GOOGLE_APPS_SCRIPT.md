# Configuration Google Apps Script pour les Tests de Connexion

## ⚠️ Important : Google Apps Script ne peut PAS exécuter directement Python/Selenium

Google Apps Script exécute uniquement du **JavaScript**. Il ne peut pas exécuter directement votre script Python avec Selenium.

## Options disponibles

### Option 1 : Google Apps Script + Service Externe (Recommandé)

Votre Google Apps Script appelle un service externe qui exécute le script Python.

**Architecture :**
```
Frontend → Google Apps Script → Service Externe (Python/Selenium) → Résultat
```

**Services possibles :**
1. **Google Cloud Functions** (gratuit jusqu'à un certain seuil)
2. **AWS Lambda** 
3. **Heroku** (gratuit pour hobby)
4. **Votre propre serveur web**
5. **Autre service cloud**

### Option 2 : Réimplémenter en JavaScript (Complexe)

Réimplémenter toute la logique de test de connexion en JavaScript dans Google Apps Script. Mais **Selenium n'existe pas en JavaScript côté serveur**, donc c'est très difficile/impossible.

## Configuration Option 1 : Service Externe

### Étape 1 : Déployer votre script Python quelque part

Par exemple, avec Google Cloud Functions :

1. Créer une Cloud Function qui exécute votre script Python
2. Cette fonction reçoit les paramètres et exécute `test_bank_connection.py`
3. Retourne le résultat en JSON

### Étape 2 : Configurer Google Apps Script

1. Copier le code de `google_apps_script_code.js` dans votre Google Apps Script
2. Modifier `PYTHON_SERVICE_URL` avec l'URL de votre service externe
3. Déployer comme "Web App" :
   - **Exécuter en tant que** : Moi
   - **Qui a accès** : Tous (y compris les utilisateurs anonymes)

### Étape 3 : Tester

Utiliser l'URL de déploiement dans votre frontend.

## Alternative : Utiliser directement le service externe

Si vous déployez votre script Python comme API (Cloud Functions, serveur web, etc.), vous pouvez **sauter Google Apps Script** et appeler directement l'API depuis le frontend.

**Avantage :** Plus simple, moins de latence

**Inconvénient :** Vous devez gérer l'authentification/rate limiting vous-même

## Exemple : Google Cloud Functions

Si vous utilisez Google Cloud Functions, voici un exemple :

```python
# main.py (dans Cloud Functions)
from test_bank_connection import test_connection_sync

def test_connection(request):
    request_json = request.get_json()
    bank_id = request_json.get('bank_id')
    email = request_json.get('email')
    password = request_json.get('password')
    
    result = test_connection_sync(bank_id, email, password)
    return result, 200
```

Puis votre frontend appelle directement l'URL de la Cloud Function.

## Recommandation

**Si vous voulez utiliser Google Apps Script :**
- Utilisez-le comme proxy vers un service externe qui exécute Python
- Mais vous devez d'abord déployer votre script Python quelque part

**Alternative plus simple :**
- Déployez directement votre script Python comme API
- Appelez-le directement depuis le frontend (sans Google Apps Script)

Quelle option préférez-vous ?
