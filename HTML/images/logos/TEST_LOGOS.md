# 🔍 Test et Debug des Logos

Ce document explique comment vérifier que les logos fonctionnent correctement.

## 📋 Vérification des noms de fichiers

### Correspondance noms JSON → Fichiers PNG

Voici les correspondances attendues entre les noms d'entreprises dans le JSON et les fichiers PNG :

| Nom dans JSON | Nom de fichier attendu | Variantes acceptées |
|---------------|------------------------|---------------------|
| `Crédit Agricole S.A.` | `credit_agricole.png` | `credit_agricole.png` ✅ |
| `Crédit Agricole CIB` | `credit_agricole.png` ou `credit_agricole_cib.png` | Les deux fonctionnent |
| `Crédit Agricole Assurances` | `credit_agricole.png` ou `credit_agricole_assurances.png` | Les deux fonctionnent |
| `Deloitte` | `deloitte.png` ou `deloitte_france.png` | Les deux fonctionnent ✅ |
| `Société Générale` | `societe_generale.png` | `societe_generale.png` ✅ |
| `CACEIS` | `caceis.png` | `caceis.png` |
| `LCL` | `lcl.png` ou `credit_lyonnais.png` | Les deux fonctionnent |
| `Amundi` | `amundi.png` | `amundi.png` |

## 🧪 Comment tester

### 1. Vérifier les noms normalisés

Ouvrez la console du navigateur (F12) et exécutez :

```javascript
// Tester la normalisation
console.log(getCompanyLogoFileName("Crédit Agricole S.A.")); 
// Devrait afficher: credit_agricole

console.log(getCompanyLogoFileName("Deloitte")); 
// Devrait afficher: deloitte

console.log(getCompanyLogoFileName("Société Générale")); 
// Devrait afficher: societe_generale
```

### 2. Vérifier les variantes générées

```javascript
// Tester les variantes
console.log(getCompanyLogoFileNameVariants("Crédit Agricole S.A.")); 
// Devrait afficher: ['credit_agricole']

console.log(getCompanyLogoFileNameVariants("Deloitte")); 
// Devrait afficher: ['deloitte', 'deloitte_france']

console.log(getCompanyLogoFileNameVariants("Crédit Agricole CIB")); 
// Devrait afficher: ['credit_agricole', 'credit_agricole_cib']
```

### 3. Vérifier les URLs générées

```javascript
// Tester les URLs
console.log(getCompanyLogoUrls("Crédit Agricole S.A.")); 
// Devrait afficher un tableau avec: ['images/logos/credit_agricole.png', ...]

console.log(getCompanyLogoUrls("Deloitte")); 
// Devrait afficher un tableau avec: ['images/logos/deloitte.png', 'images/logos/deloitte_france.png', ...]
```

### 4. Vérifier le chargement des images

Dans la console du navigateur, vérifiez les erreurs 404 :
- Ouvrez l'onglet "Network" (Réseau)
- Filtrez par "img" (images)
- Rechargez la page
- Cherchez les requêtes avec un code 404 (non trouvé)
- Vérifiez le chemin tenté pour chaque logo

### 5. Vérifier visuellement

1. Allez sur la page "Offres"
2. Recherchez les entreprises dont vous avez ajouté les logos
3. Les logos devraient s'afficher automatiquement
4. Si un logo ne s'affiche pas :
   - Vérifiez le nom du fichier (doit correspondre au nom normalisé)
   - Vérifiez que le fichier est bien dans `HTML/images/logos/`
   - Vérifiez que le format est supporté (.png, .jpg, .jpeg, .svg)
   - Ouvrez la console pour voir les erreurs

## 🐛 Problèmes courants

### Le logo ne s'affiche pas

**Causes possibles :**
1. **Nom de fichier incorrect** : Le nom du fichier ne correspond pas au nom normalisé
   - Solution : Vérifiez le nom avec `getCompanyLogoFileName("Nom Entreprise")` dans la console

2. **Chemin incorrect** : Le chemin vers le logo est incorrect
   - Solution : Vérifiez dans la console (Network) le chemin tenté et comparez avec le chemin réel

3. **Format non supporté** : Le format du fichier n'est pas supporté
   - Solution : Utilisez .png, .jpg, .jpeg ou .svg

4. **Fichier manquant** : Le fichier n'est pas dans le bon dossier
   - Solution : Vérifiez que le fichier est bien dans `HTML/images/logos/`

### Le logo s'affiche mais est cassé

**Causes possibles :**
1. **Fichier corrompu** : Le fichier image est corrompu
   - Solution : Ré-exportez le logo depuis un éditeur d'images

2. **Permissions** : Les permissions du fichier sont incorrectes
   - Solution : Vérifiez les permissions du fichier (doit être lisible)

### Le logo s'affiche mais n'est pas le bon

**Causes possibles :**
1. **Nom de fichier ambigu** : Plusieurs entreprises ont le même nom normalisé
   - Solution : Utilisez des variantes spécifiques (ex: `credit_agricole_cib.png` pour CIB)

## 📝 Exemple de test complet

Pour tester tous les logos :

```javascript
// Liste des entreprises avec leurs logos attendus
const testCompanies = [
    { name: "Crédit Agricole S.A.", expected: "credit_agricole.png" },
    { name: "Deloitte", expected: "deloitte.png ou deloitte_france.png" },
    { name: "Société Générale", expected: "societe_generale.png" }
];

// Tester chaque entreprise
testCompanies.forEach(company => {
    const normalized = getCompanyLogoFileName(company.name);
    const variants = getCompanyLogoFileNameVariants(company.name);
    const urls = getCompanyLogoUrls(company.name);
    
    console.log(`\nEntreprise: ${company.name}`);
    console.log(`Normalisé: ${normalized}`);
    console.log(`Variantes: ${variants.join(', ')}`);
    console.log(`URLs générées (premières 3): ${urls.slice(0, 3).join(', ')}`);
});
```

## ✅ Checklist de vérification

Avant de considérer que les logos fonctionnent :

- [ ] Les fichiers PNG sont dans `HTML/images/logos/`
- [ ] Les noms de fichiers correspondent aux noms normalisés (vérifié avec `getCompanyLogoFileName`)
- [ ] Les formats sont supportés (.png, .jpg, .jpeg, .svg)
- [ ] Les fichiers ne sont pas corrompus (ouvrables dans un éditeur d'images)
- [ ] Les permissions sont correctes (fichiers lisibles)
- [ ] Aucune erreur 404 dans la console (onglet Network)
- [ ] Les logos s'affichent visuellement sur la page "Offres"
