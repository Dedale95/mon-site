# 🔧 Correction du problème Python 3.13

## ❌ Problème

Render utilise Python 3.13.4 au lieu de Python 3.11.0, et le package `greenlet` (dépendance) n'est pas compatible avec Python 3.13.

## ✅ Solution : Forcer Python 3.11 dans Render

### Méthode 1 : Dans l'interface web Render (Recommandé)

Dans les **Settings** de votre service sur Render :

1. Aller dans **Settings** → **Environment**
2. Ajouter une **Environment Variable** :
   - **Key** : `PYTHON_VERSION`
   - **Value** : `3.11.0`
3. Sauvegarder et redéployer

### Méthode 2 : Utiliser .python-version

Le fichier `runtime.txt` devrait fonctionner, mais Render l'ignore parfois. Vous pouvez aussi créer un fichier `.python-version` à la racine du projet (mais il doit être à la racine du repo, pas dans taleos-backend).

### Méthode 3 : Spécifier dans le Build Command

Dans les **Settings** → **Build & Deploy** → **Build Command**, utiliser :

```bash
python3.11 -m pip install --upgrade pip && python3.11 -m pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
```

Mais cela nécessite que Python 3.11 soit installé, ce qui n'est pas garanti.

## 💡 Solution recommandée : Variable d'environnement

La meilleure solution est d'ajouter une variable d'environnement `PYTHON_VERSION=3.11.0` dans les Settings Render.
