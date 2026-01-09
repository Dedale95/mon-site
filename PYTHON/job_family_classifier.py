"""
Classifier les offres d'emploi par famille de métier
basé sur les titres et descriptions
Harmonisé avec les catégories Crédit Agricole
"""
import re

# Familles de métiers (harmonisées avec CA)
JOB_FAMILIES = {
    "IT, Digital et Data": [
        r'\bdata\b', r'\bIT\b', r'\bdigital\b', r'\bengineer\b', r'\bdeveloper\b',
        r'\bdevops\b', r'\bsoftware\b', r'\bprogramm', r'\bcyber\b', r'\bcloud\b',
        r'\binfra', r'\bsystem', r'\bnetwork\b', r'\bjava\b', r'\bpython\b',
        r'\b\.net\b', r'\bfullstack\b', r'\bfull stack\b', r'\bbackend\b',
        r'\bfrontend\b', r'\bfront-end\b', r'\bback-end\b', r'\bsql\b',
        r'\bdatabase\b', r'\bteradata\b', r'\bpostgres\b', r'\bmongodb\b',
        r'\boracle\b', r'\barchitecte technique\b', r'\bscrum\b', r'\bagile\b',
        r'\btechnical lead\b', r'\btech lead\b', r'\bdevops\b', r'\bsite reliability\b',
        r'\bmachine learning\b', r'\bartificial intelligence\b', r'\bIA\b',
        r'\bdata scien', r'\bdata engineer\b', r'\bdata analyst\b', r'\bbigdata\b',
        r'\banalyst.*data\b', r'\bBI\b', r'\bbusiness intelligence\b',
        r'\bapplicat(if|ion)\b', r'\bsupport.*applicat\b', r'\bQA\b',
        r'\btest', r'\bqualité.*logiciel\b', r'\binformatique\b',
    ],
    
    "Commercial / Relations Clients": [
        r'\bconseiller.*clientèle\b', r'\bconseiller.*client\b', r'\bchargé.*clientèle\b',
        r'\brelation.*client\b', r'\bclient.*relation\b', r'\bcommercial\b',
        r'\bvente\b', r'\bsales\b', r'\bbanquier\b', r'\bgestionnaire.*patrimoine\b',
        r'\bpatrimonial\b', r'\bagent.*commercial\b', r'\bdirecteur.*agence\b',
        r'\bresponsable.*agence\b', r'\badjoint.*agence\b', r'\bagence\b',
        r'\bconseiller.*particulier\b', r'\bconseiller.*professionnel\b',
        r'\bconseiller.*essentiel\b', r'\bconseiller.*premium\b', r'\bconseiller.*privé\b',
        r'\bprivate bank', r'\bcoverage\b', r'\brelationship manager\b',
        r'\baccount manager\b', r'\bclient.*advisor\b', r'\bcustomer.*advisor\b',
    ],
    
    "Financement et Investissement": [
        r'\bfinance\b', r'\bfinancing\b', r'\binvestment\b', r'\binvestissement\b',
        r'\bM&A\b', r'\bfusions.*acquisitions\b', r'\bcorporate.*finance\b',
        r'\bproject.*finance\b', r'\bstructur.*finance\b', r'\btrade.*finance\b',
        r'\bcrédit\b', r'\bcredit\b', r'\bprêt\b', r'\bloan\b', r'\bleasing\b',
        r'\bfactoring\b', r'\banalyste.*crédit\b', r'\bcredit.*analyst\b',
        r'\bchargé.*crédit\b', r'\bcredit.*officer\b', r'\bfinancement\b',
        r'\bequity\b', r'\bdebt\b', r'\bcapital.*markets\b', r'\bmarkets\b',
        r'\btrading\b', r'\btrader\b', r'\bquant\b', r'\bstructuration\b',
        r'\bproduit.*financier\b', r'\bfinancial.*product\b',
    ],
    
    "Risques / Contrôles permanents": [
        r'\brisque\b', r'\brisk\b', r'\bERM\b', r'\bcontrôle.*risque\b',
        r'\brisk.*control\b', r'\brisk.*manage', r'\bmodel.*risk\b',
        r'\bcredit.*risk\b', r'\bmarket.*risk\b', r'\boperational.*risk\b',
        r'\brisque.*opérationnel\b', r'\brisque.*crédit\b', r'\brisque.*marché\b',
        r'\bcontrôle.*permanent\b', r'\bpermanent.*control\b', r'\binternal.*control\b',
        r'\bcontrôle.*interne\b', r'\bvalidation.*modèle\b', r'\bmodel.*validation\b',
    ],
    
    "Conformité / Sécurité financière": [
        r'\bconformité\b', r'\bcompliance\b', r'\bKYC\b', r'\bAML\b', r'\bAMLO\b',
        r'\banti.*money.*launder\b', r'\banti.*blanch', r'\bLCB-FT\b',
        r'\bsécurité.*financière\b', r'\bfinancial.*security\b', r'\bfraud\b',
        r'\bfraude\b', r'\bréglement', r'\bregulat', r'\bréglementaire\b',
    ],
    
    "Finances / Comptabilité / Contrôle de gestion": [
        r'\bcomptab', r'\baccounting\b', r'\bcomptable\b', r'\baccountant\b',
        r'\bcontrôle.*gestion\b', r'\bmanagement.*control\b', r'\bcontrol.*gestion\b',
        r'\bfinancial.*control\b', r'\bcontrôleur.*gestion\b', r'\bcontroller\b',
        r'\bbudget\b', r'\bconsolidation\b', r'\breporting.*financier\b',
        r'\bfinancial.*reporting\b', r'\bFP&A\b', r'\btrésor', r'\btreasur',
        r'\bcash.*management\b', r'\bback.*office.*comptab\b',
    ],
    
    "Gestion des opérations": [
        r'\bopérations\b', r'\boperations\b', r'\bback.*office\b', r'\bmiddle.*office\b',
        r'\bpost.*trade\b', r'\bsettlement\b', r'\bclearing\b', r'\bcustody\b',
        r'\breconciliation\b', r'\brapprochement\b', r'\bprocessing\b',
        r'\btraitement.*opération\b', r'\bgestionnaire.*opération\b',
        r'\boperation.*manager\b', r'\bprocess.*manager\b',
    ],
    
    "Ressources Humaines": [
        r'\bRH\b', r'\bHR\b', r'\bhuman.*resource\b', r'\bressource.*humaine\b',
        r'\brecrutement\b', r'\brecruitment\b', r'\btalent\b', r'\bformation\b',
        r'\btraining\b', r'\bpaye\b', r'\bpayroll\b', r'\bcompensation\b',
        r'\brémunération\b', r'\bpeople\b', r'\bemployee\b', r'\bsalarié\b',
    ],
    
    "Juridique": [
        r'\bjuridique\b', r'\blegal\b', r'\bavocat\b', r'\blawyer\b',
        r'\bconseiller.*juridique\b', r'\blegal.*counsel\b', r'\bcontrat\b',
        r'\bcontract\b', r'\bdroit\b', r'\blaw\b', r'\blitigation\b',
        r'\bcontentieux\b',
    ],
    
    "Marketing et Communication": [
        r'\bmarketing\b', r'\bcommunication\b', r'\bpublicité\b', r'\badvertising\b',
        r'\bbrand\b', r'\bmarque\b', r'\bdigital.*marketing\b', r'\bcontent\b',
        r'\bsocial.*media\b', r'\bréseaux.*sociaux\b', r'\bevent\b', r'\bévénement\b',
    ],
    
    "Inspection / Audit": [
        r'\baudit\b', r'\binspection\b', r'\binspecteur\b', r'\bauditor\b',
        r'\binternal.*audit\b', r'\baudit.*interne\b', r'\bcontrôle.*qualité\b',
    ],
    
    "Analyse financière et économique": [
        r'\banalyste.*financier\b', r'\bfinancial.*analyst\b', r'\béconomiste\b',
        r'\beconomist\b', r'\banalyst.*economic\b', r'\banalyse.*économique\b',
        r'\bresearch\b', r'\bétude.*économique\b',
    ],
    
    "Organisation / Qualité": [
        r'\borganisation\b', r'\bqualité\b', r'\bquality\b', r'\bprocess\b',
        r'\bamélioration.*continue\b', r'\bcontinuous.*improvement\b',
        r'\blean\b', r'\bsix.*sigma\b', r'\btransformation\b',
    ],
    
    "Achat": [
        r'\bachat\b', r'\bpurchas', r'\bprocurement\b', r'\bacheteur\b',
        r'\bbuyer\b', r'\bsourcing\b', r'\bfournisseur\b', r'\bsupplier\b',
    ],
}

def classify_job_family(job_title: str, job_description: str = "") -> str:
    """
    Classifie une offre dans une famille de métier
    
    Args:
        job_title: Titre du poste
        job_description: Description du poste (optionnel)
        
    Returns:
        Nom de la famille de métier ou "Autres"
    """
    # Combiner titre et description pour l'analyse
    text = f"{job_title} {job_description}".lower()
    
    # Scores par famille
    family_scores = {}
    
    for family, patterns in JOB_FAMILIES.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Le titre a plus de poids que la description
                if re.search(pattern, job_title.lower(), re.IGNORECASE):
                    score += 3
                else:
                    score += 1
        family_scores[family] = score
    
    # Retourner la famille avec le meilleur score
    if family_scores:
        best_family = max(family_scores.items(), key=lambda x: x[1])
        if best_family[1] > 0:
            return best_family[0]
    
    return "Autres"
