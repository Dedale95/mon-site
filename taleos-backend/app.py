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
            # Sur Render, Playwright installe dans un chemin spécifique
            import os
            from pathlib import Path
            
            # Essayer plusieurs chemins possibles pour Chromium
            possible_paths = [
                # Chemin Render standard
                Path('/opt/render/.cache/ms-playwright/chromium-1091/chrome-linux/chrome'),
                # Chemin home
                Path.home() / '.cache' / 'ms-playwright' / 'chromium-1091' / 'chrome-linux' / 'chrome',
                # Chemin avec variable d'environnement
                Path(os.environ.get('PLAYWRIGHT_BROWSERS_PATH', '')) / 'chromium-1091' / 'chrome-linux' / 'chrome' if os.environ.get('PLAYWRIGHT_BROWSERS_PATH') else None,
            ]
            
            browser = None
            chromium_found = False
            
            for chromium_path in possible_paths:
                if chromium_path and chromium_path.exists():
                    logger.info(f"✅ Chromium trouvé à: {chromium_path}")
                    try:
                        browser = p.chromium.launch(headless=True, executable_path=str(chromium_path))
                        chromium_found = True
                        break
                    except Exception as e:
                        logger.warning(f"⚠️ Impossible de lancer Chromium depuis {chromium_path}: {e}")
                        continue
            
            # Si aucun chemin explicite n'a fonctionné, laisser Playwright trouver automatiquement
            if not chromium_found:
                logger.info("🔍 Tentative de lancement Chromium avec chemin automatique de Playwright")
                try:
                    browser = p.chromium.launch(headless=True)
                    chromium_found = True
                except Exception as launch_error:
                    logger.error(f"❌ Erreur lors du lancement de Chromium: {launch_error}")
                    # Dernière tentative : installer Playwright à la volée (ne fonctionnera pas sur Render mais on essaie)
                    raise Exception(f"Chromium non disponible. Erreur: {launch_error}. Vérifiez que 'playwright install chromium' a été exécuté dans le build command.")
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
                logger.info("✅ Formulaire soumis, vérification IMMÉDIATE des erreurs...")
                
                # PRIORITÉ ABSOLUE : Vérifier les erreurs IMMÉDIATEMENT après soumission
                # Les messages d'erreur apparaissent très rapidement (1-2 secondes)
                # On vérifie plusieurs fois avec des intervalles courts pour ne pas manquer l'erreur
                errors_found = []
                max_checks = 6  # Vérifier 6 fois maximum
                check_interval = 1  # Toutes les 1 seconde
                
                for check_num in range(1, max_checks + 1):
                    logger.info(f"🔍 Vérification #{check_num}/{max_checks} des erreurs (après {check_num * check_interval}s)...")
                    time.sleep(check_interval)
                    
                    # Récupérer le texte et HTML actuels
                    try:
                        current_url = page.url
                        page_text = page.inner_text('body').lower()
                        page_html = page.content().lower()
                    except:
                        page_text = ''
                        page_html = ''
                        current_url = page.url
                    
                    # Vérifier chaque indicateur d'erreur
                    # PRIORITÉ aux messages complets d'abord, puis aux mots-clés courts
                    sorted_indicators = sorted(config['error_indicators'], key=len, reverse=True)
                    
                    for error_indicator in sorted_indicators:
                        error_lower = error_indicator.lower()
                        # Vérifier dans le texte de la page
                        if error_lower in page_text:
                            logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le texte (check #{check_num}): '{error_indicator}'")
                            # Extraire le contexte complet du message d'erreur
                            error_pos = page_text.find(error_lower)
                            context_start = max(0, error_pos - 100)
                            context_end = min(len(page_text), error_pos + len(error_indicator) + 200)
                            context = page_text[context_start:context_end]
                            logger.error(f"📄 Contexte complet trouvé: {context}")
                            errors_found.append(('text', error_indicator))
                            # Ne pas continuer à chercher d'autres erreurs une fois qu'on en a trouvé une
                            break
                        # Vérifier aussi dans le HTML
                        elif error_lower in page_html:
                            logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le HTML (check #{check_num}): '{error_indicator}'")
                            errors_found.append(('html', error_indicator))
                            break
                    
                    # Si on trouve des erreurs, on retourne IMMÉDIATEMENT
                    if errors_found:
                        error_method, error_text = errors_found[0]
                        logger.error(f"❌❌❌ CONNEXION ÉCHOUÉE - Erreur détectée au check #{check_num}: {error_text}")
                        logger.error(f"❌❌❌ Toutes les erreurs trouvées: {errors_found}")
                        logger.error(f"❌❌❌ ARRÊT IMMÉDIAT - Pas de vérification supplémentaire")
                        
                        # Construire un message d'erreur plus descriptif
                        if 'email ou mot de passe incorrect' in error_text.lower() or 'incorrect' in error_text.lower():
                            error_message = 'Connexion échouée: email ou mot de passe incorrect'
                        elif 'tentatives' in error_text.lower() or 'vous reste' in error_text.lower():
                            error_message = 'Connexion échouée: identifiants incorrects'
                        else:
                            error_message = f'Connexion échouée: {error_text}'
                        
                        browser.close()
                        return {
                            'success': False,
                            'message': error_message,
                            'details': {
                                'url': current_url,
                                'error_found': error_text,
                                'detection_method': error_method,
                                'all_errors': errors_found,
                                'check_number': check_num,
                                'page_text_sample': page_text[:500]
                            }
                        }
                    
                    # Vérifier aussi si l'URL a changé (signe de succès potentiel)
                    if current_url != url_before_submit and 'connexion' not in current_url.lower() and 'login' not in current_url.lower():
                        logger.info(f"✅ URL a changé et ne contient pas 'connexion' - probable succès, arrêt des vérifications d'erreur")
                        break
                
                logger.info("✅ Aucune erreur détectée après vérifications répétées - continuation des vérifications")
                
                # Attendre que le réseau soit idle (seulement si pas d'erreur détectée)
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                    logger.info("✅ État réseau idle atteint")
                except PlaywrightTimeout:
                    logger.warning("⚠️ Timeout sur networkidle, continuation...")
                
                # Récupérer l'URL finale
                url_after_submit = page.url
                current_url = page.url
                logger.info(f"📍 URL après soumission: {url_after_submit}")
                
                if url_before_submit == url_after_submit:
                    logger.warning("⚠️ URL n'a PAS changé après soumission - probable échec")
                else:
                    logger.info("✅ URL a changé après soumission")
                
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
                # C'est un ÉCHEC ABSOLU - pas de négociation possible
                if 'connexion' in current_url.lower() or 'login' in current_url.lower():
                    logger.error("❌❌❌ URL contient 'connexion' ou 'login' - ÉCHEC ABSOLU")
                    # Vérifier si les champs de connexion sont toujours présents
                    try:
                        email_field_check = page.query_selector(f"#{config['email_id']}")
                        password_field_check = page.query_selector(f"#{config['password_id']}")
                        submit_button_check = page.query_selector(f"#{config['submit_id']}")
                        
                        # Si AU MOINS UN champ est présent, c'est un échec
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
                        else:
                            # Même si les champs ne sont pas visibles, si l'URL contient connexion/login, c'est un échec
                            logger.error("❌❌❌ CONNEXION ÉCHOUÉE - URL contient 'connexion' ou 'login'")
                            browser.close()
                            return {
                                'success': False,
                                'message': 'Connexion échouée: identifiants incorrects',
                                'details': {
                                    'url': current_url,
                                    'reason': 'url_contains_login_or_connexion'
                                }
                            }
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur lors de la vérification des champs: {e}")
                        # Même en cas d'erreur, si l'URL contient connexion/login, c'est un échec
                        logger.error("❌❌❌ CONNEXION ÉCHOUÉE - URL contient 'connexion' ou 'login' (erreur vérification)")
                        browser.close()
                        return {
                            'success': False,
                            'message': 'Connexion échouée: identifiants incorrects',
                            'details': {
                                'url': current_url,
                                'reason': 'url_contains_login_or_connexion_after_error'
                            }
                        }
                
                # Vérification supplémentaire : si l'URL n'a PAS changé, c'est un échec
                if url_before_submit == url_after_submit:
                    logger.error("❌❌❌ CONNEXION ÉCHOUÉE - URL n'a PAS changé après soumission")
                    browser.close()
                    return {
                        'success': False,
                        'message': 'Connexion échouée: identifiants incorrects (URL inchangée)',
                        'details': {
                            'url': current_url,
                            'url_before': url_before_submit,
                            'url_after': url_after_submit,
                            'reason': 'url_not_changed_after_submit'
                        }
                    }
                
                # PRIORITÉ 3: Vérifier si on est sur le formulaire de candidature (succès)
                # SEULEMENT si on a passé toutes les vérifications précédentes
                logger.info("🔍 Vérification du formulaire de candidature...")
                
                # Vérification STRICTE : on doit être ABSOLUMENT sûr que c'est un succès
                try:
                    # Attendre le formulaire de candidature avec un timeout COURT
                    # Si pas trouvé en 5 secondes, c'est un échec
                    logger.info(f"⏳ Attente du formulaire de candidature (timeout: 5s)...")
                    success_element = page.wait_for_selector(f"#{config['success_indicator_id']}", timeout=5000)
                    logger.info("✅ Formulaire de candidature trouvé")
                    logger.info("✅ Élément de succès trouvé")
                    
                    # Vérifications supplémentaires STRICTES :
                    # 1. L'URL ne doit PAS contenir "connexion" ou "login" (déjà vérifié, mais on re-vérifie)
                    # 2. Les champs de connexion ne doivent PLUS être présents
                    # 3. Le formulaire de candidature doit être visible
                    # 4. L'URL DOIT avoir changé
                    
                    url_check = 'connexion' not in current_url.lower() and 'login' not in current_url.lower()
                    url_changed = url_before_submit != url_after_submit
                    logger.info(f"✅ Vérification URL: {url_check}, URL changée: {url_changed} (URL: {current_url})")
                    
                    # Si l'URL n'a pas changé, c'est un ÉCHEC ABSOLU
                    if not url_changed:
                        logger.error("❌❌❌ CONNEXION ÉCHOUÉE - URL n'a PAS changé (obligatoire pour succès)")
                        browser.close()
                        return {
                            'success': False,
                            'message': 'Connexion échouée: identifiants incorrects (URL inchangée)',
                            'details': {
                                'url': current_url,
                                'url_before': url_before_submit,
                                'url_after': url_after_submit,
                                'reason': 'url_must_change_for_success'
                            }
                        }
                    
                    # Vérifier que les champs de connexion ne sont PLUS présents
                    try:
                        email_field_after = page.query_selector(f"#{config['email_id']}")
                        password_field_after = page.query_selector(f"#{config['password_id']}")
                        fields_gone = email_field_after is None and password_field_after is None
                        logger.info(f"✅ Champs de connexion absents: {fields_gone}")
                        
                        # Si les champs sont toujours présents, c'est un échec
                        if not fields_gone:
                            logger.error("❌❌❌ CONNEXION ÉCHOUÉE - Champs de connexion toujours présents")
                            browser.close()
                            return {
                                'success': False,
                                'message': 'Connexion échouée: identifiants incorrects',
                                'details': {
                                    'url': current_url,
                                    'reason': 'login_fields_still_present_despite_form',
                                    'email_field_present': email_field_after is not None,
                                    'password_field_present': password_field_after is not None
                                }
                            }
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur vérification champs: {e}")
                        fields_gone = False  # En cas de doute, on considère comme échec
                    
                    # Vérifier que le formulaire de candidature est bien visible
                    try:
                        form_visible = success_element.is_visible()
                        logger.info(f"✅ Formulaire de candidature visible: {form_visible}")
                    except:
                        form_visible = False
                    
                    # TOUTES les conditions doivent être remplies pour un succès
                    if url_check and fields_gone and form_visible and url_changed:
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
                                    'url_changed': url_changed
                                }
                            }
                        }
                    else:
                        logger.error(f"❌❌❌ CONNEXION ÉCHOUÉE - Vérifications échouées: url={url_check}, fields={fields_gone}, visible={form_visible}, changed={url_changed}")
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
                                    'form_visible': form_visible,
                                    'url_changed': url_changed
                                }
                            }
                        }
                except PlaywrightTimeout:
                    # Si le formulaire de candidature n'est pas trouvé, c'est un ÉCHEC
                    logger.error("❌❌❌ TIMEOUT - Formulaire de candidature NON trouvé après 5s - ÉCHEC")
                    logger.error(f"❌❌❌ URL actuelle: {current_url}")
                    logger.error(f"❌❌❌ URL avant soumission: {url_before_submit}")
                    browser.close()
                    return {
                        'success': False,
                        'message': 'Connexion échouée: identifiants incorrects (formulaire de candidature non accessible)',
                        'details': {
                            'url': current_url,
                            'url_before': url_before_submit,
                            'reason': 'application_form_not_found_timeout'
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
