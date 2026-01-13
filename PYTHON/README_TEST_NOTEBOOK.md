# Instructions de Test depuis Jupyter Notebook

Ce guide vous explique comment tester le script de connexion bancaire depuis un Jupyter Notebook.

## 📋 Prérequis

1. **Jupyter Notebook installé** :
   ```bash
   pip install jupyter notebook
   ```

2. **Dépendances Python** :
   - Selenium
   - webdriver-manager
   - Chrome installé sur votre système

## 🚀 Démarrage rapide

### Option 1 : Utiliser le notebook fourni

1. **Ouvrir le notebook** :
   ```bash
   cd PYTHON
   jupyter notebook test_connection_notebook.ipynb
   ```

2. **Suivre les cellules dans l'ordre** :
   - Cellule 1 : Installation des dépendances
   - Cellule 2 : Import des modules
   - Cellule 3 : Configuration des identifiants (⚠️ **modifiez vos identifiants ici**)
   - Cellule 4 : Exécution du test
   - Cellule 5 : Affichage des résultats

### Option 2 : Créer votre propre notebook

1. **Créer un nouveau notebook** :
   ```bash
   jupyter notebook
   ```

2. **Copier-coller ce code dans une cellule** :

```python
# Installation des dépendances (si nécessaire)
import sys
!{sys.executable} -m pip install selenium webdriver-manager --quiet

# Import du module
import sys
from pathlib import Path

python_dir = Path.cwd()
if str(python_dir) not in sys.path:
    sys.path.insert(0, str(python_dir))

from test_bank_connection import test_connection_sync

# Configuration
BANK_ID = "credit_agricole"
EMAIL = "votre.email@exemple.com"  # ← MODIFIEZ
PASSWORD = "votre_mot_de_passe"     # ← MODIFIEZ

# Exécution du test
print("🚀 Démarrage du test...")
result = test_connection_sync(BANK_ID, EMAIL, PASSWORD, timeout=30)

# Affichage des résultats
if result['success']:
    print(f"\n✅ SUCCÈS: {result['message']}")
else:
    print(f"\n❌ ÉCHEC: {result['message']}")

if result.get('details'):
    import json
    print(f"\n📋 Détails: {json.dumps(result['details'], indent=2)}")
```

## 🔍 Ce qui va se passer

1. **Un navigateur Chrome s'ouvrira automatiquement** (visible, pas en mode headless)
2. Le script va :
   - Ouvrir une page d'offre d'emploi Crédit Agricole
   - Gérer les cookies
   - Cliquer sur "Je postule"
   - Cliquer sur le lien de connexion
   - Remplir le formulaire avec vos identifiants
   - Vérifier si la connexion a réussi

3. **Vous verrez tout en temps réel** dans le navigateur

## ⚠️ Notes importantes

- **Le navigateur reste visible** : vous pouvez voir toutes les actions
- **Ne fermez pas le navigateur** pendant le test
- **Le test peut prendre 20-30 secondes**
- Si ChromeDriver n'est pas trouvé, `webdriver-manager` le téléchargera automatiquement

## 🐛 Dépannage

### Erreur : "ChromeDriver not found"
```python
# Installer webdriver-manager
!pip install webdriver-manager
```

### Erreur : "Module not found"
```python
# Vérifier que vous êtes dans le bon répertoire
import os
print(os.getcwd())  # Doit être dans le dossier PYTHON
```

### Le navigateur ne s'ouvre pas
- Vérifiez que Chrome est installé
- Vérifiez les permissions système (macOS peut demander l'autorisation)

## 📝 Exemple de sortie

```
🚀 Démarrage du test...
📌 Le navigateur Chrome va s'ouvrir dans quelques secondes...
⏳ Veuillez patienter pendant le test...

============================================================
🔍 Test de connexion pour Crédit Agricole avec votre.email@exemple.com
🌐 Ouverture du navigateur Chrome...
📡 Ouverture de la page d'offre: https://groupecreditagricole.jobs/...
✅ Bannière de cookies refusée
✅ 'Je postule' cliqué
✅ Formulaire soumis
✅ Connexion réussie ! Formulaire de candidature détecté
============================================================

📊 RÉSULTAT DU TEST
============================================================

✅ SUCCÈS !

Connexion réussie ! Votre compte Crédit Agricole est maintenant lié.

📋 Détails:
{
  "url": "https://groupecreditagricole.jobs/...",
  "reason": "application_form_detected"
}
```
