# 🔧 Correction Build Command Render

## ❌ Problème

Le build échoue avec :
```
Failed to install browser dependencies
Error: Installation process exited with code: 1
```

Cela vient de `playwright install-deps chromium` qui essaie de passer en root pour installer les dépendances système.

## ✅ Solution

Sur Render, les dépendances système nécessaires pour Playwright/Chromium sont **déjà présentes**, donc `playwright install-deps` n'est **pas nécessaire** et cause des erreurs.

## 📝 Build Command correct

Le build command correct pour Render est :

```bash
pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium
```

**Sans** `playwright install-deps chromium` à la fin.

## 🔄 Mise à jour dans Render

Si vous avez déjà configuré le service dans Render :

1. Aller dans **Settings** → **Build & Deploy**
2. Dans **Build Command**, remplacer par :
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium
   ```
3. **Supprimer** la partie `&& playwright install-deps chromium`
4. Sauvegarder et redéployer

## ✅ Vérification

Après le rebuild, vous devriez voir :
- ✅ Installation des packages Python réussie
- ✅ Installation de Chromium réussie
- ✅ Build successful
