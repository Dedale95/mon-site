# 🚀 GUIDE DE DÉPLOIEMENT DÉTAILLÉ - RENDER.COM (GRATUIT)

Ce guide vous explique **EXACTEMENT** ce que vous devez faire, étape par étape, pour déployer votre serveur d'authentification sur **Render.com** (plan gratuit disponible).

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
   - **Nom** : Tapez "Render Auth Server"
6. **Cliquez** sur **"Générer"**
7. **Google va afficher un mot de passe de 16 caractères** (ex: `abcd efgh ijkl mnop`)
8. **COPIEZ CE MOT DE PASSE** (sans les espaces) - vous en aurez besoin plus tard
   - Exemple : si Google affiche `abcd efgh ijkl mnop`, copiez `abcdefghijklmnop`
9. **IMPORTANT** : Notez ce mot de passe dans un endroit sûr, vous ne pourrez plus le voir après

---

## 📋 ÉTAPE 2 : CRÉER UN COMPTE RENDER

### 2.1 Aller sur Render

1. **Ouvrez votre navigateur**
2. **Allez sur** : https://render.com
3. Vous verrez une page avec un bouton **"Get Started for Free"** ou **"Sign Up"**

### 2.2 S'inscrire avec GitHub

1. **Cliquez** sur **"Get Started for Free"** ou **"Sign Up"**
2. Render va vous proposer plusieurs options de connexion
3. **Cliquez** sur **"Continue with GitHub"** (ou l'icône GitHub)
4. **Autorisez Render** à accéder à votre compte GitHub
   - GitHub va vous demander de confirmer
   - **Cliquez** sur **"Authorize Render"** ou **"Autoriser"**
5. Render va créer votre compte automatiquement
6. **Vérifiez votre email** si Render le demande

---

## 📋 ÉTAPE 3 : CRÉER UN NOUVEAU WEB SERVICE

### 3.1 Accéder au tableau de bord

1. **Une fois connecté**, vous verrez le tableau de bord Render
2. **Cliquez** sur le bouton **"+ New"** (en haut à droite)
3. Un menu déroulant s'affiche

### 3.2 Choisir Web Service

1. Dans le menu, **cliquez** sur **"Web Service"**
2. Render va vous demander de connecter votre dépôt GitHub

### 3.3 Connecter votre dépôt GitHub

1. **Si c'est la première fois**, Render va vous demander d'autoriser l'accès
   - **Cliquez** sur **"Configure account"** ou **"Connect GitHub"**
   - **Autorisez** Render à accéder à vos dépôts
2. **Une liste de vos dépôts GitHub s'affiche**
3. **Cherchez** votre dépôt : `mon-site` (ou `Dedale95/mon-site`)
4. **Cliquez** sur votre dépôt `mon-site`

---

## 📋 ÉTAPE 4 : CONFIGURER LE WEB SERVICE

### 4.1 Remplir les informations de base

Render va vous demander de remplir un formulaire. Voici ce que vous devez mettre :

#### Nom du service
- **Tapez** : `taleos-auth-server` (ou un nom de votre choix)
- Ce nom apparaîtra dans votre URL

#### Environnement
- **Laissez** : `Docker` (par défaut)
- **OU** changez pour `Pip` si vous préférez

#### Région
- **Laissez** : `Frankfurt` (ou choisissez la plus proche de vous)

#### Branche
- **Laissez** : `main` (ou `master` selon votre dépôt)

### 4.2 Configurer le Build Command

1. **Cherchez** le champ **"Build Command"**
2. **Cliquez** dans ce champ
3. **Tapez exactement** : `pip install -r requirements_auth.txt`
   - En minuscules
   - Sans guillemets

### 4.3 Configurer le Start Command

1. **Cherchez** le champ **"Start Command"**
2. **Cliquez** dans ce champ
3. **Tapez exactement** : `python auth_server.py`
   - En minuscules
   - Sans guillemets

### 4.4 Configurer le Root Directory

1. **Cherchez** le champ **"Root Directory"** (peut être dans "Advanced")
2. **Cliquez** dans ce champ
3. **Tapez exactement** : `PYTHON`
   - En majuscules
   - Sans guillemets

### 4.5 Choisir le plan

1. **Cherchez** la section **"Plan"** ou **"Pricing"**
2. **Sélectionnez** : **"Free"** (gratuit)
   - ⚠️ **Note** : Le plan gratuit met le service en veille après 15 minutes d'inactivité
   - Le premier démarrage peut prendre 30-60 secondes
   - C'est normal et gratuit !

---

## 📋 ÉTAPE 5 : CONFIGURER LES VARIABLES D'ENVIRONNEMENT

### 5.1 Accéder aux variables

**AVANT de cliquer sur "Create Web Service"**, cherchez la section **"Environment Variables"** ou **"Advanced"** → **"Environment Variables"**

### 5.2 Ajouter la variable SECRET_KEY

1. **Cliquez** sur **"Add Environment Variable"** ou **"+ Add"**
2. Dans le champ **"Key"** (Clé), **tapez** : `SECRET_KEY`
   - En majuscules
   - Avec un underscore
3. Pour générer une valeur, **ouvrez un terminal** sur votre ordinateur et tapez :
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
4. **Copiez** le résultat (une longue chaîne de caractères)
5. **Collez** cette valeur dans le champ **"Value"** (Valeur)
6. **Cliquez** sur **"Add"** ou laissez tel quel

### 5.3 Ajouter les variables SMTP

**Ajoutez ces variables UNE PAR UNE** en cliquant sur **"Add Environment Variable"** pour chacune :

#### Variable 1 : SMTP_SERVER
- **Key** : `SMTP_SERVER`
- **Value** : `smtp.gmail.com`
- **Cliquez** sur **"Add"** ou passez à la suivante

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

### 5.5 Créer le service

1. **Une fois toutes les variables ajoutées**, **faites défiler** vers le bas
2. **Cherchez** le bouton **"Create Web Service"** (en bas de la page)
3. **Cliquez** sur **"Create Web Service"**
4. Render va commencer à déployer votre service

---

## 📋 ÉTAPE 6 : ATTENDRE LE DÉPLOIEMENT

### 6.1 Vérifier le déploiement

1. **Vous serez redirigé** vers la page de votre service
2. Vous verrez un onglet **"Events"** ou **"Logs"** avec un déploiement en cours
3. **Attendez** que le statut passe à **"Live"** (cela peut prendre 2-5 minutes)
4. Vous verrez des messages dans les logs comme :
   - "Building..."
   - "Starting service..."
   - "Your service is live at..."

### 6.2 Récupérer l'URL de votre application

1. **Une fois le déploiement terminé** (statut "Live")
2. **En haut de la page**, vous verrez une section avec une **URL**
3. L'URL ressemblera à : `https://taleos-auth-server.onrender.com`
   - Le nom peut varier selon ce que vous avez choisi
4. **COPIEZ CETTE URL** (sans le `/api` à la fin)
   - Exemple : Si vous voyez `https://taleos-auth-server.onrender.com`, copiez exactement ça

### 6.3 Ajouter la variable BASE_URL

1. **Dans la page de votre service**, **cliquez** sur l'onglet **"Environment"** (ou cherchez "Environment Variables")
2. **Cliquez** sur **"Add Environment Variable"**
3. **Key** : `BASE_URL`
4. **Value** : Collez l'URL que vous venez de copier (ex: `https://taleos-auth-server.onrender.com`)
   - **IMPORTANT** : Pas de `/api` à la fin, juste l'URL de base
5. **Cliquez** sur **"Save Changes"** ou **"Add"**
6. Render va **redéployer automatiquement** (cela prendra 1-2 minutes)

---

## 📋 ÉTAPE 7 : TESTER QUE LE SERVEUR FONCTIONNE

### 7.1 Tester l'endpoint de santé

1. **Ouvrez un nouvel onglet** dans votre navigateur
2. **Tapez** dans la barre d'adresse : `https://VOTRE-URL-RENDER/api/health`
   - Remplacez `VOTRE-URL-RENDER` par l'URL que vous avez copiée
   - Exemple : `https://taleos-auth-server.onrender.com/api/health`
3. **Appuyez** sur Entrée
4. **La première fois**, cela peut prendre 30-60 secondes (le service se réveille)
5. **Vous devriez voir** : `{"status":"ok"}`
6. Si vous voyez ça, **c'est bon signe !** ✅

### 7.2 Vérifier les logs (si problème)

1. **Retournez** sur Render
2. **Cliquez** sur l'onglet **"Logs"** de votre service
3. **Vérifiez** qu'il n'y a pas d'erreurs en rouge
4. Vous devriez voir des messages comme :
   - "🚀 SERVEUR D'AUTHENTIFICATION TALEOS"
   - "📁 Base de données: ..."
   - "🌐 URL: ..."

---

## 📋 ÉTAPE 8 : METTRE À JOUR LE FRONTEND

### 8.1 Ouvrir les fichiers à modifier

1. **Sur votre ordinateur**, ouvrez le dossier du projet
2. **Ouvrez** le fichier `HTML/auth.html` dans un éditeur de texte
   - Vous pouvez utiliser Visual Studio Code, Notepad++, ou même le Bloc-notes

### 8.2 Modifier auth.html

1. **Cherchez** la ligne qui contient : `const PRODUCTION_API = 'https://VOTRE-APP.railway.app/api';`
   - Utilisez Ctrl+F (ou Cmd+F sur Mac) pour chercher "PRODUCTION_API"
2. **Remplacez** `https://VOTRE-APP.railway.app/api` par votre URL Render + `/api`
   - Exemple : Si votre URL Render est `https://taleos-auth-server.onrender.com`
   - Remplacez par : `https://taleos-auth-server.onrender.com/api`
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
git commit -m "Mise à jour: URL API Render"
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
4. **⚠️ ATTENTION** : La première fois, cela peut prendre 30-60 secondes car Render réveille le service
5. **Attendez** patiemment

### 9.3 Vérifier le résultat

**Si ça fonctionne** ✅ :
- Vous verrez un message vert : "Inscription réussie ! Un email de vérification a été envoyé..."
- Vérifiez votre boîte email (y compris les spams)

**Si ça ne fonctionne pas** ❌ :
- Vous verrez un message d'erreur rouge
- **Ouvrez la console du navigateur** (F12, puis onglet "Console")
- **Regardez** les messages d'erreur
- **Vérifiez** dans Render que le service est bien "Live"

---

## ⚠️ IMPORTANT : PLAN GRATUIT RENDER

### Limitations du plan gratuit :

1. **Mise en veille** : Le service se met en veille après 15 minutes d'inactivité
2. **Démarrage lent** : Le premier démarrage après la veille prend 30-60 secondes
3. **C'est normal** : C'est le prix de la gratuité !

### Solutions :

- **Pour tester** : Attendez simplement 30-60 secondes lors du premier appel
- **Pour la production** : Si vous voulez éviter la mise en veille, vous pouvez :
  - Utiliser un service de "ping" gratuit (comme UptimeRobot) qui appelle votre service toutes les 10 minutes
  - Ou passer au plan payant de Render (7$/mois)

---

## 🔍 VÉRIFICATIONS FINALES

### Checklist de vérification

Cochez chaque point au fur et à mesure :

- [ ] Gmail : Validation en 2 étapes activée
- [ ] Gmail : App Password créé et copié
- [ ] Render : Compte créé et connecté à GitHub
- [ ] Render : Web Service créé depuis le dépôt `mon-site`
- [ ] Render : Root Directory = `PYTHON`
- [ ] Render : Build Command = `pip install -r requirements_auth.txt`
- [ ] Render : Start Command = `python auth_server.py`
- [ ] Render : Plan = Free
- [ ] Render : Variable `SECRET_KEY` ajoutée
- [ ] Render : Variable `SMTP_SERVER` = `smtp.gmail.com`
- [ ] Render : Variable `SMTP_PORT` = `587`
- [ ] Render : Variable `SMTP_USER` = votre email
- [ ] Render : Variable `SMTP_PASSWORD` = votre app password
- [ ] Render : Variable `EMAIL_FROM` = votre email
- [ ] Render : Variable `BASE_URL` = votre URL Render
- [ ] Render : Déploiement réussi (statut "Live")
- [ ] Test : `/api/health` retourne `{"status":"ok"}` (après 30-60s d'attente)
- [ ] Frontend : `auth.html` mis à jour avec l'URL Render
- [ ] Frontend : `profile.html` mis à jour avec l'URL Render
- [ ] GitHub : Changements poussés sur GitHub
- [ ] Test : Inscription fonctionne sur le site (après 30-60s d'attente)

---

## 🆘 RÉSOLUTION DE PROBLÈMES

### Problème : "Erreur de connexion au serveur"

**Solutions à essayer** :

1. **Vérifiez que Render est déployé** :
   - Allez sur Render
   - Vérifiez que le statut est "Live" (pas "Building" ou "Failed")

2. **Attendez 30-60 secondes** :
   - Le service gratuit se met en veille
   - Le premier appel après la veille prend du temps
   - C'est normal !

3. **Vérifiez l'URL dans le code** :
   - Ouvrez `HTML/auth.html`
   - Vérifiez que l'URL dans `PRODUCTION_API` est correcte
   - Elle doit se terminer par `/api`

4. **Testez l'URL directement** :
   - Allez sur `https://VOTRE-URL/api/health`
   - Attendez 30-60 secondes
   - Si ça ne fonctionne pas, le problème vient de Render

5. **Vérifiez les logs Render** :
   - Onglet "Logs" de votre service
   - Cherchez des erreurs en rouge

### Problème : Les emails ne sont pas envoyés

**Solutions** :

1. **Vérifiez les variables SMTP** dans Render
2. **Vérifiez que vous utilisez un App Password**, pas votre mot de passe normal
3. **Vérifiez les spams** dans votre boîte email
4. **Regardez les logs Render** pour voir les erreurs d'envoi d'email

### Problème : Le déploiement échoue sur Render

**Solutions** :

1. **Vérifiez les logs** dans Render (onglet "Logs")
2. **Vérifiez** que `requirements_auth.txt` contient bien toutes les dépendances
3. **Vérifiez** que le Root Directory est bien `PYTHON` (en majuscules)
4. **Vérifiez** que le Build Command est bien `pip install -r requirements_auth.txt`
5. **Vérifiez** que le Start Command est bien `python auth_server.py`

---

## 📞 BESOIN D'AIDE ?

Si vous êtes bloqué à une étape :

1. **Relisez** attentivement l'étape en question
2. **Vérifiez** la checklist de vérification
3. **Regardez** les logs Render pour voir les erreurs
4. **Vérifiez** que tous les noms de variables sont exactement comme indiqué (sensible à la casse)
5. **N'oubliez pas** : Le plan gratuit met le service en veille, attendez 30-60 secondes lors du premier appel

---

## ✅ FÉLICITATIONS !

Une fois toutes les étapes terminées, votre serveur d'authentification fonctionnera 24/7 sur Render (avec une petite mise en veille après 15 minutes d'inactivité, mais c'est gratuit !) 🎉
