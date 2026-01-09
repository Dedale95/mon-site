# Système d'authentification Taleos

## Installation

1. Installer les dépendances Python :
```bash
pip install -r requirements_auth.txt
```

## Configuration

### Configuration SMTP (pour l'envoi d'emails)

Avant de lancer le serveur, configurez les variables d'environnement pour l'envoi d'emails :

**Pour Gmail :**
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=votre_email@gmail.com
export SMTP_PASSWORD=votre_app_password  # Utilisez un "App Password" Gmail
export EMAIL_FROM=votre_email@gmail.com
export BASE_URL=http://localhost:5000
```

**Note pour Gmail :** Vous devez créer un "App Password" dans votre compte Google :
1. Allez dans votre compte Google → Sécurité
2. Activez la validation en 2 étapes si ce n'est pas déjà fait
3. Créez un "App Password" pour l'application
4. Utilisez ce mot de passe dans `SMTP_PASSWORD`

**Pour d'autres fournisseurs :**
- **Outlook/Hotmail** : `smtp-mail.outlook.com:587`
- **Yahoo** : `smtp.mail.yahoo.com:587`
- **Autre** : Consultez la documentation de votre fournisseur

### Configuration sans SMTP

Si vous ne configurez pas SMTP, le serveur fonctionnera toujours mais :
- Les emails ne seront pas envoyés
- Les tokens de vérification seront affichés dans la console
- Vous devrez copier manuellement le lien de vérification

## Lancement du serveur

```bash
cd PYTHON
python auth_server.py
```

Le serveur sera accessible sur `http://localhost:5000`

## Endpoints API

### POST `/api/signup`
Inscription d'un nouvel utilisateur

**Body :**
```json
{
  "email": "user@example.com",
  "password": "MotDePasse123"
}
```

**Réponse :**
```json
{
  "message": "Inscription réussie. Un email de vérification a été envoyé.",
  "user_id": 1
}
```

### POST `/api/login`
Connexion d'un utilisateur

**Body :**
```json
{
  "email": "user@example.com",
  "password": "MotDePasse123"
}
```

**Réponse :**
```json
{
  "message": "Connexion réussie",
  "token": "jwt_token_here",
  "email": "user@example.com"
}
```

### GET `/api/verify?token=...`
Vérification de l'email avec le token reçu par email

**Réponse :**
```json
{
  "message": "Email vérifié avec succès ! Vous pouvez maintenant vous connecter."
}
```

### GET `/api/health`
Vérification que le serveur fonctionne

## Base de données

La base de données `users.db` est créée automatiquement dans le dossier `PYTHON/`.

Structure :
- `id` : Identifiant unique
- `email` : Adresse email (unique)
- `password_hash` : Hash du mot de passe (SHA-256)
- `email_verified` : 0 ou 1 (email vérifié ou non)
- `verification_token` : Token de vérification
- `verification_token_expires` : Date d'expiration du token (24h)
- `created_at` : Date de création
- `last_login` : Dernière connexion

## Sécurité

- Les mots de passe sont hashés avec SHA-256
- Les tokens de vérification expirent après 24 heures
- Les tokens JWT expirent après 7 jours
- Les mots de passe doivent respecter des critères stricts :
  - Au moins 8 caractères
  - Au moins une majuscule
  - Au moins une minuscule
  - Au moins un chiffre

## Utilisation

1. L'utilisateur s'inscrit sur `/HTML/auth.html`
2. Un email de vérification est envoyé (ou affiché dans la console)
3. L'utilisateur clique sur le lien dans l'email
4. L'email est vérifié
5. L'utilisateur peut se connecter
