# 🛡️ Sécurité Firebase - Guide complet

## ⚠️ Alerte Google Cloud Platform reçue

Vous avez reçu une alerte concernant votre clé API Firebase exposée publiquement sur GitHub. **C'est normal et attendu pour une application web Firebase !**

---

## ✅ Pourquoi c'est normal

### La clé API Firebase Web est PUBLIQUE par conception

Contrairement aux clés API backend, la clé API Firebase pour les applications web **DOIT être publique** car elle est utilisée directement dans le navigateur de l'utilisateur.

**Votre clé actuelle :**
```
AIzaSyAGeNfIevsaNjfbKTYWMaURhJWdfzWMjmc
```

### La sécurité ne repose PAS sur le secret de cette clé

La sécurité Firebase repose sur **3 piliers** :

1. ✅ **Règles de sécurité Firestore** - Contrôlent qui peut lire/écrire quelles données
2. ✅ **Restrictions d'API** - Limitent les domaines autorisés à utiliser la clé
3. ✅ **Authentification Firebase** - Vérifie l'identité des utilisateurs

---

## 🔧 Actions recommandées

### 1. Ajouter des restrictions de domaine (PRIORITAIRE)

Cela empêche quelqu'un d'utiliser votre clé depuis un autre site web.

#### Étapes détaillées :

1. **Allez sur la Console Google Cloud**
   - URL : https://console.cloud.google.com/
   - Projet : **Project Taleos** (project-taleos)

2. **Naviguez vers les identifiants**
   - Menu (☰) → **"APIs et services"** → **"Identifiants"**
   - Trouvez votre clé : `AIzaSyAGeNfIevsaNjfbKTYWMaURhJWdfzWMjmc`
   - Cliquez dessus pour éditer

3. **Ajouter des restrictions de référence HTTP**
   - Section : **"Restrictions relatives aux sites web"**
   - Sélectionnez : **"Références HTTP (sites web)"**
   - Ajoutez les domaines autorisés :

```
https://dedale95.github.io/*
http://localhost:*
http://127.0.0.1:*
file:///*
```

4. **Restreindre les API autorisées**
   - Section : **"Restrictions relatives aux API"**
   - Sélectionnez : **"Restreindre la clé"**
   - Cochez uniquement :
     - ✅ Identity Toolkit API
     - ✅ Cloud Firestore API
     - ❌ Décochez toutes les autres API

5. **Enregistrer** les modifications

---

### 2. Vérifier vos règles de sécurité Firestore

Vos règles actuelles devraient ressembler à ceci :

```javascript
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    
    // Règles pour les profils utilisateurs
    match /profiles/{userId} {
      // L'utilisateur peut lire et écrire son propre profil
      allow read, write: if request.auth != null && request.auth.uid == userId;
      
      // Sous-collection des candidatures
      match /job_applications/{applicationId} {
        // L'utilisateur peut gérer ses propres candidatures
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
    }
    
    // Par défaut, tout est refusé
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

#### Comment vérifier vos règles :

1. **Console Firebase** : https://console.firebase.google.com/
2. Sélectionnez **"Project Taleos"**
3. Menu → **"Firestore Database"**
4. Onglet **"Règles"**
5. Vérifiez que vos règles correspondent au modèle ci-dessus

**Points critiques :**
- ✅ Seul l'utilisateur authentifié peut accéder à ses propres données
- ✅ Vérification `request.auth.uid == userId` sur toutes les opérations
- ✅ Pas de règles `allow read, write: if true` (dangereux !)

---

### 3. Vérifier l'utilisation et la facturation

1. **Console Google Cloud Platform**
2. Menu → **"Facturation"**
3. Vérifiez qu'il n'y a pas d'utilisation anormale

**Limites gratuites Firebase (plan Spark) :**
- Firestore : 50 000 lectures/jour, 20 000 écritures/jour
- Authentication : Illimité
- Hosting : 10 GB/mois

Si vous dépassez, passez au plan **Blaze** (paiement à l'utilisation).

---

## 📊 Surveillance continue

### Dashboard Firebase

Surveillez l'utilisation de votre projet :

1. **Console Firebase** → **"Usage and billing"**
2. Graphiques de l'utilisation Firestore, Auth, etc.
3. Alertes si vous approchez des limites

### Dashboard Google Cloud

1. **Console Google Cloud** → **"APIs et services"** → **"Tableau de bord"**
2. Visualisez les requêtes par API
3. Détectez les pics anormaux

---

## 🚨 Signes d'utilisation abusive

**Surveillez ces indicateurs :**

- ❌ Pics soudains de requêtes Firestore
- ❌ Utilisation depuis des IP/pays inattendus
- ❌ Coûts de facturation anormaux
- ❌ Nouveaux utilisateurs non légitimes dans Firebase Auth

**En cas de problème :**

1. **Régénérez immédiatement la clé API** (voir section suivante)
2. Renforcez les règles de sécurité Firestore
3. Activez reCAPTCHA pour l'inscription
4. Contactez le support Google Cloud

---

## 🔄 Comment régénérer la clé API (si compromission)

**⚠️ À faire UNIQUEMENT en cas de compromission réelle !**

1. **Console Google Cloud** → **"Identifiants"**
2. Trouvez votre clé API
3. Cliquez sur **"Regénérer la clé"**
4. **Notez la nouvelle clé**
5. Mettez à jour tous vos fichiers HTML avec la nouvelle clé :
   - `offres.html`
   - `HTML/offres.html`
   - `profile.html`
   - `HTML/profile.html`
   - `landing_page_finance.html`
   - `HTML/landing_page_finance.html`
   - `filtres.html`
   - `HTML/filtres.html`
   - `auth.html`
   - `HTML/auth.html`
   - `mes-candidatures.html`
   - `HTML/mes-candidatures.html`

6. Commit et push sur GitHub
7. Supprimez l'ancienne clé

---

## 📚 Ressources officielles

- **Firebase Security Rules** : https://firebase.google.com/docs/rules
- **Sécuriser les clés API** : https://cloud.google.com/docs/authentication/api-keys
- **Firebase Best Practices** : https://firebase.google.com/docs/projects/api-keys

---

## ✅ Checklist de sécurité

Assurez-vous d'avoir fait ces actions :

- [ ] Ajouté des restrictions de domaine sur la clé API
- [ ] Restreint les API autorisées (uniquement Identity Toolkit + Firestore)
- [ ] Vérifié les règles de sécurité Firestore
- [ ] Vérifié qu'il n'y a pas d'utilisation anormale
- [ ] Configuré des alertes de facturation
- [ ] Documenté la clé API et les restrictions

---

## 💡 Conclusion

**Votre clé API Firebase DOIT être publique** - c'est le fonctionnement normal d'une application web Firebase.

**La vraie sécurité vient de :**
1. ✅ Restrictions de domaine sur la clé API
2. ✅ Règles de sécurité Firestore strictes
3. ✅ Authentification Firebase correctement configurée

**Tant que ces 3 points sont respectés, votre application est sécurisée !** 🛡️

---

## 🆘 Besoin d'aide ?

- Documentation Firebase : https://firebase.google.com/docs
- Support Google Cloud : https://cloud.google.com/support
- Stack Overflow : https://stackoverflow.com/questions/tagged/firebase

**N'hésitez pas à me contacter si vous avez des questions !** 🚀
