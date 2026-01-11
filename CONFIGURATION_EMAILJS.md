# 📧 Configuration EmailJS pour le Support

Ce guide explique comment configurer **EmailJS** pour que le formulaire de support envoie des emails directement depuis le site web, sans ouvrir le client mail de l'utilisateur.

---

## 🎯 Pourquoi EmailJS ?

- ✅ **100% gratuit** jusqu'à 200 emails/mois
- ✅ **Sans backend** - fonctionne directement depuis le navigateur
- ✅ **Sécurisé** - pas besoin d'exposer votre mot de passe email
- ✅ **Simple** - configuration en 10 minutes

---

## 📝 Étape 1 : Créer un compte EmailJS

1. Allez sur [https://www.emailjs.com/](https://www.emailjs.com/)
2. Cliquez sur **"Sign Up"** (Inscription)
3. Créez un compte gratuit avec votre email
4. Confirmez votre email

---

## ⚙️ Étape 2 : Configurer un service email

### Option A : Utiliser Gmail (recommandé)

1. Dans le dashboard EmailJS, cliquez sur **"Email Services"**
2. Cliquez sur **"Add New Service"**
3. Sélectionnez **"Gmail"**
4. Cliquez sur **"Connect Account"**
5. Autorisez EmailJS à accéder à votre compte Gmail
6. **Notez le Service ID** (ex: `service_xxxxxxx`)

### Option B : Utiliser Outlook/Hotmail

1. Sélectionnez **"Outlook"** au lieu de Gmail
2. Entrez votre email Outlook : `thibault.giraudet@outlook.com`
3. Créez un **mot de passe d'application** :
   - Allez sur https://account.microsoft.com/security
   - Sécurité > Options de sécurité avancées
   - Créer un nouveau mot de passe d'application
4. Entrez ce mot de passe dans EmailJS
5. **Notez le Service ID**

---

## 📄 Étape 3 : Créer un template d'email

1. Dans le dashboard, cliquez sur **"Email Templates"**
2. Cliquez sur **"Create New Template"**
3. Configurez le template comme suit :

### Template Settings (Paramètres)

**Template Name:** `Support Taleos`  
**Template ID:** `template_support` *(notez-le !)*

### Template Content (Contenu)

**Subject (Sujet):**
```
[Taleos Support] {{subject}}
```

**Content (Corps du message):**
```
Nouveau message de support Taleos
=================================

Type de demande: {{support_type}}

Email de l'expéditeur: {{from_email}}

Sujet: {{subject}}

Message:
--------
{{message}}

---
Message envoyé depuis https://dedale95.github.io/mon-site/
```

**From Name:** `Taleos Support`  
**From Email:** `noreply@taleos.com` *(ou votre email)*  
**To Email:** `{{to_email}}`  
**Reply To:** `{{from_email}}`

4. Cliquez sur **"Save"** (Enregistrer)
5. Testez le template en cliquant sur **"Test It"**

---

## 🔑 Étape 4 : Récupérer votre Public Key

1. Dans le dashboard, cliquez sur **"Account"** (en haut à droite)
2. Allez dans l'onglet **"General"**
3. Copiez votre **Public Key** (ex: `vKq9xxxxxxxxxxx`)

---

## 💻 Étape 5 : Configurer le code

Maintenant, modifiez les fichiers suivants en remplaçant les valeurs :

### Fichiers à modifier :
- `/offres.html`
- `/HTML/offres.html`
- `/filtres.html`
- `/HTML/filtres.html`

### Dans chaque fichier, trouvez ces lignes :

```javascript
// EmailJS Configuration - À configurer sur https://www.emailjs.com/
const EMAILJS_SERVICE_ID = 'service_taleos';  // Remplacer par votre Service ID
const EMAILJS_TEMPLATE_ID = 'template_support'; // Remplacer par votre Template ID
const EMAILJS_PUBLIC_KEY = 'VOTRE_PUBLIC_KEY';  // Remplacer par votre Public Key
```

### Remplacez par vos vraies valeurs :

**Exemple :**
```javascript
const EMAILJS_SERVICE_ID = 'service_abc123xyz';  // Votre Service ID
const EMAILJS_TEMPLATE_ID = 'template_support';   // Votre Template ID
const EMAILJS_PUBLIC_KEY = 'vKq9xxxxxxxxxxx';     // Votre Public Key
```

---

## 🧪 Étape 6 : Tester

1. Sauvegardez tous les fichiers modifiés
2. Commitez et poussez sur GitHub :
   ```bash
   git add .
   git commit -m "Configure EmailJS for support form"
   git push
   ```
3. Attendez 1-2 minutes que GitHub Pages se mette à jour
4. Allez sur votre site : https://dedale95.github.io/mon-site/offres.html
5. Cliquez sur le bouton **"💬 Support"**
6. Remplissez le formulaire et envoyez
7. Vérifiez votre boîte mail !

---

## ✅ Vérifications

### Si ça ne fonctionne pas :

1. **Vérifiez la console du navigateur (F12)** pour voir les erreurs
2. **Vérifiez que les 3 IDs sont corrects** (Service ID, Template ID, Public Key)
3. **Vérifiez que le service email est bien connecté** dans EmailJS
4. **Testez le template** depuis le dashboard EmailJS
5. **Vérifiez votre quota** (200 emails/mois max en gratuit)

### Messages d'erreur courants :

- **"Invalid Public Key"** → Votre Public Key est incorrect
- **"Service not found"** → Votre Service ID est incorrect
- **"Template not found"** → Votre Template ID est incorrect
- **"Quota exceeded"** → Vous avez dépassé les 200 emails/mois

---

## 📊 Dashboard EmailJS

Une fois configuré, vous pourrez :
- ✅ Voir tous les emails envoyés
- ✅ Suivre le taux de succès/échec
- ✅ Voir votre quota restant
- ✅ Gérer plusieurs templates

---

## 🆓 Limites du plan gratuit

- **200 emails par mois**
- **50 Ko par email maximum**
- **Support par email uniquement**

Si vous dépassez 200 emails/mois, vous pouvez upgrader vers un plan payant (à partir de 7$/mois pour 1000 emails).

---

## 🎉 C'est tout !

Votre formulaire de support est maintenant opérationnel ! Les emails seront envoyés directement sans ouvrir le client mail de l'utilisateur.

**Avantages pour l'utilisateur :**
- ✅ Pas besoin d'avoir un client mail configuré
- ✅ Envoi instantané
- ✅ Confirmation visuelle avec toast/alert
- ✅ Pas de redirection vers une autre application

---

## 🆘 Support

Si vous avez des questions sur EmailJS :
- Documentation : https://www.emailjs.com/docs/
- Support : https://www.emailjs.com/support/

Pour les problèmes de configuration Taleos, contactez-moi ! 🚀
