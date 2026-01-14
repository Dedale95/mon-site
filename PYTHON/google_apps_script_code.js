/**
 * Google Apps Script pour tester les connexions bancaires
 * 
 * Ce script reçoit les requêtes POST depuis le frontend et teste les connexions
 * 
 * IMPORTANT : Ce code appelle un service externe qui exécute le script Python
 * Vous devez déployer votre script Python quelque part (Cloud Functions, serveur web, etc.)
 * 
 * Configuration requise :
 * 1. Déployer ce script comme "Web App"
 * 2. Configurer : Exécuter en tant que "Moi" / Qui a accès "Tous"
 */

// URL du service qui exécute le script Python (à configurer)
// Exemples :
// - Google Cloud Functions
// - AWS Lambda
// - Votre propre serveur
// - Autre service web
const PYTHON_SERVICE_URL = 'https://votre-service.com/api/test-connection';

/**
 * Fonction principale qui reçoit les requêtes POST
 */
function doPost(e) {
  try {
    // Logger pour le débogage
    console.log('Requête reçue:', e.postData.contents);
    
    // Parser les données JSON reçues
    const requestData = JSON.parse(e.postData.contents);
    const bankId = requestData.bank_id;
    const email = requestData.email;
    const password = requestData.password;
    
    // Validation des données
    if (!bankId || !email || !password) {
      return createResponse(false, 'bank_id, email et password requis', null);
    }
    
    // Option 1 : Appeler un service externe qui exécute le script Python
    // (Recommandé si vous avez déployé votre script Python quelque part)
    if (PYTHON_SERVICE_URL && PYTHON_SERVICE_URL !== 'https://votre-service.com/api/test-connection') {
      try {
        const response = UrlFetchApp.fetch(PYTHON_SERVICE_URL, {
          method: 'post',
          contentType: 'application/json',
          payload: JSON.stringify({
            bank_id: bankId,
            email: email,
            password: password
          }),
          muteHttpExceptions: true
        });
        
        const result = JSON.parse(response.getContentText());
        return createResponse(result.success, result.message, result.details);
      } catch (error) {
        console.error('Erreur appel service externe:', error);
        return createResponse(false, 'Erreur lors de l\'appel au service de test: ' + error.toString(), null);
      }
    }
    
    // Option 2 : Réimplémenter la logique directement ici
    // (Plus complexe - nécessite d'utiliser des bibliothèques JavaScript)
    // Pour l'instant, on retourne une erreur
    return createResponse(false, 'Service non configuré. Configurez PYTHON_SERVICE_URL ou implémentez la logique ici.', null);
    
  } catch (error) {
    console.error('Erreur dans doPost:', error);
    return createResponse(false, 'Erreur serveur: ' + error.toString(), null);
  }
}

/**
 * Fonction GET pour tester (optionnel)
 */
function doGet(e) {
  return createResponse(false, 'Utilisez POST pour tester les connexions', null);
}

/**
 * Fonction helper pour créer une réponse JSON
 */
function createResponse(success, message, details) {
  const response = {
    success: success,
    message: message
  };
  
  if (details) {
    response.details = details;
  }
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Fonction de test (optionnel - pour tester dans l'éditeur)
 */
function test() {
  const testData = {
    bank_id: 'credit_agricole',
    email: 'test@example.com',
    password: 'test123'
  };
  
  const e = {
    postData: {
      contents: JSON.stringify(testData)
    }
  };
  
  const result = doPost(e);
  console.log(result.getContentText());
}
