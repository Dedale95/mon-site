# 🚀 GUIDE DE DÉPLOIEMENT DÉTAILLÉ - ÉTAPE PAR ÉTAPE

Ce guide vous explique **EXACTEMENT** ce que vous devez faire, étape par étape, pour déployer votre serveur d'authentification sur Railway.

---

## 📋 ÉTAPE 1 : PRÉPARER GMAIL POUR L'ENVOI D'EMAILS

### 1.1 Activer la validation en 2 étapes

1. **Ouvrez votre navigateur** et allez sur : https://myaccount.google.com/security
2. **Connectez-vous** avec votre compte Gmail
3. Dans la section **"Connexion à Google"**, cherchez **"Validation en deux étapes"**
4. **Cliquez** sur "Validation en deux étapes"
5. Si ce n'est pas activé, **suivez les instructions** pour l'activer
   - Vous devrez peut-être entrer votre numéro de téléphone
   - Google vous enverra un code par SMS
   - Entrez le code pour confirmer

### 1.2 Créer un "App Password" (mot de passe d'application)

1. **Toujours sur** https://myaccount.google.com/security
2. **Cherchez** la section **"Validation en deux étapes"** (maintenant activée)
3. **Cliquez** sur **"Mots de passe des applications"** (ou "App passwords" en anglais)
4. Si vous ne voyez pas cette option, allez directement sur : https://myaccount.google.com/apppasswords
5. **Sélectionnez** :
   - **Application** : "Mail"
   - **Appareil** : "Autre (nom personnalisé)"
   - **Nom** : Tapez "Railway Auth Server"
6. **Cliquez** sur **"Générer"**
7. **Google va afficher un mot de passe de 16 caractères** (ex: `abcd efgh ijkl mnop`)
8. **COPIEZ CE MOT DE PASSE** (sans les espaces) - vous en aurez besoin plus tard
   - Exemple : si Google affiche `abcd efgh ijkl mnop`, copiez `abcdefghijklmnop`
9. **IMPORTANT** : Notez ce mot de passe dans un endroit sûr, vous ne pourrez plus le voir après

---

## 📋 ÉTAPE 2 : CRÉER UN COMPTE RAILWAY

### 2.1 Aller sur Railway

1. **Ouvrez votre navigateur**
2. **Allez sur** : https://railway.app
3. Vous verrez une page avec un bouton **"Start a New Project"** ou **"Login"**

### 2.2 S'inscrire avec GitHub

1. **Cliquez** sur **"Login"** ou **"Start a New Project"**
2. Railway va vous proposer plusieurs options de connexion
3. **Cliquez** sur **"Login with GitHub"** (ou l'icône GitHub)
4. **Autorisez Railway** à accéder à votre compte GitHub
   - GitHub va vous demander de confirmer
   - **Cliquez** sur **"Authorize Railway"** ou **"Autoriser"**
5. Railway va créer votre compte automatiquement

---

## 📋 ÉTAPE 3 : CRÉER UN NOUVEAU PROJET SUR RAILWAY

### 3.1 Démarrer un nouveau projet

1. **Une fois connecté**, vous verrez un tableau de bord Railway
2. **Cliquez** sur le bouton **"+ New Project"** (en haut à droite ou au centre de l'écran)
3. Une fenêtre s'ouvre avec plusieurs options

### 3.2 Connecter votre dépôt GitHub

1. Dans la fenêtre qui s'ouvre, **cherchez** l'option **"Deploy from GitHub repo"**
2. **Cliquez** sur **"Deploy from GitHub repo"**
3. Railway va vous demander d'autoriser l'accès à vos dépôts GitHub
   - **Cliquez** sur **"Configure GitHub App"** ou **"Autoriser"**
   - **Sélectionnez** votre compte GitHub
   - **Autorisez** Railway à accéder à vos dépôts
4. **Une liste de vos dépôts GitHub s'affiche**
5. **Cherchez** votre dépôt : `mon-site` (ou `Dedale95/mon-site`)
6. **Cliquez** sur votre dépôt `mon-site`
7. Railway va commencer à créer le projet

---

## 📋 ÉTAPE 4 : CONFIGURER LE SERVICE

### 4.1 Accéder aux paramètres du service

1. **Railway a créé un service automatiquement**
2. **Cliquez** sur le service (il devrait s'appeler quelque chose comme "mon-site" ou "web")
3. Vous verrez plusieurs onglets : **"Deployments"**, **"Settings"**, **"Variables"**, etc.

### 4.2 Configurer le répertoire racine

1. **Cliquez** sur l'onglet **"Settings"** (Paramètres)
2. **Faites défiler** jusqu'à la section **"Build & Deploy"**
3. **Cherchez** le champ **"Root Directory"**
4. **Cliquez** dans ce champ
5. **Tapez exactement** : `PYTHON`
   - En majuscules
   - Sans guillemets
   - Sans espace avant ou après
6. **Cliquez** ailleurs pour sauvegarder (ou appuyez sur Entrée)

### 4.3 Configurer la commande de démarrage

1. **Toujours dans "Settings"**, cherchez le champ **"Start Command"**
2. **Cliquez** dans ce champ
3. **Tapez exactement** : `python auth_server.py`
   - En minuscules
   - Sans guillemets
4. **Cliquez** ailleurs pour sauvegarder

### 4.4 Vérifier la configuration

1. **Vérifiez** que vous avez bien :
   - **Root Directory** : `PYTHON`
   - **Start Command** : `python auth_server.py`
2. Si tout est correct, **Railway va automatiquement redéployer** votre application

---

## 📋 ÉTAPE 5 : CONFIGURER LES VARIABLES D'ENVIRONNEMENT

### 5.1 Accéder aux variables

1. **Cliquez** sur l'onglet **"Variables"** (en haut de la page)
2. Vous verrez une section **"Variables"** avec un bouton **"+ New Variable"**

### 5.2 Ajouter la variable SECRET_KEY

1. **Cliquez** sur **"+ New Variable"**
2. Dans le champ **"Key"** (Clé), **tapez** : `SECRET_KEY`
   - En majuscules
   - Avec un underscore
3. Pour générer une valeur, **ouvrez un terminal** sur votre ordinateur et tapez :
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
4. **Copiez** le résultat (une longue chaîne de caractères)
5. **Collez** cette valeur dans le champ **"Value"** (Valeur) de Railway
6. **Cliquez** sur **"Add"** ou **"Save"**

### 5.3 Ajouter les variables SMTP

**Ajoutez ces variables UNE PAR UNE** en cliquant sur **"+ New Variable"** pour chacune :

#### Variable 1 : SMTP_SERVER
- **Key** : `SMTP_SERVER`
- **Value** : `smtp.gmail.com`
- **Cliquez** sur **"Add"**

#### Variable 2 : SMTP_PORT
- **Key** : `SMTP_PORT`
- **Value** : `587`
- **Cliquez** sur **"Add"**

#### Variable 3 : SMTP_USER
- **Key** : `SMTP_USER`
- **Value** : Votre adresse email Gmail (ex: `votre.email@gmail.com`)
- **Cliquez** sur **"Add"**

#### Variable 4 : SMTP_PASSWORD
- **Key** : `SMTP_PASSWORD`
- **Value** : Le mot de passe d'application que vous avez copié à l'étape 1.2 (les 16 caractères sans espaces)
- **Cliquez** sur **"Add"**

#### Variable 5 : EMAIL_FROM
- **Key** : `EMAIL_FROM`
- **Value** : La même adresse email que SMTP_USER (ex: `votre.email@gmail.com`)
- **Cliquez** sur **"Add"**

### 5.4 Vérifier toutes les variables

**Vous devriez avoir exactement 5 variables** :
1. `SECRET_KEY` = (votre clé générée)
2. `SMTP_SERVER` = `smtp.gmail.com`
3. `SMTP_PORT` = `587`
4. `SMTP_USER` = (votre email Gmail)
5. `SMTP_PASSWORD` = (votre app password de 16 caractères)
6. `EMAIL_FROM` = (votre email Gmail)

---

## 📋 ÉTAPE 6 : ATTENDRE LE DÉPLOIEMENT

### 6.1 Vérifier le déploiement

1. **Cliquez** sur l'onglet **"Deployments"** (Déploiements)
2. Vous verrez un déploiement en cours avec un statut **"Building"** ou **"Deploying"**
3. **Attendez** que le statut passe à **"Active"** (cela peut prendre 2-5 minutes)
4. Si vous voyez une erreur (statut rouge), **cliquez** sur le déploiement pour voir les logs

### 6.2 Récupérer l'URL de votre application

1. **Une fois le déploiement terminé** (statut "Active")
2. **Cliquez** sur l'onglet **"Settings"**
3. **Faites défiler** jusqu'à la section **"Domains"** ou **"Networking"**
4. **Cherchez** une URL qui ressemble à : `https://votre-app-production.up.railway.app`
   - Ou dans l'onglet **"Deployments"**, vous verrez peut-être l'URL directement
5. **COPIEZ CETTE URL** (sans le `/api` à la fin)
   - Exemple : Si vous voyez `https://mon-site-production.up.railway.app`, copiez exactement ça

### 6.3 Ajouter la variable BASE_URL

1. **Retournez** dans l'onglet **"Variables"**
2. **Cliquez** sur **"+ New Variable"**
3. **Key** : `BASE_URL`
4. **Value** : Collez l'URL que vous venez de copier (ex: `https://mon-site-production.up.railway.app`)
   - **IMPORTANT** : Pas de `/api` à la fin, juste l'URL de base
5. **Cliquez** sur **"Add"**
6. Railway va redéployer automatiquement

---

## 📋 ÉTAPE 7 : TESTER QUE LE SERVEUR FONCTIONNE

### 7.1 Tester l'endpoint de santé

1. **Ouvrez un nouvel onglet** dans votre navigateur
2. **Tapez** dans la barre d'adresse : `https://VOTRE-URL-RAILWAY/api/health`
   - Remplacez `VOTRE-URL-RAILWAY` par l'URL que vous avez copiée
   - Exemple : `https://mon-site-production.up.railway.app/api/health`
3. **Appuyez** sur Entrée
4. **Vous devriez voir** : `{"status":"ok"}`
5. Si vous voyez ça, **c'est bon signe !** ✅

### 7.2 Vérifier les logs (si problème)

1. **Retournez** sur Railway
2. **Cliquez** sur l'onglet **"Deployments"**
3. **Cliquez** sur le dernier déploiement
4. **Cliquez** sur **"View Logs"** ou **"Logs"**
5. **Vérifiez** qu'il n'y a pas d'erreurs en rouge

---

## 📋 ÉTAPE 8 : METTRE À JOUR LE FRONTEND

### 8.1 Ouvrir les fichiers à modifier

1. **Sur votre ordinateur**, ouvrez le dossier du projet
2. **Ouvrez** le fichier `HTML/auth.html` dans un éditeur de texte
   - Vous pouvez utiliser Visual Studio Code, Notepad++, ou même le Bloc-notes

### 8.2 Modifier auth.html

1. **Cherchez** la ligne qui contient : `const PRODUCTION_API = 'https://VOTRE-APP.railway.app/api';`
   - Utilisez Ctrl+F (ou Cmd+F sur Mac) pour chercher "PRODUCTION_API"
2. **Remplacez** `https://VOTRE-APP.railway.app/api` par votre URL Railway + `/api`
   - Exemple : Si votre URL Railway est `https://mon-site-production.up.railway.app`
   - Remplacez par : `https://mon-site-production.up.railway.app/api`
3. **Sauvegardez** le fichier (Ctrl+S ou Cmd+S)

### 8.3 Modifier profile.html

1. **Ouvrez** le fichier `HTML/profile.html`
2. **Cherchez** la ligne qui contient : `const PRODUCTION_API = 'https://VOTRE-APP.railway.app/api';`
3. **Remplacez** de la même manière que pour auth.html
4. **Sauvegardez** le fichier

### 8.4 Pousser les changements sur GitHub

1. **Ouvrez un terminal** dans le dossier de votre projet
2. **Tapez** ces commandes une par une :

```bash
cd "/Users/thibault/Documents/Projet TALEOS/Antigravity"
git add HTML/auth.html HTML/profile.html
git commit -m "Mise à jour: URL API Railway"
git push origin main
```

3. **Attendez** que les commandes se terminent
4. **Vérifiez** qu'il n'y a pas d'erreur

---

## 📋 ÉTAPE 9 : TESTER L'INSCRIPTION

### 9.1 Aller sur la page d'inscription

1. **Ouvrez votre navigateur**
2. **Allez sur** : https://dedale95.github.io/mon-site/auth.html
3. **Attendez** que la page se charge

### 9.2 Tester l'inscription

1. **Cliquez** sur l'onglet **"Inscription"** (si ce n'est pas déjà sélectionné)
2. **Remplissez** le formulaire :
   - **Email** : Entrez une adresse email valide (vous pouvez utiliser la vôtre)
   - **Mot de passe** : Créez un mot de passe (au moins 8 caractères, avec majuscule, minuscule et chiffre)
   - **Confirmer le mot de passe** : Retapez le même mot de passe
3. **Cliquez** sur **"S'inscrire"**
4. **Attendez** quelques secondes

### 9.3 Vérifier le résultat

**Si ça fonctionne** ✅ :
- Vous verrez un message vert : "Inscription réussie ! Un email de vérification a été envoyé..."
- Vérifiez votre boîte email (y compris les spams)

**Si ça ne fonctionne pas** ❌ :
- Vous verrez un message d'erreur rouge
- **Ouvrez la console du navigateur** (F12, puis onglet "Console")
- **Regardez** les messages d'erreur
- **Vérifiez** dans Railway que le serveur est bien "Active"

---

## 🔍 VÉRIFICATIONS FINALES

### Checklist de vérification

Cochez chaque point au fur et à mesure :

- [ ] Gmail : Validation en 2 étapes activée
- [ ] Gmail : App Password créé et copié
- [ ] Railway : Compte créé et connecté à GitHub
- [ ] Railway : Projet créé depuis le dépôt `mon-site`
- [ ] Railway : Root Directory = `PYTHON`
- [ ] Railway : Start Command = `python auth_server.py`
- [ ] Railway : Variable `SECRET_KEY` ajoutée
- [ ] Railway : Variable `SMTP_SERVER` = `smtp.gmail.com`
- [ ] Railway : Variable `SMTP_PORT` = `587`
- [ ] Railway : Variable `SMTP_USER` = votre email
- [ ] Railway : Variable `SMTP_PASSWORD` = votre app password
- [ ] Railway : Variable `EMAIL_FROM` = votre email
- [ ] Railway : Variable `BASE_URL` = votre URL Railway
- [ ] Railway : Déploiement réussi (statut "Active")
- [ ] Test : `/api/health` retourne `{"status":"ok"}`
- [ ] Frontend : `auth.html` mis à jour avec l'URL Railway
- [ ] Frontend : `profile.html` mis à jour avec l'URL Railway
- [ ] GitHub : Changements poussés sur GitHub
- [ ] Test : Inscription fonctionne sur le site

---

## 🆘 RÉSOLUTION DE PROBLÈMES

### Problème : "Erreur de connexion au serveur"

**Solutions à essayer** :

1. **Vérifiez que Railway est déployé** :
   - Allez sur Railway
   - Vérifiez que le statut est "Active" (pas "Building" ou "Failed")

2. **Vérifiez l'URL dans le code** :
   - Ouvrez `HTML/auth.html`
   - Vérifiez que l'URL dans `PRODUCTION_API` est correcte
   - Elle doit se terminer par `/api`

3. **Testez l'URL directement** :
   - Allez sur `https://VOTRE-URL/api/health`
   - Si ça ne fonctionne pas, le problème vient de Railway

4. **Vérifiez les logs Railway** :
   - Onglet "Deployments" → Cliquez sur le déploiement → "View Logs"
   - Cherchez des erreurs en rouge

### Problème : Les emails ne sont pas envoyés

**Solutions** :

1. **Vérifiez les variables SMTP** dans Railway
2. **Vérifiez que vous utilisez un App Password**, pas votre mot de passe normal
3. **Vérifiez les spams** dans votre boîte email
4. **Regardez les logs Railway** pour voir les erreurs d'envoi d'email

### Problème : Le déploiement échoue sur Railway

**Solutions** :

1. **Vérifiez les logs** dans Railway
2. **Vérifiez** que `requirements_auth.txt` contient bien toutes les dépendances
3. **Vérifiez** que le Root Directory est bien `PYTHON` (en majuscules)
4. **Vérifiez** que le Start Command est bien `python auth_server.py`

---

## 📞 BESOIN D'AIDE ?

Si vous êtes bloqué à une étape :

1. **Relisez** attentivement l'étape en question
2. **Vérifiez** la checklist de vérification
3. **Regardez** les logs Railway pour voir les erreurs
4. **Vérifiez** que tous les noms de variables sont exactement comme indiqué (sensible à la casse)

---

## ✅ FÉLICITATIONS !

Une fois toutes les étapes terminées, votre serveur d'authentification fonctionnera 24/7, même quand votre ordinateur est éteint ! 🎉
