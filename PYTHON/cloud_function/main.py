"""
Google Cloud Function pour tester les connexions bancaires
Point d'entrée pour la fonction HTTP
"""

import json
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PATH pour importer test_bank_connection
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from test_bank_connection import test_connection_sync


def test_bank_connection_http(request):
    """
    Fonction HTTP pour Google Cloud Functions
    
    Args:
        request: Flask Request object (Cloud Functions v1) ou CloudEvent (v2)
    
    Returns:
        Tuple (response_body, status_code) ou Response object
    """
    try:
        # Gérer les requêtes CORS preflight
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)
        
        # Vérifier que c'est une requête POST
        if request.method != 'POST':
            return json.dumps({
                'success': False,
                'message': 'Méthode non autorisée. Utilisez POST.'
            }), 405, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        
        # Parser les données JSON
        try:
            if hasattr(request, 'get_json'):
                data = request.get_json()
            elif hasattr(request, 'json'):
                data = request.json
            else:
                # Pour Cloud Functions v2
                data = json.loads(request.data) if hasattr(request, 'data') else {}
        except Exception as e:
            return json.dumps({
                'success': False,
                'message': f'Erreur parsing JSON: {str(e)}'
            }), 400, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        
        # Validation des données
        bank_id = data.get('bank_id', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not bank_id or not email or not password:
            return json.dumps({
                'success': False,
                'message': 'bank_id, email et password requis'
            }), 400, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        
        # Validation basique de l'email
        if '@' not in email:
            return json.dumps({
                'success': False,
                'message': 'Format email invalide'
            }), 400, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        
        # Appeler la fonction de test
        print(f"🔍 Test de connexion pour {bank_id} avec {email}")
        
        try:
            result = test_connection_sync(bank_id, email, password, timeout=30)
            
            # Retourner le résultat avec les headers CORS
            return json.dumps(result, ensure_ascii=False), 200, {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            }
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            import traceback
            traceback.print_exc()
            
            return json.dumps({
                'success': False,
                'message': f'Erreur lors du test de connexion: {str(e)}',
                'error': str(e)
            }), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    
    except Exception as e:
        print(f"❌ Erreur dans la fonction: {e}")
        import traceback
        traceback.print_exc()
        
        return json.dumps({
            'success': False,
            'message': f'Erreur serveur: {str(e)}',
            'error': str(e)
        }), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


# Pour Cloud Functions v1 (2nd gen avec Flask)
def main(request):
    """Point d'entrée principal pour Cloud Functions v1"""
    return test_bank_connection_http(request)
