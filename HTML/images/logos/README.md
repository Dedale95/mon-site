# 📁 Dossier Logos d'Entreprises

Ce dossier contient les logos des entreprises affichées dans l'onglet "Offres".

## 📋 Comment ajouter un logo

### 1. Nommer le fichier

Le nom du fichier doit correspondre au nom normalisé de l'entreprise. Le système génère automatiquement le nom de fichier à partir du nom de l'entreprise affiché.

**Exemples :**
- Nom entreprise : `Crédit Agricole` → Nom fichier : `credit_agricole.png`
- Nom entreprise : `Société Générale` → Nom fichier : `societe_generale.png`
- Nom entreprise : `Deloitte France` → Nom fichier : `deloitte_france.png`

### 2. Format des fichiers

**Formats acceptés :**
- `.png` (recommandé - meilleure qualité avec transparence)
- `.jpg` / `.jpeg` (si pas de transparence nécessaire)
- `.svg` (recommandé pour les logos vectoriels)

**Taille recommandée :**
- Largeur : 200-400px
- Hauteur : 200-400px
- Ratio : 1:1 (carré) de préférence

### 3. Processus de normalisation

Le système normalise automatiquement le nom de l'entreprise :
- Suppression des accents (é → e, à → a, etc.)
- Remplacement des espaces par des underscores (_)
- Suppression des caractères spéciaux
- Suppression des préfixes juridiques (SA, SAS, SARL, etc.)
- Conversion en minuscules

**Exemples de normalisation :**
- `Crédit Agricole SA` → `credit_agricole.png`
- `BNP Paribas` → `bnp_paribas.png`
- `KPMG France` → `kpmg_france.png`

### 4. Ordre de chargement des logos

Le système essaie de charger les logos dans l'ordre suivant :

1. **Logo local** (ce dossier) :
   - `{nom_normalisé}.png`
   - `{nom_normalisé}.jpg`
   - `{nom_normalisé}.jpeg`
   - `{nom_normalisé}.svg`

2. **Clearbit Logo API** (fallback automatique) :
   - Si aucun logo local n'est trouvé, le système essaie de récupérer le logo depuis Clearbit

3. **Placeholder avec initiales** (fallback final) :
   - Si aucun logo n'est trouvé, un placeholder avec les initiales de l'entreprise s'affiche

### 5. Exemples de noms de fichiers

Pour les entreprises suivantes, utilisez ces noms de fichiers :

| Nom de l'entreprise | Nom du fichier |
|---------------------|----------------|
| Crédit Agricole | `credit_agricole.png` |
| Société Générale | `societe_generale.png` |
| Deloitte | `deloitte.png` |
| BNP Paribas | `bnp_paribas.png` |
| AXA | `axa.png` |
| KPMG | `kpmg.png` |
| EY (Ernst & Young) | `ey.png` ou `ernst_young.png` |
| PWC | `pwc.png` |
| LCL | `lcl.png` |
| Natixis | `natixis.png` |

### 6. Comment trouver le nom exact d'une entreprise

Pour trouver le nom exact utilisé dans le système :

1. Allez sur la page "Offres"
2. Faites un clic droit sur le placeholder du logo d'une entreprise
3. Inspectez l'élément (F12)
4. Regardez l'attribut `data-sources` de l'image
5. Le premier chemin vous indique le nom de fichier attendu

**Exemple :** Si vous voyez `images/logos/credit_agricole.png`, le fichier doit s'appeler `credit_agricole.png`

### 7. Vérifier qu'un logo fonctionne

Après avoir ajouté un logo :

1. Rechargez la page "Offres"
2. Le logo devrait s'afficher automatiquement
3. Si le logo ne s'affiche pas, vérifiez :
   - Le nom du fichier est correct (voir section 1)
   - Le format est supporté (.png, .jpg, .svg)
   - Le fichier est bien dans le dossier `HTML/images/logos/`
   - Les permissions du fichier sont correctes

### 8. Optimisation des logos

**Bonnes pratiques :**
- Utilisez des logos avec fond transparent (.png ou .svg)
- Optimisez la taille des fichiers (max 50KB recommandé)
- Utilisez des logos carrés (ratio 1:1) pour un meilleur rendu
- Vérifiez que le logo est lisible à petite taille (40x40px)

**Outils recommandés pour optimiser :**
- [TinyPNG](https://tinypng.com/) pour compresser les PNG
- [Squoosh](https://squoosh.app/) pour optimiser les images
- [SVGOMG](https://jakearchibald.github.io/svgomg/) pour optimiser les SVG

### 9. Structure du dossier

```
HTML/
  images/
    logos/
      credit_agricole.png
      societe_generale.png
      deloitte.png
      bnp_paribas.png
      ...
      README.md (ce fichier)
```

### 10. Support

Si vous avez des questions ou besoin d'aide :
- Vérifiez la console du navigateur (F12) pour les erreurs
- Assurez-vous que le nom du fichier correspond exactement au nom normalisé
- Vérifiez que le fichier n'est pas corrompu

---

**Note :** Le système essaie automatiquement plusieurs formats (.png, .jpg, .jpeg, .svg) dans l'ordre. Vous n'avez pas besoin de spécifier l'extension dans le nom, le système la détectera automatiquement.
