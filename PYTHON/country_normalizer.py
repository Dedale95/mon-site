"""
Normalisation des noms de pays
EN → FR pour cohérence
"""

COUNTRY_MAPPING = {
    # Anglais → Français
    'united states': 'États-Unis',
    'united states of america': 'États-Unis',
    'usa': 'États-Unis',
    'united kingdom': 'Royaume-Uni',
    'uk': 'Royaume-Uni',
    'germany': 'Allemagne',
    'spain': 'Espagne',
    'italy': 'Italie',
    'netherlands': 'Pays-Bas',
    'belgium': 'Belgique',
    'switzerland': 'Suisse',
    'austria': 'Autriche',
    'poland': 'Pologne',
    'czech republic': 'République Tchèque',
    'romania': 'Roumanie',
    'hungary': 'Hongrie',
    'portugal': 'Portugal',
    'greece': 'Grèce',
    'denmark': 'Danemark',
    'sweden': 'Suède',
    'norway': 'Norvège',
    'finland': 'Finlande',
    'ireland': 'Irlande',
    'russia': 'Russie',
    'turkey': 'Turquie',
    
    # Asie / Océanie
    'india': 'Inde',
    'china': 'Chine',
    'japan': 'Japon',
    'south korea': 'Corée du Sud',
    'korea': 'Corée du Sud',
    'taiwan': 'Taiwan',
    'singapore': 'Singapour',
    'malaysia': 'Malaisie',
    'vietnam': 'Vietnam',
    'thailand': 'Thaïlande',
    'australia': 'Australie',
    'new zealand': 'Nouvelle-Zélande',
    
    # Afrique / Moyen-Orient
    'morocco': 'Maroc',
    'tunisia': 'Tunisie',
    'algeria': 'Algérie',
    'egypt': 'Égypte',
    'south africa': 'Afrique du Sud',
    'united arab emirates': 'Émirats Arabes Unis',
    'uae': 'Émirats Arabes Unis',
    'dubai': 'Émirats Arabes Unis',
    'qatar': 'Qatar',
    'saudi arabia': 'Arabie Saoudite',
    
    # Amériques
    'brazil': 'Brésil',
    'argentina': 'Argentine',
    'chile': 'Chili',
    'mexico': 'Mexique',
    'colombia': 'Colombie',
    'canada': 'Canada',
    
    # Europe (Français / Stable)
    'france': 'France',
    'luxembourg': 'Luxembourg',
    'monaco': 'Monaco',
    'belgique': 'Belgique',
    'suisse': 'Suisse',
    'italie': 'Italie',
    'espagne': 'Espagne',
    'allemagne': 'Allemagne',
    'hong-kong': 'Hong-Kong',
    'hong kong': 'Hong-Kong',
}

def normalize_country(country_raw):
    """
    Normalise le nom d'un pays en français
    """
    if not country_raw:
        return country_raw
    
    country_clean = country_raw.strip()
    
    # Supprimer le préfixe "- " si présent (ex: "- France" → "France")
    if country_clean.startswith('- '):
        country_clean = country_clean[2:].strip()
    
    country_clean = country_clean.lower()
    
    # Supprimer les codes numériques (ex: "91" qui est un département français)
    if country_clean.isdigit() or (len(country_clean) <= 3 and country_clean.isdigit()):
        return "France"  # Les codes numériques courts sont probablement des départements français
    
    # Supprimer les codes ISO ou régions si présents après une virgule
    if ',' in country_clean:
        country_clean = country_clean.split(',')[-1].strip()
    
    # Normaliser les variantes courantes
    country_variants = {
        'etats-unis': 'États-Unis',
        'etats unis': 'États-Unis',
        'etats-unis d\'amérique': 'États-Unis',
        'etats unis d\'amérique': 'États-Unis',
        'usa': 'États-Unis',
        'u.s.a': 'États-Unis',
        'corée': 'Corée du Sud',
        'corée du sud': 'Corée du Sud',
    }
    
    # Vérifier les variantes d'abord
    if country_clean in country_variants:
        return country_variants[country_clean]
        
    if country_clean in COUNTRY_MAPPING:
        return COUNTRY_MAPPING[country_clean]
    
    # Si pas dans le mapping, mettre la première lettre en majuscule
    result = country_raw.strip()
    if result.startswith('- '):
        result = result[2:].strip()
    result = result.title()
    
    # Harmoniser "France" (toujours retourner "France" sans préfixe)
    if result.lower() == 'france' or result == '- France':
        return 'France'
    
    return result
