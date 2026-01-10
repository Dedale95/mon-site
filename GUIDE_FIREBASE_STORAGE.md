# Guide de configuration Firebase Storage pour l'upload de CV et lettres de motivation

## 📋 Résumé

Firebase Storage a été intégré pour stocker les CV et lettres de motivation des utilisateurs au format PDF de manière **sécurisée, gratuite et accessible**.

### Avantages de Firebase Storage

✅ **Gratuit** jusqu'à 5 GB de stockage et 1 GB de transfert/jour (Plan Spark)  
✅ **Sécurisé** avec les règles de sécurité Firebase  
✅ **Performant** avec CDN global  
✅ **Accessible** depuis n'importe quel appareil  
✅ **Déjà intégré** dans votre projet Firebase  

---

## 🔧 Configuration requise

### 1. Activer Firebase Storage dans Firebase Console

1. Allez sur [Firebase Console](https://console.firebase.google.com/)
2. Sélectionnez votre projet `project-taleos`
3. Dans le menu de gauche, cliquez sur **"Storage"**
4. Cliquez sur **"Commencer"** ou **"Get started"**
5. Choisissez **"Mode test"** (nous configurerons les règles après)
6. Sélectionnez une **région** (Europe de l'Ouest recommandé pour la France)
7. Cliquez sur **"Terminé"**

### 2. Configurer les règles de sécurité Storage

Dans la Firebase Console, allez dans **Storage > Rules** et collez les règles suivantes :

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Fichiers des utilisateurs dans users/{userId}/{filename}
    match /users/{userId}/{fileName} {
      // Un utilisateur peut lire ses propres fichiers
      allow read: if request.auth != null && request.auth.uid == userId;
      
      // Un utilisateur peut créer/mettre à jour ses propres fichiers
      allow write: if request.auth != null && request.auth.uid == userId
        && request.resource.size < 10 * 1024 * 1024  // Max 10MB
        && request.resource.contentType == 'application/pdf';  // Seulement PDF
      
      // Un utilisateur peut supprimer ses propres fichiers
      allow delete: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

**Explication des règles :**
- `request.auth != null` : L'utilisateur doit être authentifié
- `request.auth.uid == userId` : L'utilisateur ne peut accéder qu'à ses propres fichiers
- `request.resource.size < 10 * 1024 * 1024` : Limite de taille à 10MB par fichier
- `request.resource.contentType == 'application/pdf'` : Seulement les fichiers PDF sont autorisés
- **Sécurité garantie** : Chaque utilisateur ne peut voir/modifier/supprimer que ses propres fichiers

Cliquez sur **"Publier"** pour activer les règles.

---

## 📊 Structure des fichiers dans Storage

Les fichiers sont stockés dans Firebase Storage avec la structure suivante :

```
gs://project-taleos.firebasestorage.app/
  users/
    {userId}/  // L'ID Firebase Auth de l'utilisateur
      cv_{userId}_{timestamp}.pdf
      letter_{userId}_{timestamp}.pdf
```

Les métadonnées des fichiers sont stockées dans Firestore :
- `cv_url` : URL de téléchargement du CV
- `cv_filename` : Nom original du fichier CV
- `cv_uploaded_at` : Date d'upload
- `cv_storage_path` : Chemin dans Storage
- `letter_url` : URL de téléchargement de la lettre
- `letter_filename` : Nom original de la lettre
- `letter_uploaded_at` : Date d'upload
- `letter_storage_path` : Chemin dans Storage

---

## 🎨 Interface utilisateur

### Boutons d'upload

- **Style moderne** avec bordure en pointillés et fond gris clair
- **Animation au survol** avec changement de couleur
- **Icônes** : 📄 pour CV, ✉️ pour lettre de motivation
- **Affichage du nom du fichier** après upload
- **Barre de progression** pendant l'upload
- **Bouton de suppression** (×) avec confirmation

### États visuels

1. **État initial** : Bouton avec texte "Télécharger votre CV/Lettre de motivation"
2. **Upload en cours** : Bouton avec spinner et pourcentage de progression
3. **Upload réussi** : Affichage du nom du fichier avec icône de succès
4. **Fichier présent** : Badge avec nom du fichier et bouton de suppression

---

## 💰 Coûts (Plan Spark Gratuit)

| Ressource | Limite gratuite | Estimation pour 100 utilisateurs |
|-----------|----------------|----------------------------------|
| Stockage | 5 GB | ~10 MB par utilisateur (CV + lettre) = 1 GB pour 100 utilisateurs |
| Transfert/jour | 1 GB | ~1 MB par upload/download = 1000 uploads/jour |
| Opérations écriture/jour | 20 000 | ~200 écritures/jour |
| Opérations lecture/jour | 50 000 | ~500 lectures/jour |

**Conclusion** : Le plan gratuit est largement suffisant pour plusieurs milliers d'utilisateurs actifs !

---

## 🔒 Sécurité

### Règles Storage
- ✅ Chaque utilisateur ne peut accéder qu'à ses propres fichiers
- ✅ Authentification obligatoire (Firebase Auth)
- ✅ Validation du format (PDF uniquement)
- ✅ Limite de taille (10MB par fichier)
- ✅ Validation des types MIME

### Données sensibles
Les fichiers PDF (CV et lettres de motivation) sont :
- **Cryptés en transit** (HTTPS)
- **Cryptés au repos** (Firebase Storage)
- **Accessibles uniquement par l'utilisateur propriétaire**
- **Stockés de manière sécurisée** dans des buckets privés

---

## 🐛 Dépannage

### Erreur "Permission denied"
- Vérifiez que les règles Storage sont correctement configurées
- Vérifiez que l'utilisateur est bien authentifié avec Firebase Auth
- Vérifiez que l'ID utilisateur correspond au chemin du fichier

### Erreur "File too large"
- Limite actuelle : 10MB par fichier
- Compressez vos PDF si nécessaire
- Vérifiez la taille du fichier avant upload

### Erreur "Invalid file type"
- Seuls les fichiers PDF sont acceptés
- Vérifiez que le fichier a bien l'extension `.pdf`
- Vérifiez le type MIME du fichier (`application/pdf`)

### Les fichiers ne s'affichent pas après upload
- Vérifiez la console du navigateur (F12) pour les erreurs
- Vérifiez que les URLs sont bien sauvegardées dans Firestore
- Vérifiez que les règles Storage permettent la lecture

---

## ✅ Vérification

Pour vérifier que tout fonctionne :

1. **Connectez-vous** à votre compte
2. **Allez sur "Mon Profil"**
3. **Cliquez sur "Télécharger votre CV"**
4. **Sélectionnez un fichier PDF** (max 10MB)
5. **Vérifiez la progression** de l'upload
6. **Vérifiez dans Firebase Console** :
   - Storage > Files : Vous devriez voir `users/{userId}/cv_{userId}_{timestamp}.pdf`
   - Firestore Database > Data > profiles > {userId} : Vous devriez voir les champs `cv_url`, `cv_filename`, etc.
7. **Vérifiez que le fichier s'affiche** avec son nom et le bouton de suppression
8. **Testez la suppression** du fichier

---

## 📝 Notes techniques

- **Compatibilité** : Utilise le SDK Firebase compatibilité (`storage-compat`)
- **Format** : Seuls les fichiers PDF sont acceptés
- **Taille max** : 10MB par fichier (configurable dans les règles Storage)
- **Structure** : Fichiers organisés par utilisateur dans `users/{userId}/`
- **Métadonnées** : URLs et informations stockées dans Firestore pour accès rapide
- **Performance** : Les fichiers sont servis via CDN global pour un chargement rapide

---

## 🚀 Prochaines étapes possibles

- Prévisualisation des PDF directement dans le navigateur
- Extraction de texte depuis les PDF pour analyse par l'IA
- Versionning des fichiers (garder l'historique des versions)
- Compression automatique des PDF volumineux
- Intégration avec l'IA pour générer des lettres de motivation personnalisées

---

**Besoin d'aide ?** Consultez la [documentation Firebase Storage](https://firebase.google.com/docs/storage)
