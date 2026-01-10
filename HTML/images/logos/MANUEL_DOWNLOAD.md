# 📥 Téléchargement manuel des logos

Le script automatique ne peut pas se connecter à Clearbit à cause d'un problème réseau. Voici comment télécharger les logos manuellement.

## 🔗 URLs des logos Clearbit

Vous pouvez télécharger les logos directement depuis votre navigateur :

### Logos principaux

1. **Crédit Agricole**
   - URL: https://logo.clearbit.com/credit-agricole.fr
   - Nom de fichier: `credit_agricole.png`
   - Taille recommandée: 128px (ajoutez `?size=128` à l'URL)

2. **Société Générale**
   - URL: https://logo.clearbit.com/societegenerale.com
   - Nom de fichier: `societe_generale.png`

3. **Deloitte**
   - URL: https://logo.clearbit.com/deloitte.com
   - Nom de fichier: `deloitte.png` ou `deloitte_france.png`

4. **CACEIS**
   - URL: https://logo.clearbit.com/caceis.com
   - Nom de fichier: `caceis.png`

5. **LCL**
   - URL: https://logo.clearbit.com/lcl.fr
   - Nom de fichier: `lcl.png`

6. **Amundi**
   - URL: https://logo.clearbit.com/amundi.com
   - Nom de fichier: `amundi.png`

7. **BforBank**
   - URL: https://logo.clearbit.com/bforbank.com
   - Nom de fichier: `bforbank.png`

8. **Indosuez**
   - URL: https://logo.clearbit.com/indosuez.com
   - Nom de fichier: `indosuez.png`

## 📋 Instructions de téléchargement

### Méthode 1 : Depuis le navigateur

1. Ouvrez votre navigateur web
2. Copiez l'URL du logo (ex: `https://logo.clearbit.com/credit-agricole.fr`)
3. Collez l'URL dans la barre d'adresse
4. Faites un clic droit sur l'image qui s'affiche
5. Sélectionnez "Enregistrer l'image sous..."
6. Enregistrez dans `HTML/images/logos/` avec le bon nom (ex: `credit_agricole.png`)

### Méthode 2 : Avec curl (si votre réseau fonctionne)

```bash
cd "/Users/thibault/Documents/Projet TALEOS/Antigravity/HTML/images/logos"

# Télécharger les logos principaux
curl -o credit_agricole.png "https://logo.clearbit.com/credit-agricole.fr?size=128"
curl -o societe_generale.png "https://logo.clearbit.com/societegenerale.com?size=128"
curl -o deloitte.png "https://logo.clearbit.com/deloitte.com?size=128"
curl -o caceis.png "https://logo.clearbit.com/caceis.com?size=128"
curl -o lcl.png "https://logo.clearbit.com/lcl.fr?size=128"
curl -o amundi.png "https://logo.clearbit.com/amundi.com?size=128"
curl -o bforbank.png "https://logo.clearbit.com/bforbank.com?size=128"
curl -o indosuez.png "https://logo.clearbit.com/indosuez.com?size=128"
```

### Méthode 3 : Sources alternatives

Si Clearbit ne fonctionne pas, vous pouvez aussi chercher les logos sur :
- Google Images : Cherchez "[Nom Entreprise] logo png"
- Site officiel de l'entreprise : Souvent dans leur section "Médias" ou "Presse"
- Wikipedia : Les logos des entreprises sont souvent disponibles

## ✅ Vérification

Après téléchargement, vérifiez que les fichiers :
1. Sont dans le dossier `HTML/images/logos/`
2. Ont le bon nom (ex: `credit_agricole.png`, pas `credit-agricole.png`)
3. Sont au format PNG (ou JPG/SVG si supporté)
4. Ont une taille raisonnable (> 1KB, < 1MB)

## 🔧 Résolution du problème réseau

Si le problème persiste avec Clearbit :

1. **Vérifiez votre connexion internet** : Essayez d'ouvrir https://logo.clearbit.com/credit-agricole.fr dans votre navigateur

2. **Vérifiez le DNS** : 
   ```bash
   nslookup logo.clearbit.com
   ```

3. **Vérifiez les paramètres proxy/firewall** : Il est possible qu'un proxy ou firewall bloque l'accès

4. **Essayez un autre DNS** : 
   - Utilisez 8.8.8.8 (Google DNS) ou 1.1.1.1 (Cloudflare DNS)

## 📝 Notes

- Les logos Clearbit sont généralement au format PNG avec fond transparent
- La taille recommandée est 128px pour un bon équilibre qualité/taille
- Si un logo n'existe pas sur Clearbit, utilisez un placeholder avec les initiales (c'est déjà implémenté dans le code)
