# 🔧 Correction du problème de build Render

## ❌ Problème

Render essaie d'exécuter `render.yaml` comme une commande, ce qui signifie qu'il ne détecte pas correctement le fichier quand il est dans un sous-dossier.

## ✅ Solution : Configuration manuelle (Recommandé pour service gratuit)

Pour un service gratuit avec un sous-dossier, il est **plus simple de configurer manuellement** dans l'interface web de Render.

### Configuration manuelle dans Render.com

Lors de la création du service dans l'interface web, configurez manuellement :

1. **Root Directory** : `taleos-backend`

2. **Build Command** :
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium
   ```
   
   **Note** : `playwright install-deps chromium` n'est pas nécessaire sur Render car les dépendances système sont déjà présentes.

3. **Start Command** :
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
   ```

4. **Plan** : `Free`

5. **Region** : `Frankfurt` (ou autre)

### Alternative : render.yaml à la racine (si vous voulez utiliser render.yaml)

Si vous voulez vraiment utiliser `render.yaml`, vous pouvez le déplacer à la racine du repo, mais cela nécessite de modifier la structure du projet.

## 🚀 Étapes de déploiement (Configuration manuelle)

1. Aller sur https://dashboard.render.com
2. Cliquer sur "New +" → "Web Service"
3. Connecter le repo GitHub : `Dedale95/mon-site`
4. **Ne pas utiliser render.yaml** - Configurer manuellement :
   - **Root Directory** : `taleos-backend` ⚠️ IMPORTANT
   - **Build Command** : (copier-coller la commande ci-dessus)
   - **Start Command** : (copier-coller la commande ci-dessus)
   - **Plan** : `Free`
5. Cliquer sur "Create Web Service"
