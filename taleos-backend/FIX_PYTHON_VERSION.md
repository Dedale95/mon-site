# 🔧 Correction Python 3.13 → Python 3.11

## ❌ Problème

Render utilise Python 3.13.4, mais le package `greenlet` (dépendance) n'est pas compatible avec Python 3.13, ce qui cause l'erreur de build.

## ✅ Solution appliquée

J'ai créé un fichier `.python-version` à la racine du repo avec la valeur `3.11`.

Render détectera automatiquement ce fichier et utilisera Python 3.11 au lieu de Python 3.13.

## 📋 Prochaines étapes

1. **Le fichier `.python-version` a été créé** et poussé sur GitHub
2. **Dans Render Dashboard** :
   - Le service devrait détecter automatiquement Python 3.11 au prochain build
   - OU vous pouvez **manually trigger un rebuild** :
     - Aller dans le service
     - Cliquer sur "Manual Deploy"
     - Sélectionner "Clear build cache & deploy"

## ✅ Vérification

Après le rebuild, vous devriez voir dans les logs :
```
==> Installing Python version 3.11.x...
```

Au lieu de :
```
==> Installing Python version 3.13.4...
```

## 🔄 Alternative : Variable d'environnement

Si le fichier `.python-version` ne fonctionne pas, vous pouvez aussi :

1. Aller dans **Settings** → **Environment**
2. Ajouter une variable :
   - **Key** : `PYTHON_VERSION`
   - **Value** : `3.11.0`
3. Sauvegarder et redéployer
