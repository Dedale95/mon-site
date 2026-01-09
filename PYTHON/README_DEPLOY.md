# Déploiement du serveur d'authentification

Ce guide explique comment déployer le serveur Flask sur un service cloud pour qu'il fonctionne 24/7.

## Option 1 : Railway (Recommandé - Gratuit)

### Étapes :

1. **Créer un compte sur Railway** : https://railway.app
2. **Installer Railway CLI** (optionnel) :
   ```bash
   npm i -g @railway/cli
   railway login
   ```

3. **Déployer depuis GitHub** :
   - Allez sur https://railway.app/new
   - Connectez votre dépôt GitHub
   - Sélectionnez le dossier `PYTHON`
   - Railway détectera automatiquement Python et installera les dépendances

4. **Configurer les variables d'environnement** dans Railway :
   - `SECRET_KEY` : Générez une clé secrète (ex: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `SMTP_SERVER` : Votre serveur SMTP (ex: `smtp.gmail.com`)
   - `SMTP_PORT` : Port SMTP (ex: `587`)
   - `SMTP_USER` : Votre email
   - `SMTP_PASSWORD` : Votre mot de passe ou app password
   - `EMAIL_FROM` : Email expéditeur
   - `BASE_URL` : URL de votre déploiement Railway (sera fournie après déploiement)

5. **Récupérer l'URL de l'API** :
   - Railway vous donnera une URL comme `https://votre-app.railway.app`
   - L'API sera accessible sur `https://votre-app.railway.app/api`

## Option 2 : Render (Gratuit)

### Étapes :

1. **Créer un compte sur Render** : https://render.com
2. **Créer un nouveau Web Service** :
   - Connectez votre dépôt GitHub
   - Sélectionnez le dossier `PYTHON`
   - Build Command : `pip install -r requirements_auth.txt`
   - Start Command : `python auth_server.py`

3. **Configurer les variables d'environnement** (même que Railway)

4. **Récupérer l'URL de l'API** :
   - Render vous donnera une URL comme `https://votre-app.onrender.com`
   - L'API sera accessible sur `https://votre-app.onrender.com/api`

## Option 3 : Fly.io (Gratuit)

### Étapes :

1. **Installer Fly CLI** : https://fly.io/docs/getting-started/installing-flyctl/
2. **Créer un compte** : `fly auth signup`
3. **Créer une app** : `fly launch` dans le dossier PYTHON
4. **Configurer les secrets** : `fly secrets set SECRET_KEY=... SMTP_SERVER=...`
5. **Déployer** : `fly deploy`

## Après le déploiement

1. **Mettre à jour l'URL de l'API dans le frontend** :
   - Modifiez `HTML/auth.html` et `HTML/profile.html`
   - Remplacez l'URL de l'API par celle de votre déploiement

2. **Tester l'API** :
   ```bash
   curl https://votre-app.railway.app/api/health
   ```

## Configuration Email

Pour Gmail :
- Activez "App Passwords" dans votre compte Google
- Utilisez l'app password comme `SMTP_PASSWORD`
- `SMTP_SERVER` : `smtp.gmail.com`
- `SMTP_PORT` : `587`
