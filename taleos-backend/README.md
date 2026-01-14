# Taleos Connection Tester API

Backend API pour tester les connexions aux sites de carrière bancaires.

## 🚀 Déploiement sur Render.com

1. Push ce repo sur GitHub
2. Créer un compte sur [render.com](https://render.com)
3. Créer un nouveau "Web Service"
4. Connecter le repo GitHub
5. Render détecte automatiquement le `render.yaml`
6. Cliquer sur "Create Web Service"
7. Attendre 5-10 minutes (premier build avec Playwright)
8. Récupérer l'URL : `https://taleos-connection-tester.onrender.com`

## 📋 API Endpoints

### GET /health
Endpoint de santé pour vérifier que l'API fonctionne.

**Réponse :**
```json
{
  "status": "ok",
  "message": "Taleos Connection Tester API is running"
}
```

### POST /api/test-bank-connection
Teste une connexion bancaire.

**Requête :**
```json
{
  "bank_id": "credit_agricole",
  "email": "user@example.com",
  "password": "password123"
}
```

**Réponse (succès) :**
```json
{
  "success": true,
  "message": "Connexion réussie ! Votre compte Crédit Agricole est maintenant lié.",
  "details": {
    "url": "https://...",
    "reason": "application_form_detected"
  }
}
```

**Réponse (échec) :**
```json
{
  "success": false,
  "message": "Connexion échouée: identifiants incorrects ou compte invalide",
  "details": {
    "url": "https://...",
    "error_found": "incorrect"
  }
}
```

## 🧪 Test Local

```bash
# Installer les dépendances
pip install -r requirements.txt
playwright install chromium

# Lancer le serveur
python app.py

# Tester
curl http://localhost:5000/health
```

## ⚠️ Limitations du plan gratuit Render

- **Cold start** : 20-30 secondes après 15 minutes d'inactivité
- **Timeout** : 120 secondes max par requête
- **RAM** : 512 MB
- **Heures** : 750 heures/mois

## 🔧 Configuration

Les configurations des banques sont dans `BANK_CONFIGS` dans `app.py`.
