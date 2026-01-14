# Guide de Déploiement sur Render.com

## 🔑 Informations de connexion

- **API Key Render** : `rnd_ZG9AMLoiaXln0KtAlhElCQLrqnAL`
- **Repository GitHub** : `https://github.com/Dedale95/mon-site.git`

## 🚀 Méthode 1 : Déploiement via l'interface web (Recommandé)

### Étape 1 : Préparer le repository

1. **Créer un repo séparé pour le backend** (recommandé) ou utiliser le repo actuel
   ```bash
   # Option A : Créer un repo séparé
   cd taleos-backend
   git init
   git add .
   git commit -m "Initial commit - Taleos backend"
   git remote add origin https://github.com/VOTRE-USERNAME/taleos-backend.git
   git push -u origin main
   ```

2. **OU utiliser le repo actuel** : Les fichiers sont déjà dans le repo principal

### Étape 2 : Déployer sur Render.com

1. **Aller sur** [https://dashboard.render.com](https://dashboard.render.com)
2. **Se connecter** avec votre compte (ou créer un compte avec GitHub)
3. **Cliquer sur "New +"** → **"Web Service"**
4. **Connecter votre repository GitHub** :
   - Si le repo est séparé : Sélectionner `taleos-backend`
   - Si le repo est principal : Sélectionner `mon-site` et configurer le **Root Directory** : `taleos-backend`
5. **Render détectera automatiquement le `render.yaml`** :
   - ✅ Name: `taleos-connection-tester`
   - ✅ Region: `frankfurt`
   - ✅ Build Command: (détecté automatiquement)
   - ✅ Start Command: (détecté automatiquement)
6. **Cliquer sur "Create Web Service"**
7. **Attendre 5-10 minutes** pour le premier build (installation de Playwright)

### Étape 3 : Récupérer l'URL

Une fois le déploiement terminé, vous verrez l'URL de votre service :
```
https://taleos-connection-tester.onrender.com
```

### Étape 4 : Mettre à jour connexions.html

Ouvrir `HTML/connexions.html` et mettre à jour l'URL :

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api'  // En développement local
    : 'https://taleos-connection-tester.onrender.com/api';  // En production
```

## 🔧 Méthode 2 : Déploiement via API (Avancé)

Si vous voulez automatiser le déploiement, vous pouvez utiliser l'API Render :

### Prérequis

```bash
# Installer curl et jq
brew install curl jq  # Sur macOS
```

### Étapes API

1. **Créer un service via API** (nécessite plusieurs appels)
2. **Configurer le build et le déploiement**
3. **Récupérer l'URL du service**

**Documentation API Render** : https://render.com/docs/api

**Exemple de création de service via API** :

```bash
curl -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer rnd_ZG9AMLoiaXln0KtAlhElCQLrqnAL" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web_service",
    "name": "taleos-connection-tester",
    "ownerId": "YOUR_OWNER_ID",
    "repo": "https://github.com/Dedale95/mon-site.git",
    "rootDir": "taleos-backend",
    "region": "frankfurt",
    "planId": "render-free",
    "envVars": [],
    "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium",
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"
  }'
```

⚠️ **Note** : L'utilisation de l'API nécessite de connaître votre `ownerId` et d'autres paramètres. L'interface web est beaucoup plus simple.

## ✅ Vérification du déploiement

### Test de santé

```bash
curl https://taleos-connection-tester.onrender.com/health
```

Réponse attendue :
```json
{
  "status": "ok",
  "message": "Taleos Connection Tester API is running"
}
```

### Test de connexion

```bash
curl -X POST https://taleos-connection-tester.onrender.com/api/test-bank-connection \
  -H "Content-Type: application/json" \
  -d '{
    "bank_id": "credit_agricole",
    "email": "test@example.com",
    "password": "test123"
  }'
```

## 📝 Logs

Voir les logs du service :
- Dashboard Render → votre service → onglet "Logs"
- Ou via l'API : `GET /v1/services/{serviceId}/logs`

## 🔄 Mise à jour

Pour mettre à jour le service :
1. Pousser vos modifications sur GitHub
2. Render détectera automatiquement les changements
3. Redéploiera automatiquement (si auto-deploy est activé)

## ⚠️ Limitations du plan gratuit

- **Cold start** : 20-30 secondes après 15 minutes d'inactivité
- **Timeout** : 120 secondes max par requête
- **RAM** : 512 MB
- **Heures** : 750 heures/mois

## 🐛 Dépannage

### Build échoue
- Vérifier les logs dans Render Dashboard
- Vérifier que `requirements.txt` est correct
- Vérifier que Playwright s'installe correctement

### Service ne démarre pas
- Vérifier les logs de démarrage
- Vérifier que le port est bien `$PORT` (variable d'environnement Render)
- Vérifier que Gunicorn est bien installé

### Timeout des requêtes
- Augmenter le timeout dans `render.yaml` (max 120s)
- Optimiser le script pour qu'il soit plus rapide
