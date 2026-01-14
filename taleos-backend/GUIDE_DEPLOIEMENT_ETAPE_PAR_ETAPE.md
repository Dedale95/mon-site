# Guide Déploiement Render.com - Étape par Étape

## 📋 Prérequis

✅ Tous les fichiers sont déjà créés et poussés sur GitHub  
✅ Repository: `https://github.com/Dedale95/mon-site.git`  
✅ Dossier backend: `taleos-backend/`

## 🚀 Déploiement sur Render.com

### Étape 1 : Se connecter à Render.com

1. **Aller sur** [https://dashboard.render.com](https://dashboard.render.com)
2. **Se connecter** avec votre compte GitHub (ou créer un compte si nécessaire)
3. Une fois connecté, vous verrez le dashboard Render

---

### Étape 2 : Créer un nouveau Web Service

1. **Cliquer sur le bouton "New +"** (en haut à droite du dashboard)
2. **Sélectionner "Web Service"** dans le menu déroulant

---

### Étape 3 : Connecter le repository GitHub

1. **Dans la section "Connect a repository"**, vous verrez une liste de vos repos GitHub
2. **Chercher et sélectionner** : `Dedale95/mon-site`
3. Si le repo n'apparaît pas :
   - Cliquer sur "Configure account"
   - Autoriser Render à accéder à vos repos GitHub
   - Revenir et sélectionner `mon-site`

---

### Étape 4 : Configurer le service

Une fois le repo sélectionné, Render va afficher un formulaire de configuration :

#### Configuration de base :

1. **Name** : 
   - Laisser par défaut : `mon-site`
   - OU renommer en : `taleos-connection-tester`

2. **Region** :
   - Sélectionner : `Frankfurt` (Europe)
   - OU laisser la région par défaut

3. **Branch** :
   - Laisser : `main` (ou `master` selon votre repo)

4. **Root Directory** : ⚠️ **IMPORTANT**
   - **Entrer** : `taleos-backend`
   - C'est crucial car vos fichiers sont dans ce sous-dossier

5. **Runtime** :
   - Render détectera automatiquement : `Python 3`

6. **Build Command** :
   - Render détectera automatiquement depuis `render.yaml` :
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install chromium
   playwright install-deps chromium
   ```

7. **Start Command** :
   - Render détectera automatiquement depuis `render.yaml` :
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
   ```

8. **Plan** :
   - Sélectionner : **Free** (gratuit)
   - Cela vous donne :
     - 750 heures/mois
     - 512 MB RAM
     - Cold start après inactivité

---

### Étape 5 : Variables d'environnement (optionnel)

Pour l'instant, **aucune variable d'environnement n'est nécessaire**.

Vous pouvez laisser cette section vide.

---

### Étape 6 : Créer le service

1. **Vérifier toutes les configurations** (surtout le Root Directory)
2. **Cliquer sur le bouton "Create Web Service"** (en bas du formulaire)
3. Render va commencer le déploiement

---

### Étape 7 : Attendre le déploiement

1. **Vous verrez l'écran de déploiement** avec les logs en temps réel
2. **Le build prendra 5-10 minutes** car :
   - Installation des dépendances Python
   - Installation de Playwright
   - Installation de Chromium (navigateur)
3. **Vous verrez les logs** :
   ```
   Installing dependencies...
   Installing Playwright...
   Installing Chromium...
   Starting service...
   ```

4. **Une fois terminé**, vous verrez :
   ```
   ✅ Build successful
   ✅ Service is live
   ```

---

### Étape 8 : Récupérer l'URL du service

Une fois le déploiement réussi :

1. **En haut de la page**, vous verrez l'URL du service :
   ```
   https://mon-site-XXXX.onrender.com
   ```
   ou
   ```
   https://taleos-connection-tester-XXXX.onrender.com
   ```
   (selon le nom que vous avez choisi)

2. **Copier cette URL**

---

### Étape 9 : Tester le service

1. **Ouvrir un nouvel onglet** dans votre navigateur
2. **Aller sur** : `https://VOTRE-URL.onrender.com/health`
3. **Vous devriez voir** :
   ```json
   {
     "status": "ok",
     "message": "Taleos Connection Tester API is running"
   }
   ```

✅ **Le service fonctionne !**

---

### Étape 10 : Mettre à jour connexions.html

1. **Ouvrir** `HTML/connexions.html` dans votre éditeur
2. **Trouver la ligne** (vers la ligne ~550) :
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' 
       ? 'http://localhost:5000/api'
       : 'https://taleos-connection-tester.onrender.com/api';
   ```

3. **Remplacer** `taleos-connection-tester.onrender.com` par votre URL réelle :
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' 
       ? 'http://localhost:5000/api'
       : 'https://VOTRE-URL.onrender.com/api';
   ```

4. **Sauvegarder** le fichier
5. **Commit et push** :
   ```bash
   git add HTML/connexions.html
   git commit -m "Mise à jour URL backend Render"
   git push
   ```

---

## 🧪 Tester la connexion bancaire

1. **Aller sur votre site** : `connexions.html`
2. **Se connecter** avec votre compte Firebase
3. **Cliquer sur une banque** (ex: Crédit Agricole)
4. **Entrer vos identifiants** de test
5. **Cliquer sur "Lier mon compte"**
6. **Attendre 20-30 secondes** (cold start la première fois)
7. **Voir le résultat** ✅ ou ❌

---

## 📝 Vérifications importantes

### ✅ Vérifier que le Root Directory est correct

Dans le dashboard Render → votre service → Settings → **Root Directory** doit être :
```
taleos-backend
```

### ✅ Vérifier les logs

Dans le dashboard Render → votre service → **Logs** :
- Vous devriez voir les logs de Flask/Gunicorn
- Pas d'erreurs critiques

### ✅ Vérifier que le service répond

Tester avec curl ou dans le navigateur :
```bash
curl https://VOTRE-URL.onrender.com/health
```

---

## 🐛 Dépannage

### Le build échoue

1. **Vérifier les logs** dans Render Dashboard
2. **Vérifier que** `requirements.txt` est correct
3. **Vérifier que** Playwright s'installe correctement
4. **Vérifier que** le Root Directory est `taleos-backend`

### Le service ne démarre pas

1. **Vérifier les logs de démarrage**
2. **Vérifier que** Gunicorn est dans `requirements.txt`
3. **Vérifier que** le Start Command est correct

### Timeout des requêtes

1. **Augmenter le timeout** dans `render.yaml` (max 120s)
2. **Vérifier que** le script n'est pas trop long

### Cold start trop long

- **Normal** : 20-30 secondes après 15 minutes d'inactivité
- **Les requêtes suivantes** sont rapides (2-5 secondes)

---

## 📚 Ressources

- **Dashboard Render** : https://dashboard.render.com
- **Documentation Render** : https://render.com/docs
- **Logs du service** : Dashboard → votre service → Logs
- **Settings du service** : Dashboard → votre service → Settings

---

## ✅ Checklist finale

- [ ] Service créé sur Render.com
- [ ] Build réussi (pas d'erreurs)
- [ ] Service est "live" (status vert)
- [ ] URL récupérée et notée
- [ ] Test /health réussi
- [ ] connexions.html mis à jour avec la bonne URL
- [ ] Test de connexion bancaire fonctionne

---

**🎉 Félicitations ! Votre backend est déployé !**
