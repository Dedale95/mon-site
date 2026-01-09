# 🚀 Guide de déploiement - Serveur d'authentification

Ce guide vous explique comment déployer le serveur Flask sur **Railway** (gratuit) pour qu'il fonctionne 24/7, même quand votre ordinateur est éteint.

## 📋 Prérequis

- Un compte GitHub (vous l'avez déjà)
- Un compte Gmail (ou autre service email)

## 🎯 Étapes de déploiement sur Railway

### 1. Créer un compte Railway

1. Allez sur https://railway.app
2. Cliquez sur **"Start a New Project"**
3. Connectez-vous avec votre compte GitHub

### 2. Créer un nouveau projet

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez votre dépôt : `mon-site`
4. Railway va détecter automatiquement le projet

### 3. Configurer le service

1. Railway va créer un service automatiquement
2. Cliquez sur le service créé
3. Allez dans l'onglet **"Settings"**
4. Dans **"Root Directory"**, entrez : `PYTHON`
5. Dans **"Start Command"**, entrez : `python auth_server.py`

### 4. Configurer les variables d'environnement

Dans l'onglet **"Variables"**, ajoutez ces variables :

#### Variables obligatoires :

```
SECRET_KEY=votre_cle_secrete_aleatoire
```

Pour générer une clé secrète, exécutez dans un terminal :
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### Variables pour l'envoi d'emails (Gmail) :

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre_email@gmail.com
SMTP_PASSWORD=votre_app_password
EMAIL_FROM=votre_email@gmail.com
```

**Important pour Gmail** :
1. Activez la validation en 2 étapes sur votre compte Google
2. Allez dans https://myaccount.google.com/apppasswords
3. Créez un "App Password" pour "Mail"
4. Utilisez ce mot de passe (16 caractères) comme `SMTP_PASSWORD`

#### Variable BASE_URL (après déploiement) :

Une fois déployé, Railway vous donnera une URL. Ajoutez :

```
BASE_URL=https://votre-app.railway.app
```

### 5. Déployer

1. Railway va automatiquement déployer votre application
2. Attendez quelques minutes que le déploiement se termine
3. Une fois terminé, Railway vous donnera une URL comme : `https://votre-app.railway.app`

### 6. Mettre à jour le frontend

1. Ouvrez `HTML/auth.html`
2. Trouvez la ligne : `const PRODUCTION_API = 'https://VOTRE-APP.railway.app/api';`
3. Remplacez `VOTRE-APP.railway.app` par l'URL que Railway vous a donnée
4. Faites de même dans `HTML/profile.html`
5. Commitez et poussez les changements :

```bash
git add HTML/auth.html HTML/profile.html
git commit -m "Mise à jour: URL API Railway"
git push origin main
```

### 7. Tester

1. Allez sur https://dedale95.github.io/mon-site/auth.html
2. Essayez de vous inscrire
3. Ça devrait fonctionner ! 🎉

## 🔍 Vérifier que le serveur fonctionne

Testez l'endpoint de santé :
```bash
curl https://votre-app.railway.app/api/health
```

Vous devriez recevoir : `{"status":"ok"}`

## 💡 Alternative : Render.com

Si Railway ne vous convient pas, vous pouvez utiliser Render :

1. Allez sur https://render.com
2. Créez un compte
3. Créez un nouveau **Web Service**
4. Connectez votre dépôt GitHub
5. Configuration :
   - **Root Directory** : `PYTHON`
   - **Build Command** : `pip install -r requirements_auth.txt`
   - **Start Command** : `python auth_server.py`
6. Ajoutez les mêmes variables d'environnement que pour Railway

## ⚠️ Notes importantes

- **Gratuit** : Railway offre un plan gratuit avec des limites (500 heures/mois)
- **Base de données** : SQLite est utilisé (fichier local). Pour la production, considérez PostgreSQL
- **Emails** : Les emails de vérification nécessitent une configuration SMTP valide
- **Sécurité** : Ne partagez jamais vos clés secrètes ou mots de passe

## 🆘 Problèmes courants

### Le serveur ne démarre pas
- Vérifiez les logs dans Railway
- Assurez-vous que `requirements_auth.txt` contient toutes les dépendances

### Les emails ne sont pas envoyés
- Vérifiez que `SMTP_USER` et `SMTP_PASSWORD` sont corrects
- Pour Gmail, utilisez un "App Password", pas votre mot de passe normal

### Erreur CORS
- Le code est déjà configuré pour autoriser GitHub Pages
- Vérifiez que `BASE_URL` est correctement configuré

## 📞 Support

Si vous rencontrez des problèmes, vérifiez les logs dans Railway (onglet "Deployments" puis "View Logs").
