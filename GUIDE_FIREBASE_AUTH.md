# 🔥 GUIDE DE CONFIGURATION - FIREBASE AUTHENTICATION

Ce guide vous explique **EXACTEMENT** comment configurer Firebase Authentication pour votre site, étape par étape.

**Avantages de Firebase Authentication** :
- ✅ **100% gratuit** (plan gratuit généreux)
- ✅ **Pas besoin de serveur backend** (fonctionne directement depuis le frontend)
- ✅ **Fonctionne 24/7** sans maintenance
- ✅ **Sécurisé** (géré par Google)
- ✅ **Facile à configurer**

---

## 📋 ÉTAPE 1 : CRÉER UN PROJET FIREBASE

### 1.1 Aller sur Firebase Console

1. **Ouvrez votre navigateur**
2. **Allez sur** : https://console.firebase.google.com
3. **Connectez-vous** avec votre compte Google (le même que Gmail)

### 1.2 Créer un nouveau projet

1. **Cliquez** sur **"Add project"** ou **"Créer un projet"** (bouton en haut)
2. **Étape 1 - Nom du projet** :
   - **Tapez** : `Taleos` (ou un nom de votre choix)
   - **Cliquez** sur **"Continue"** ou **"Continuer"**
3. **Étape 2 - Google Analytics** (optionnel) :
   - Vous pouvez **désactiver** Google Analytics si vous ne voulez pas
   - Ou **l'activer** si vous voulez des statistiques
   - **Cliquez** sur **"Continue"**
4. **Étape 3 - Créer le projet** :
   - **Attendez** quelques secondes que Firebase crée le projet
   - **Cliquez** sur **"Continue"** une fois terminé

---

## 📋 ÉTAPE 2 : AJOUTER UNE APPLICATION WEB

### 2.1 Accéder à la configuration du projet

1. **Une fois le projet créé**, vous serez sur le tableau de bord Firebase
2. **Cherchez** l'icône **"</>"** (code HTML) ou **"Add app"** / **"Ajouter une application"**
3. **Cliquez** sur l'icône **"</>"** pour **"Add Firebase to your web app"**

### 2.2 Enregistrer l'application web

1. **Étape 1 - Nom de l'app** :
   - **Tapez** : `Taleos Web` (ou un nom de votre choix)
   - **Cochez** la case **"Also set up Firebase Hosting"** (optionnel, vous pouvez la décocher)
   - **Cliquez** sur **"Register app"** ou **"Enregistrer l'application"**

2. **Étape 2 - Configuration Firebase** :
   - Firebase va vous afficher un **code de configuration JavaScript**
   - **NE FERMEZ PAS CETTE PAGE** - vous en aurez besoin !
   - Vous verrez quelque chose comme :
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSy...",
     authDomain: "taleos-xxxxx.firebaseapp.com",
     projectId: "taleos-xxxxx",
     storageBucket: "taleos-xxxxx.appspot.com",
     messagingSenderId: "123456789",
     appId: "1:123456789:web:abcdef"
   };
   ```
   - **COPIEZ TOUT CE CODE** (vous en aurez besoin à l'étape suivante)

3. **Cliquez** sur **"Continue to console"** ou **"Continuer vers la console"**

---

## 📋 ÉTAPE 3 : ACTIVER L'AUTHENTIFICATION EMAIL/MOT DE PASSE

### 3.1 Accéder à Authentication

1. **Dans le menu de gauche** de Firebase Console, **cliquez** sur **"Authentication"** ou **"Authentification"**
2. Si c'est la première fois, **cliquez** sur **"Get started"** ou **"Commencer"**

### 3.2 Activer Email/Password

1. **Cliquez** sur l'onglet **"Sign-in method"** ou **"Méthodes de connexion"**
2. **Cherchez** **"Email/Password"** dans la liste
3. **Cliquez** sur **"Email/Password"**
4. **Activez** le premier bouton (Email/Password) :
   - **Cliquez** sur le bouton pour l'activer
   - **Laissez** "Email link (passwordless sign-in)" **désactivé** (optionnel)
5. **Cliquez** sur **"Save"** ou **"Enregistrer"**

### 3.3 Configurer les domaines autorisés (IMPORTANT)

1. **Toujours dans "Sign-in method"**, **faites défiler** vers le bas
2. **Cherchez** la section **"Authorized domains"** ou **"Domaines autorisés"**
3. **Vérifiez** que ces domaines sont présents :
   - `localhost` (pour le développement local)
   - `dedale95.github.io` (pour GitHub Pages)
4. Si `dedale95.github.io` n'est pas présent :
   - **Cliquez** sur **"Add domain"** ou **"Ajouter un domaine"**
   - **Tapez** : `dedale95.github.io`
   - **Cliquez** sur **"Add"** ou **"Ajouter"**

---

## 📋 ÉTAPE 4 : CONFIGURER LE TEMPLATE D'EMAIL

### 4.1 Accéder aux templates d'email

1. **Toujours dans "Authentication"**, **cliquez** sur l'onglet **"Templates"** ou **"Modèles"**
2. Vous verrez plusieurs templates d'email

### 4.2 Personnaliser l'email de vérification (optionnel)

1. **Cliquez** sur **"Email address verification"** ou **"Vérification d'adresse email"**
2. Vous pouvez **personnaliser** :
   - **Subject** (Sujet) : Ex: "Vérifiez votre email pour Taleos"
   - **Message** : Personnalisez le texte si vous voulez
3. **Cliquez** sur **"Save"** ou **"Enregistrer"**

### 4.3 Personnaliser l'email de réinitialisation (optionnel)

1. **Cliquez** sur **"Password reset"** ou **"Réinitialisation du mot de passe"**
2. **Personnalisez** si vous voulez
3. **Cliquez** sur **"Save"**

---

## 📋 ÉTAPE 5 : INTÉGRER FIREBASE DANS VOTRE CODE

### 5.1 Ajouter Firebase SDK dans auth.html

1. **Sur votre ordinateur**, ouvrez le fichier `HTML/auth.html`
2. **Cherchez** la section `<head>` (en haut du fichier)
3. **Ajoutez** ces lignes **AVANT** la balise `</head>` :

```html
<!-- Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>
```

4. **Cherchez** la section `<script>` qui contient `const API_BASE`
5. **Remplacez** tout le code JavaScript d'authentification par le code Firebase (voir étape suivante)

### 5.2 Ajouter la configuration Firebase

1. **Dans le fichier `HTML/auth.html`**, **cherchez** la balise `<script>` dans le `<body>`
2. **Remplacez** le code qui commence par `const API_BASE` par :

```javascript
<script>
    // Configuration Firebase - REMPLACEZ par votre configuration
    const firebaseConfig = {
        apiKey: "VOTRE_API_KEY",
        authDomain: "VOTRE_AUTH_DOMAIN",
        projectId: "VOTRE_PROJECT_ID",
        storageBucket: "VOTRE_STORAGE_BUCKET",
        messagingSenderId: "VOTRE_MESSAGING_SENDER_ID",
        appId: "VOTRE_APP_ID"
    };

    // Initialiser Firebase
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();

    // Remplacer les valeurs ci-dessus par celles de votre projet Firebase
    // (Vous les avez copiées à l'étape 2.2)
</script>
```

3. **Remplacez** `VOTRE_API_KEY`, `VOTRE_AUTH_DOMAIN`, etc. par les vraies valeurs que vous avez copiées à l'étape 2.2

---

## 📋 ÉTAPE 6 : METTRE À JOUR LES FONCTIONS D'AUTHENTIFICATION

Le code JavaScript sera mis à jour automatiquement dans les fichiers HTML. Voici ce qui change :

### Fonctionnalités :
- ✅ **Inscription** : Crée un compte avec email/mot de passe
- ✅ **Connexion** : Connecte l'utilisateur avec email/mot de passe
- ✅ **Vérification d'email** : Envoie automatiquement un email de vérification
- ✅ **Gestion de session** : Maintient la session utilisateur
- ✅ **Déconnexion** : Déconnecte l'utilisateur

---

## 📋 ÉTAPE 7 : TESTER L'AUTHENTIFICATION

### 7.1 Tester l'inscription

1. **Allez sur** : https://dedale95.github.io/mon-site/auth.html
2. **Cliquez** sur l'onglet **"Inscription"**
3. **Remplissez** le formulaire :
   - Email : Votre email
   - Mot de passe : Au moins 6 caractères
   - Confirmer : Le même mot de passe
4. **Cliquez** sur **"S'inscrire"**
5. **Vous devriez voir** : "Inscription réussie ! Un email de vérification a été envoyé..."
6. **Vérifiez votre boîte email** (y compris les spams)
7. **Cliquez** sur le lien dans l'email pour vérifier votre compte

### 7.2 Tester la connexion

1. **Allez sur** la page d'inscription/connexion
2. **Cliquez** sur l'onglet **"Connexion"**
3. **Entrez** votre email et mot de passe
4. **Cliquez** sur **"Se connecter"**
5. **Vous devriez être redirigé** vers la page des offres

---

## 🔍 VÉRIFICATIONS FINALES

### Checklist de vérification

Cochez chaque point au fur et à mesure :

- [ ] Compte Firebase créé
- [ ] Projet Firebase créé (nom : Taleos)
- [ ] Application web enregistrée
- [ ] Configuration Firebase copiée (apiKey, authDomain, etc.)
- [ ] Authentication activé (Email/Password)
- [ ] Domaine `dedale95.github.io` ajouté aux domaines autorisés
- [ ] Code Firebase ajouté dans `auth.html`
- [ ] Configuration Firebase remplie avec vos vraies valeurs
- [ ] Code JavaScript mis à jour (inscription/connexion)
- [ ] Test d'inscription réussi
- [ ] Email de vérification reçu
- [ ] Email vérifié (clic sur le lien)
- [ ] Test de connexion réussi
- [ ] Redirection après connexion fonctionne

---

## 🆘 RÉSOLUTION DE PROBLÈMES

### Problème : "auth/unauthorized-domain"

**Solution** :
- Vérifiez que `dedale95.github.io` est bien dans les domaines autorisés
- Allez dans Firebase Console → Authentication → Sign-in method → Authorized domains
- Ajoutez `dedale95.github.io` si ce n'est pas présent

### Problème : "auth/email-already-in-use"

**Solution** :
- C'est normal si vous essayez de créer un compte avec un email déjà utilisé
- Utilisez "Connexion" au lieu de "Inscription"

### Problème : "auth/weak-password"

**Solution** :
- Le mot de passe doit faire au moins 6 caractères
- Utilisez un mot de passe plus fort

### Problème : L'email de vérification n'arrive pas

**Solutions** :
1. Vérifiez les spams
2. Attendez quelques minutes
3. Vérifiez que l'email est correct
4. Dans Firebase Console → Authentication → Users, vérifiez que l'utilisateur est créé

### Problème : Erreur JavaScript dans la console

**Solutions** :
1. Ouvrez la console (F12)
2. Vérifiez que les scripts Firebase sont bien chargés
3. Vérifiez que la configuration Firebase est correcte
4. Vérifiez qu'il n'y a pas de fautes de frappe dans les valeurs

---

## 📝 NOTES IMPORTANTES

### Limites du plan gratuit Firebase :

- ✅ **10 000 authentifications/mois** (largement suffisant pour commencer)
- ✅ **Illimité** pour les utilisateurs actifs
- ✅ **Gratuit à vie** pour ce volume

### Sécurité :

- Firebase gère automatiquement la sécurité
- Les mots de passe sont hashés et sécurisés
- Les sessions sont gérées automatiquement
- Pas besoin de gérer un serveur backend

---

## ✅ FÉLICITATIONS !

Une fois toutes les étapes terminées, votre authentification fonctionnera 24/7 avec Firebase, sans serveur à maintenir ! 🎉
