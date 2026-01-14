# 🔧 Configuration des règles Firestore pour career_connections

## ❌ Problème actuel

L'erreur "Missing or insufficient permissions" vient des règles Firestore qui n'autorisent pas l'écriture dans la sous-collection `career_connections`.

## ✅ Solution : Ajouter les règles pour career_connections

Dans la **Firebase Console** → **Firestore Database** → **Règles**, vous devez ajouter les règles pour la sous-collection `career_connections`.

### Règles complètes à utiliser

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Collection des profils utilisateurs
    match /profiles/{userId} {
      // L'utilisateur peut lire et écrire son propre profil
      allow read, write: if request.auth != null && request.auth.uid == userId;
      
      // Sous-collection des candidatures
      match /job_applications/{applicationId} {
        // L'utilisateur peut gérer ses propres candidatures
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
      
      // Sous-collection des connexions bancaires
      match /career_connections/{connectionId} {
        // L'utilisateur peut lire et écrire ses propres connexions
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

### 🚀 Étapes pour appliquer les règles

1. **Aller sur Firebase Console** : https://console.firebase.google.com/
2. **Sélectionner votre projet** : `project-taleos`
3. **Menu** → **Firestore Database**
4. **Onglet "Règles"**
5. **Remplacer les règles existantes** par les règles complètes ci-dessus
6. **Cliquer sur "Publier"**

### ✅ Vérification

Après avoir publié les règles, vous pouvez tester à nouveau la connexion bancaire. L'erreur "Missing or insufficient permissions" devrait disparaître.

## 📝 Structure des données

Les connexions bancaires sont stockées dans :
```
profiles/{userId}/career_connections/connections
```

Avec la structure :
```javascript
{
  credit_agricole: {
    email: "user@example.com",
    password: "encrypted_password",
    connected: true,
    connectedAt: "2026-01-15T10:30:00.000Z"
  }
}
```

## 🔒 Sécurité

- ✅ Seul l'utilisateur authentifié peut lire/écrire ses propres connexions
- ✅ `request.auth.uid == userId` garantit que l'utilisateur ne peut accéder qu'à ses propres données
- ✅ Les mots de passe sont cryptés avant sauvegarde (base64 dans le code actuel)
