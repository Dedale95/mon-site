# Guide de configuration Firebase Firestore pour le stockage des profils utilisateurs

## 📋 Résumé

Firebase Firestore a été intégré pour stocker les profils utilisateurs de manière **sécurisée, gratuite et synchronisée** entre tous les appareils.

### Avantages de Firestore

✅ **Gratuit** jusqu'à 50 000 lectures/jour et 20 000 écritures/jour (Plan Spark)  
✅ **Sécurisé** avec les règles de sécurité Firebase  
✅ **Synchronisé** automatiquement entre tous les appareils  
✅ **Accessible** depuis n'importe quel navigateur/appareil  
✅ **Sauvegarde automatique** dans le cloud Google  
✅ **Déjà intégré** dans votre projet Firebase  

---

## 🔧 Configuration requise

### 1. Activer Firestore dans Firebase Console

1. Allez sur [Firebase Console](https://console.firebase.google.com/)
2. Sélectionnez votre projet `project-taleos`
3. Dans le menu de gauche, cliquez sur **"Firestore Database"**
4. Cliquez sur **"Créer une base de données"**
5. Choisissez **"Démarrer en mode test"** (nous configurerons les règles après)
6. Sélectionnez une **région** (Europe de l'Ouest recommandé pour la France)
7. Cliquez sur **"Activé"**

### 2. Configurer les règles de sécurité Firestore

Dans la Firebase Console, allez dans **Firestore Database > Règles** et collez les règles suivantes :

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Collection des profils utilisateurs
    match /profiles/{userId} {
      // Un utilisateur peut lire son propre profil
      allow read: if request.auth != null && request.auth.uid == userId;
      
      // Un utilisateur peut créer/mettre à jour son propre profil
      allow create: if request.auth != null && request.auth.uid == userId;
      allow update: if request.auth != null && request.auth.uid == userId;
      
      // Un utilisateur peut supprimer son propre profil
      allow delete: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

**Explication des règles :**
- `request.auth != null` : L'utilisateur doit être authentifié
- `request.auth.uid == userId` : L'utilisateur ne peut accéder qu'à son propre profil
- **Sécurité garantie** : Chaque utilisateur ne peut voir/modifier que son propre profil

Cliquez sur **"Publier"** pour activer les règles.

---

## 📊 Structure des données

Les profils sont stockés dans une collection `profiles` avec la structure suivante :

```javascript
profiles/
  {userId}/  // L'ID Firebase Auth de l'utilisateur
    {
      civility: "Monsieur",
      first_name: "Jean",
      last_name: "Dupont",
      phone: "+33123456789",
      address: "123 Rue Example",
      postal_code: "75001",
      city: "Paris",
      country: "France",
      email: "jean.dupont@example.com",
      created_at: "2026-01-15T10:30:00.000Z",
      updated_at: "2026-01-15T14:45:00.000Z"
    }
```

---

## 🔄 Fonctionnement

### Sauvegarde du profil

1. L'utilisateur remplit le formulaire sur `profile.html`
2. Lorsqu'il clique sur **"Enregistrer"** :
   - Les données sont sauvegardées dans **Firestore** (cloud)
   - Les données sont aussi sauvegardées dans **localStorage** (cache local)
3. La sauvegarde dans Firestore est **prioritaire** et sécurisée

### Chargement du profil

1. Lors de la connexion, le système :
   - Essaie de charger depuis **Firestore** (source de vérité)
   - Si Firestore n'est pas disponible, charge depuis **localStorage** (fallback)
   - Synchronise localStorage vers Firestore si possible

### Synchronisation automatique

- Les données sont **automatiquement synchronisées** entre tous les appareils
- Si un utilisateur modifie son profil sur un appareil, il sera disponible sur tous ses autres appareils
- Le cache localStorage permet une utilisation hors-ligne

---

## 💰 Coûts (Plan Spark Gratuit)

| Action | Limite gratuite | Estimation pour 100 utilisateurs |
|--------|----------------|----------------------------------|
| Lectures/jour | 50 000 | ~500 lectures/jour |
| Écritures/jour | 20 000 | ~100 écritures/jour |
| Stockage | 1 GB | ~10 KB par profil = 1 MB pour 100 profils |

**Conclusion** : Le plan gratuit est largement suffisant pour plusieurs milliers d'utilisateurs actifs !

---

## 🔒 Sécurité

### Règles Firestore
- ✅ Chaque utilisateur ne peut accéder qu'à son propre profil
- ✅ Authentification obligatoire (Firebase Auth)
- ✅ Validation des données côté client et serveur

### Données sensibles
Les informations stockées dans le profil (nom, adresse, téléphone) sont :
- **Cryptées en transit** (HTTPS)
- **Cryptées au repos** (Firebase)
- **Accessibles uniquement par l'utilisateur propriétaire**

---

## 🐛 Dépannage

### Erreur "Permission denied"
- Vérifiez que les règles Firestore sont correctement configurées
- Vérifiez que l'utilisateur est bien authentifié avec Firebase Auth

### Les données ne se synchronisent pas
- Vérifiez votre connexion internet
- Vérifiez la console du navigateur (F12) pour les erreurs
- Les données sont sauvegardées localement en fallback

### Firestore n'est pas disponible
- Le système utilise automatiquement localStorage comme fallback
- Les données seront synchronisées vers Firestore lors de la prochaine connexion

---

## ✅ Vérification

Pour vérifier que tout fonctionne :

1. **Connectez-vous** à votre compte
2. **Allez sur "Mon Profil"**
3. **Remplissez le formulaire** et cliquez sur "Enregistrer"
4. **Vérifiez dans Firebase Console** :
   - Firestore Database > Data
   - Vous devriez voir une collection `profiles` avec votre `userId`
5. **Déconnectez-vous et reconnectez-vous** : les données doivent être présentes

---

## 📝 Notes techniques

- **Compatibilité** : Utilise le SDK Firebase compatibilité (`firestore-compat`)
- **Fallback** : localStorage est utilisé si Firestore n'est pas disponible
- **Synchronisation** : Les données localStorage sont synchronisées vers Firestore à chaque chargement
- **Performance** : Les données sont mises en cache localement pour un chargement rapide

---

## 🚀 Prochaines étapes possibles

- Ajouter un upload de CV (Firebase Storage)
- Ajouter des préférences de recherche d'emploi
- Ajouter un historique des candidatures
- Notifications en temps réel lors de modifications

---

**Besoin d'aide ?** Consultez la [documentation Firestore](https://firebase.google.com/docs/firestore)
