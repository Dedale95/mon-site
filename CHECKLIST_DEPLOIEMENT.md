# ✅ CHECKLIST DE DÉPLOIEMENT - RENDER.COM (GRATUIT)

Imprimez cette page ou gardez-la ouverte pendant le déploiement.

---

## 📧 ÉTAPE 1 : PRÉPARER GMAIL

- [ ] Validation en 2 étapes activée sur Gmail
- [ ] App Password créé pour "Mail"
- [ ] App Password copié et noté (16 caractères) : _______________________

---

## 🌐 ÉTAPE 2 : RENDER.COM

- [ ] Compte Render créé (connecté avec GitHub)
- [ ] Nouveau Web Service créé depuis le dépôt `mon-site`
- [ ] Plan Free sélectionné

---

## ⚙️ ÉTAPE 3 : CONFIGURATION DU SERVICE

- [ ] Root Directory = `PYTHON` (dans le formulaire)
- [ ] Build Command = `pip install -r requirements_auth.txt`
- [ ] Start Command = `python auth_server.py`
- [ ] Plan = Free

---

## 🔐 ÉTAPE 4 : VARIABLES D'ENVIRONNEMENT

Ajoutez ces variables dans l'onglet "Variables" de Railway :

- [ ] `SECRET_KEY` = (votre clé générée)
- [ ] `SMTP_SERVER` = `smtp.gmail.com`
- [ ] `SMTP_PORT` = `587`
- [ ] `SMTP_USER` = (votre email Gmail)
- [ ] `SMTP_PASSWORD` = (votre app password)
- [ ] `EMAIL_FROM` = (votre email Gmail)

---

## 🌐 ÉTAPE 5 : DÉPLOIEMENT

- [ ] Déploiement terminé (statut "Live" dans Render)
- [ ] URL Render récupérée : _________________________________________
- [ ] Variable `BASE_URL` ajoutée avec l'URL ci-dessus

---

## 🧪 ÉTAPE 6 : TEST DU SERVEUR

- [ ] Test de `/api/health` réussi (⚠️ attendre 30-60s la première fois)
  - URL testée : https://________________________/api/health
  - Résultat : `{"status":"ok"}` ✅

---

## 💻 ÉTAPE 7 : MISE À JOUR DU FRONTEND

- [ ] Fichier `HTML/auth.html` modifié
  - Ancienne URL : `https://VOTRE-APP.railway.app/api`
  - Nouvelle URL Render : _________________________________________
- [ ] Fichier `HTML/profile.html` modifié
  - Ancienne URL : `https://VOTRE-APP.railway.app/api`
  - Nouvelle URL Render : _________________________________________
- [ ] Changements poussés sur GitHub
  - Commande exécutée : `git add HTML/auth.html HTML/profile.html`
  - Commande exécutée : `git commit -m "Mise à jour: URL API Railway"`
  - Commande exécutée : `git push origin main`

---

## 🎯 ÉTAPE 8 : TEST FINAL

- [ ] Site visité : https://dedale95.github.io/mon-site/auth.html
- [ ] Test d'inscription effectué (⚠️ attendre 30-60s la première fois)
- [ ] Inscription réussie ✅
- [ ] Email de vérification reçu (vérifier les spams aussi)

---

## 📝 NOTES IMPORTANTES

**URL Render** : _________________________________________

**Email utilisé pour SMTP** : _________________________________________

**Date du déploiement** : _________________________________________

**⚠️ RAPPEL** : Le plan gratuit Render met le service en veille après 15 min d'inactivité. Le premier appel prend 30-60 secondes.

---

## 🆘 EN CAS DE PROBLÈME

**Erreur rencontrée** : _________________________________________

**Où** : _________________________________________

**Solution trouvée** : _________________________________________

---

## ✅ DÉPLOIEMENT TERMINÉ !

Une fois toutes les cases cochées, votre serveur fonctionne 24/7 ! 🎉
