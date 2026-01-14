from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes depuis tous les origines

# Configuration des banques
BANK_CONFIGS = {
    'credit_agricole': {
        'name': 'Crédit Agricole',
        'test_job_url': 'https://groupecreditagricole.jobs/fr/nos-offres-emploi/577-170479-4-gestionnaire-middle-office-titrisation-abc-gestion-hf-reference--2025-105204--/',
        'email_id': 'form-login-email',
        'password_id': 'form-login-password',
        'submit_id': 'form-login-submit',
        'connexion_link_selector': "a.cta.secondary.arrow[href*='connexion']",
        'postuler_button_selector': "button.cta.primary[data-popin='popin-application']",
        'cookie_button_selector': 'button.rgpd-btn-refuse',
        'success_indicator_id': 'form-apply-firstname',
        'error_indicators': [
            'erreur',
            'incorrect',
            'invalid',
            'échec',
            'identifiant ou mot de passe incorrect',
            'email ou mot de passe incorrect',
            'renseigner un adresse e-mail au format attendu',
            'format attendu',
            'tentatives',
            'vous reste',
            'mot de passe incorrect',
            'adresse e-mail',
            'format',
            'connexion impossible',
            'compte invalide'
        ]
    }
}


def test_credit_agricole_connection(email: str, password: str, timeout: int = 30):
    """Teste la connexion à Crédit Agricole avec Playwright"""
    logger.info(f"🔍 Test de connexion pour Crédit Agricole avec {email}")
    
    try:
        with sync_playwright() as p:
            # Lancer le navigateur en mode headless
            # Spécifier le chemin explicite pour Render
            import os
            browser_path = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', None)
            launch_options = {'headless': True}
            if browser_path:
                launch_options['executable_path'] = f'{browser_path}/chromium-1091/chrome-linux/chrome'
            browser = p.chromium.launch(**launch_options)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            config = BANK_CONFIGS['credit_agricole']
            
            try:
                # Ouvrir la page d'offre d'emploi
                logger.info(f"📡 Ouverture de la page d'offre: {config['test_job_url']}")
                page.goto(config['test_job_url'], wait_until='domcontentloaded', timeout=timeout * 1000)
                time.sleep(2)
                
                # Gérer les cookies
                try:
                    cookie_button = page.wait_for_selector(config['cookie_button_selector'], timeout=5000)
                    cookie_button.click()
                    time.sleep(1)
                    logger.info("✅ Bannière de cookies refusée")
                except PlaywrightTimeout:
                    logger.info("⚠️ Bannière de cookies non trouvée")
                
                # Cliquer sur "Je postule"
                logger.info("🔘 Clic sur 'Je postule'")
                postuler = page.wait_for_selector(config['postuler_button_selector'], timeout=10000)
                page.evaluate("element => element.scrollIntoView({block: 'center'})", postuler)
                postuler.click()
                time.sleep(2)
                logger.info("✅ 'Je postule' cliqué")
                
                # Cliquer sur le lien de connexion
                logger.info("🔗 Clic sur le lien de connexion")
                connexion = page.wait_for_selector(config['connexion_link_selector'], timeout=10000)
                connexion.click()
                time.sleep(2)
                
                # Remplir le formulaire de connexion
                logger.info("✍️  Remplissage du formulaire de connexion")
                email_field = page.wait_for_selector(f"#{config['email_id']}", timeout=10000)
                password_field = page.wait_for_selector(f"#{config['password_id']}", timeout=10000)
                
                email_field.fill(email)
                time.sleep(0.5)
                password_field.fill(password)
                time.sleep(0.5)
                
                # Soumettre le formulaire
                logger.info("📤 Soumission du formulaire")
                submit_button = page.wait_for_selector(f"#{config['submit_id']}", timeout=10000)
                
                # Capturer l'URL avant soumission
                url_before_submit = page.url
                logger.info(f"📍 URL avant soumission: {url_before_submit}")
                
                # Capturer l'état des champs avant soumission
                email_value_before = email_field.input_value()
                logger.info(f"📧 Email saisi: {email_value_before}")
                
                submit_button.click()
                logger.info("✅ Formulaire soumis, attente de la réponse...")
                
                # Attendre que la page réagisse - utiliser plusieurs méthodes
                # 1. Attendre que l'URL change OU qu'un élément apparaisse/disparaisse
                try:
                    # Attendre soit un changement d'URL, soit l'apparition du formulaire de candidature
                    # soit l'apparition d'un message d'erreur
                    page.wait_for_function(
                        """
                        () => {
                            const url = window.location.href;
                            const hasSuccessForm = document.getElementById('form-apply-firstname') !== null;
                            const hasError = document.body.innerText.toLowerCase().includes('incorrect') || 
                                           document.body.innerText.toLowerCase().includes('erreur') ||
                                           document.body.innerText.toLowerCase().includes('tentatives');
                            return hasSuccessForm || hasError || url !== arguments[0];
                        }
                        """,
                        url_before_submit,
                        timeout=15000
                    )
                    logger.info("✅ Page a réagi (URL ou contenu changé)")
                except PlaywrightTimeout:
                    logger.warning("⚠️ Timeout en attendant la réaction de la page")
                
                # Attendre que le réseau soit idle
                try:
                    page.wait_for_load_state('networkidle', timeout=10000)
                    logger.info("✅ État réseau idle atteint")
                except PlaywrightTimeout:
                    logger.warning("⚠️ Timeout sur networkidle")
                
                # Attendre un peu plus pour que les messages d'erreur/succès apparaissent
                time.sleep(4)  # Augmenté à 4 secondes
                
                # Vérifier si l'URL a changé
                url_after_submit = page.url
                logger.info(f"📍 URL après soumission: {url_after_submit}")
                
                if url_before_submit == url_after_submit:
                    logger.warning("⚠️ URL n'a PAS changé après soumission - probable échec")
                else:
                    logger.info("✅ URL a changé après soumission")
                
                # Récupérer l'URL actuelle et le texte de la page
                current_url = page.url
                
                # Récupérer le texte de la page de manière plus complète
                try:
                    page_text = page.inner_text('body').lower()
                    # Récupérer aussi le HTML pour vérifier les messages d'erreur dans les éléments spécifiques
                    page_html = page.content().lower()
                except:
                    page_text = ''
                    page_html = ''
                
                logger.info(f"📍 URL actuelle: {current_url}")
                logger.info(f"📄 Texte de la page (extrait): {page_text[:200]}...")
                
                # PRIORITÉ 1: Vérifier les erreurs AVANT de vérifier le succès
                logger.info("🔍 Vérification des erreurs...")
                logger.info(f"📄 Longueur du texte de la page: {len(page_text)} caractères")
                logger.info(f"📄 Extrait du texte (200 premiers caractères): {page_text[:200]}")
                
                # Vérifier dans le texte ET dans le HTML (pour capturer les messages d'erreur même s'ils sont dans des attributs)
                combined_text = page_text + ' ' + page_html
                
                # Vérifier chaque indicateur d'erreur
                errors_found = []
                for error_indicator in config['error_indicators']:
                    error_lower = error_indicator.lower()
                    # Vérifier dans le texte de la page
                    if error_lower in page_text:
                        logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le texte: '{error_indicator}'")
                        logger.error(f"📄 Contexte trouvé: {page_text[max(0, page_text.find(error_lower)-50):page_text.find(error_lower)+100]}")
                        errors_found.append(('text', error_indicator))
                    # Vérifier aussi dans le HTML
                    elif error_lower in page_html:
                        logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le HTML: '{error_indicator}'")
                        errors_found.append(('html', error_indicator))
                
                # Si on trouve des erreurs, on retourne immédiatement un échec
                if errors_found:
                    error_method, error_text = errors_found[0]
                    logger.error(f"❌❌❌ CONNEXION ÉCHOUÉE - Erreur détectée: {error_text}")
                    logger.error(f"❌❌❌ Toutes les erreurs trouvées: {errors_found}")
                    browser.close()
                    return {
                        'success': False,
                        'message': f'Connexion échouée: {error_text}',
                        'details': {
                            'url': current_url,
                            'error_found': error_text,
                            'detection_method': error_method,
                            'all_errors': errors_found,
                            'page_text_sample': page_text[:500]
                        }
                    }
                
                logger.info("✅ Aucune erreur détectée dans le texte/HTML")
                
                # Vérifier aussi les messages d'erreur dans les éléments de formulaire
                try:
                    # Chercher les messages d'erreur dans les divs, spans, et autres éléments
                    error_elements = page.query_selector_all('.error, .alert, .warning, [role="alert"], .message-error, .form-error')
                    for element in error_elements:
                        element_text = element.inner_text().lower()
                        for error_indicator in config['error_indicators']:
                            if error_indicator.lower() in element_text:
                                logger.warning(f"❌ Erreur détectée dans un élément: {error_indicator}")
                                browser.close()
                                return {
                                    'success': False,
                                    'message': f'Connexion échouée: {error_indicator}',
                                    'details': {
                                        'url': current_url,
                                        'error_found': error_indicator,
                                        'detection_method': 'element'
                                    }
                                }
                except Exception as e:
                    logger.info(f"⚠️ Impossible de vérifier les éléments d'erreur: {e}")
                
                # PRIORITÉ 2: Vérifier si on est toujours sur la page de connexion
                # C'est un INDICATEUR FORT d'échec
                if 'connexion' in current_url.lower() or 'login' in current_url.lower():
                    logger.warning("⚠️ URL contient 'connexion' ou 'login' - probable échec")
                    # Vérifier si les champs de connexion sont toujours présents
                    try:
                        email_field_check = page.query_selector(f"#{config['email_id']}")
                        password_field_check = page.query_selector(f"#{config['password_id']}")
                        submit_button_check = page.query_selector(f"#{config['submit_id']}")
                        
                        if email_field_check or password_field_check or submit_button_check:
                            logger.error("❌❌❌ CONNEXION ÉCHOUÉE - Toujours sur la page de connexion avec les champs visibles")
                            browser.close()
                            return {
                                'success': False,
                                'message': 'Connexion échouée: identifiants incorrects ou problème de connexion',
                                'details': {
                                    'url': current_url,
                                    'reason': 'still_on_login_page_with_fields',
                                    'email_field_present': email_field_check is not None,
                                    'password_field_present': password_field_check is not None,
                                    'submit_button_present': submit_button_check is not None
                                }
                            }
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur lors de la vérification des champs: {e}")
                
                # PRIORITÉ 3: Vérifier si on est sur le formulaire de candidature (succès)
                # MAIS SEULEMENT si on n'a PAS détecté d'erreur
                logger.info("🔍 Vérification du formulaire de candidature...")
                
                # Vérification STRICTE : on doit être ABSOLUMENT sûr que c'est un succès
                try:
                    # Attendre le formulaire de candidature avec un timeout plus court
                    success_element = page.wait_for_selector(f"#{config['success_indicator_id']}", timeout=5000)
                    logger.info("✅ Élément de succès trouvé")
                    
                    # Vérifications supplémentaires STRICTES :
                    # 1. L'URL ne doit PAS contenir "connexion" ou "login"
                    # 2. Les champs de connexion ne doivent PLUS être présents
                    # 3. Le formulaire de candidature doit être visible
                    
                    url_check = 'connexion' not in current_url.lower() and 'login' not in current_url.lower()
                    logger.info(f"✅ Vérification URL: {url_check} (URL: {current_url})")
                    
                    # Vérifier que les champs de connexion ne sont PLUS présents
                    try:
                        email_field_after = page.query_selector(f"#{config['email_id']}")
                        password_field_after = page.query_selector(f"#{config['password_id']}")
                        fields_gone = email_field_after is None and password_field_after is None
                        logger.info(f"✅ Champs de connexion absents: {fields_gone}")
                    except:
                        fields_gone = True  # Si on ne peut pas vérifier, on assume qu'ils sont absents
                    
                    # Vérifier que le formulaire de candidature est bien visible
                    try:
                        form_visible = success_element.is_visible()
                        logger.info(f"✅ Formulaire de candidature visible: {form_visible}")
                    except:
                        form_visible = False
                    
                    # TOUTES les conditions doivent être remplies pour un succès
                    # Vérification ULTRA-STRICTE
                    if url_check and fields_gone and form_visible:
                        # Vérification supplémentaire : s'assurer que l'URL a vraiment changé
                        if url_before_submit != url_after_submit:
                            logger.info("✅✅✅ CONNEXION RÉUSSIE - Toutes les vérifications passées !")
                            browser.close()
                            return {
                                'success': True,
                                'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                                'details': {
                                    'url': current_url,
                                    'url_before': url_before_submit,
                                    'url_after': url_after_submit,
                                    'reason': 'application_form_detected',
                                    'checks': {
                                        'url_ok': url_check,
                                        'fields_gone': fields_gone,
                                        'form_visible': form_visible,
                                        'url_changed': url_before_submit != url_after_submit
                                    }
                                }
                            }
                        else:
                            logger.error("❌❌❌ URL n'a pas changé malgré le formulaire détecté - ÉCHEC")
                            browser.close()
                            return {
                                'success': False,
                                'message': 'Connexion échouée: impossible de confirmer la connexion (URL inchangée)',
                                'details': {
                                    'url': current_url,
                                    'url_before': url_before_submit,
                                    'url_after': url_after_submit,
                                    'reason': 'url_not_changed',
                                    'checks': {
                                        'url_ok': url_check,
                                        'fields_gone': fields_gone,
                                        'form_visible': form_visible,
                                        'url_changed': False
                                    }
                                }
                            }
                    else:
                        logger.error(f"❌❌❌ CONNEXION ÉCHOUÉE - Vérifications échouées: url={url_check}, fields={fields_gone}, visible={form_visible}")
                        browser.close()
                        return {
                            'success': False,
                            'message': 'Connexion échouée: impossible de confirmer la connexion',
                            'details': {
                                'url': current_url,
                                'url_before': url_before_submit,
                                'url_after': url_after_submit,
                                'reason': 'verification_failed',
                                'checks': {
                                    'url_ok': url_check,
                                    'fields_gone': fields_gone,
                                    'form_visible': form_visible
                                }
                            }
                        }
                except PlaywrightTimeout:
                    # Si le formulaire de candidature n'est pas trouvé, c'est un ÉCHEC
                    logger.warning("❌ Formulaire de candidature NON trouvé - ÉCHEC")
                    
                    # Vérification finale: si on est toujours sur la page de connexion
                    if 'connexion' in current_url.lower() or 'login' in current_url.lower():
                        logger.warning("❌ Toujours sur la page de connexion - ÉCHEC")
                        browser.close()
                        return {
                            'success': False,
                            'message': 'Connexion échouée: identifiants incorrects ou problème de connexion',
                            'details': {
                                'url': current_url,
                                'reason': 'still_on_login_page'
                            }
                        }
                    
                    # Vérifier une dernière fois si les champs de connexion sont toujours là
                    try:
                        email_field_final = page.query_selector(f"#{config['email_id']}")
                        if email_field_final:
                            logger.warning("❌ Champs de connexion toujours présents - ÉCHEC")
                            browser.close()
                            return {
                                'success': False,
                                'message': 'Connexion échouée: identifiants incorrects',
                                'details': {
                                    'url': current_url,
                                    'reason': 'login_fields_still_present'
                                }
                            }
                    except:
                        pass
                    
                    # Cas indéterminé mais on considère comme ÉCHEC par défaut
                    logger.warning("⚠️ Impossible de confirmer le succès - ÉCHEC par défaut")
                    browser.close()
                    return {
                        'success': False,
                        'message': 'Connexion échouée: impossible de confirmer la connexion. Vérifiez vos identifiants.',
                        'details': {
                            'url': current_url,
                            'reason': 'cannot_confirm_success'
                        }
                    }
            
            except PlaywrightTimeout as e:
                logger.error(f"❌ Timeout: {str(e)}")
                browser.close()
                return {
                    'success': False,
                    'message': 'Timeout: La page a pris trop de temps à répondre',
                    'details': {
                        'url': page.url if 'page' in locals() else 'unknown',
                        'error': str(e)
                    }
                }
            except Exception as e:
                logger.error(f"❌ Erreur lors du test de connexion: {e}")
                browser.close()
                return {
                    'success': False,
                    'message': f'Erreur technique: {str(e)}',
                    'details': {
                        'error': str(e)
                    }
                }
    
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'message': f'Erreur critique: {str(e)}',
            'details': {
                'error': str(e)
            }
        }


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    logger.info("🏥 Health check appelé")
    return jsonify({'status': 'ok', 'message': 'Taleos Connection Tester API is running'}), 200

@app.route('/', methods=['GET'])
def root():
    """Endpoint racine pour tester"""
    logger.info("🏠 Root endpoint appelé")
    return jsonify({'status': 'ok', 'message': 'Taleos Connection Tester API', 'endpoints': ['/health', '/api/test-bank-connection']}), 200


@app.route('/api/test-bank-connection', methods=['POST', 'OPTIONS'])
def test_bank_connection():
    """Endpoint pour tester une connexion bancaire"""
    # LOG IMMÉDIAT pour voir si la requête arrive
    logger.info("=" * 80)
    logger.info("🚀 REQUÊTE REÇUE sur /api/test-bank-connection")
    logger.info(f"📍 Méthode: {request.method}")
    logger.info(f"📍 Headers: {dict(request.headers)}")
    logger.info(f"📍 Remote Address: {request.remote_addr}")
    logger.info("=" * 80)
    
    # Gérer CORS preflight
    if request.method == 'OPTIONS':
        logger.info("✅ OPTIONS preflight - retour CORS")
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
    
    try:
        logger.info("📥 Récupération des données JSON...")
        data = request.get_json()
        logger.info(f"📦 Données reçues: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        bank_id = data.get('bank_id', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        logger.info(f"🔍 Validation des données: bank_id={bank_id}, email={email[:10]}...")
        if not bank_id or not email or not password:
            logger.warning("❌ Données manquantes")
            return jsonify({
                'success': False,
                'message': 'bank_id, email et password requis'
            }), 400
        
        if '@' not in email:
            logger.warning(f"❌ Format email invalide: {email}")
            return jsonify({
                'success': False,
                'message': 'Format email invalide'
            }), 400
        
        # Tester la connexion
        logger.info(f"🚀 Démarrage du test de connexion pour {bank_id}")
        if bank_id == 'credit_agricole':
            result = test_credit_agricole_connection(email, password, timeout=30)
            logger.info(f"✅ Test terminé: success={result.get('success')}")
        else:
            logger.warning(f"❌ Banque non implémentée: {bank_id}")
            return jsonify({
                'success': False,
                'message': f'Banque {bank_id} non encore implémentée'
            }), 400
        
        logger.info("📤 Envoi de la réponse au client")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"❌ Erreur dans l'endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
