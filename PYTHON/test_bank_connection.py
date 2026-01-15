#!/usr/bin/env python3
"""
Script pour tester les connexions aux sites carrière des banques
Utilise Selenium pour automatiser la connexion et vérifier si elle fonctionne
"""

import time
import sys
from pathlib import Path
from typing import Dict, Optional
import logging

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        ElementClickInterceptedException,
        TimeoutException,
        NoSuchElementException
    )
    from selenium.webdriver.common.keys import Keys
    try:
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        ChromeDriverManager = None
except ImportError:
    print("❌ Selenium n'est pas installé. Installez-le avec: pip install selenium webdriver-manager")
    sys.exit(1)

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration des banques avec leurs URLs de connexion
BANK_CONFIGS = {
    'credit_agricole': {
        'name': 'Crédit Agricole',
        'base_url': 'https://groupecreditagricole.jobs',
        'test_job_url': 'https://groupecreditagricole.jobs/fr/nos-offres-emploi/577-170479-4-gestionnaire-middle-office-titrisation-abc-gestion-hf-reference--2025-105204--/',
        'email_id': 'form-login-email',
        'password_id': 'form-login-password',
        'submit_id': 'form-login-submit',
        'connexion_link_selector': "a.cta.secondary.arrow[href*='connexion']",
        'postuler_button_selector': "button.cta.primary[data-popin='popin-application']",
        'cookie_button_selector': 'button.rgpd-btn-refuse',
        'success_indicator_id': 'form-apply-firstname',  # Formulaire de candidature après connexion
        'error_indicators': [
            'email ou mot de passe incorrect',
            'identifiant ou mot de passe incorrect',
            'renseigner un adresse e-mail au format attendu',
            'format attendu',
            'tentatives',
            'vous reste',
            'mot de passe incorrect',
            'erreur',
            'incorrect',
            'invalid',
            'échec',
            'connexion impossible',
            'compte invalide'
        ]
    },
    'societe_generale': {
        'name': 'Société Générale',
        'base_url': 'https://careers.societegenerale.com',
        'login_url': 'https://careers.societegenerale.com/login',
        'email_selector': 'input[type="email"], input[name*="email"], input[id*="email"], input[name*="username"]',
        'password_selector': 'input[type="password"], input[name*="password"], input[id*="password"]',
        'submit_selector': 'button[type="submit"], input[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter"), button:has-text("Sign in")',
        'success_indicators': ['dashboard', 'profile', 'my account', 'candidatures', 'applications'],
        'error_indicators': ['erreur', 'incorrect', 'invalid', 'failed', 'error']
    },
    'deloitte': {
        'name': 'Deloitte',
        'base_url': 'https://jobs2.deloitte.com',
        'login_url': 'https://jobs2.deloitte.com/login',
        'email_selector': 'input[type="email"], input[name*="email"], input[id*="email"], input[name*="username"]',
        'password_selector': 'input[type="password"], input[name*="password"], input[id*="password"]',
        'submit_selector': 'button[type="submit"], input[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter"), button:has-text("Sign in"), button:has-text("Log in")',
        'success_indicators': ['dashboard', 'profile', 'my account', 'applications', 'jobs'],
        'error_indicators': ['erreur', 'incorrect', 'invalid', 'failed', 'error', 'authentication failed']
    }
}


def safe_click(driver, element):
    """Clique sur un élément, même s'il est intercepté."""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def test_credit_agricole_connection(email: str, password: str, timeout: int = 30) -> Dict:
    """
    Teste la connexion à Crédit Agricole en suivant le flux réel
    
    Cette fonction ouvre automatiquement un navigateur Chrome (visible) pour :
    1. Ouvrir une page d'offre d'emploi Crédit Agricole
    2. Cliquer sur "Je postule"
    3. Cliquer sur le lien de connexion
    4. Remplir le formulaire de connexion
    5. Vérifier si la connexion a réussi en détectant le formulaire de candidature
    
    Le navigateur reste visible pour que vous puissiez voir ce qui se passe.
    """
    logger.info(f"🔍 Test de connexion pour Crédit Agricole avec {email}")
    
    # Configuration Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Fenêtre maximisée
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Masquer l'automation
    
    # Mode headless désactivé pour voir ce qui se passe pendant les tests
    # Le navigateur Chrome s'ouvrira et vous pourrez voir toutes les actions
    # chrome_options.add_argument("--headless")  # Décommenter pour activer le mode headless (invisible)
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        # Initialiser le driver Chrome
        # webdriver-manager télécharge automatiquement le bon ChromeDriver si nécessaire
        if ChromeDriverManager:
            logger.info("🌐 Ouverture du navigateur Chrome...")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        else:
            # Fallback si webdriver_manager n'est pas disponible
            # Nécessite que ChromeDriver soit dans le PATH
            logger.info("🌐 Ouverture du navigateur Chrome (sans webdriver-manager)...")
            driver = webdriver.Chrome(options=chrome_options)
        
        wait = WebDriverWait(driver, timeout)
        config = BANK_CONFIGS['credit_agricole']
        
        # ---------- Ouvrir une page d'offre d'emploi ----------
        logger.info(f"📡 Ouverture de la page d'offre: {config['test_job_url']}")
        driver.get(config['test_job_url'])
        time.sleep(2)
        
        # ---------- Gérer les cookies ----------
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config['cookie_button_selector']))
            )
            safe_click(driver, cookie_button)
            time.sleep(1)
            logger.info("✅ Bannière de cookies refusée")
        except (TimeoutException, NoSuchElementException):
            logger.info("⚠️ Bannière de cookies non trouvée")
        
        # ---------- Cliquer sur "Je postule" ----------
        logger.info("🔘 Clic sur 'Je postule'")
        postuler = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, config['postuler_button_selector']))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", postuler)
        safe_click(driver, postuler)
        time.sleep(2)
        logger.info("✅ 'Je postule' cliqué")
        
        # ---------- Cliquer sur le lien de connexion ----------
        logger.info("🔗 Clic sur le lien de connexion")
        connexion = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, config['connexion_link_selector']))
        )
        safe_click(driver, connexion)
        time.sleep(2)
        
        # ---------- Remplir le formulaire de connexion ----------
        logger.info("✍️  Remplissage du formulaire de connexion")
        email_field = wait.until(EC.element_to_be_clickable((By.ID, config['email_id'])))
        password_field = wait.until(EC.element_to_be_clickable((By.ID, config['password_id'])))
        
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.5)
        
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)
        
        # ---------- Soumettre le formulaire ----------
        logger.info("📤 Soumission du formulaire")
        url_before_submit = driver.current_url
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, config['submit_id'])))
        safe_click(driver, submit_button)
        logger.info("✅ Formulaire soumis")
        
        # ---------- PRIORITÉ 1: Vérifier le SUCCÈS d'abord (plus fiable) ----------
        # Le formulaire de candidature est un indicateur de succès très fiable
        logger.info("🔍 Vérification du SUCCÈS en premier...")
        
        # Attendre un peu que la page réagisse
        time.sleep(2)
        
        # Vérifier plusieurs fois si le formulaire de candidature apparaît
        max_success_checks = 5
        for success_check in range(1, max_success_checks + 1):
            try:
                current_url = driver.current_url
                logger.info(f"🔍 Vérification succès #{success_check}/{max_success_checks} - URL: {current_url}")
                
                # Vérifier si le formulaire de candidature est présent (SUCCÈS)
                try:
                    success_element = driver.find_element(By.ID, config['success_indicator_id'])
                    if success_element.is_displayed():
                        logger.info("✅✅✅ SUCCÈS DÉTECTÉ ! Formulaire de candidature trouvé et visible")
                        driver.quit()
                        return {
                            'success': True,
                            'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                            'details': {
                                'url': current_url,
                                'reason': 'application_form_detected',
                                'check_number': success_check
                            }
                        }
                except NoSuchElementException:
                    pass  # Pas encore trouvé, continuer
                
                # Si l'URL a changé et ne contient pas 'connexion', c'est probablement un succès
                if current_url != url_before_submit and 'connexion' not in current_url.lower() and 'login' not in current_url.lower():
                    # Vérifier que les champs de connexion ne sont plus présents
                    try:
                        email_field = driver.find_elements(By.ID, config['email_id'])
                        password_field = driver.find_elements(By.ID, config['password_id'])
                        if not email_field and not password_field:
                            logger.info("✅ URL a changé et champs de connexion absents - probable succès")
                            # Vérifier une dernière fois le formulaire de candidature
                            try:
                                success_element = WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located((By.ID, config['success_indicator_id']))
                                )
                                logger.info("✅✅✅ SUCCÈS CONFIRMÉ ! Formulaire de candidature trouvé")
                                driver.quit()
                                return {
                                    'success': True,
                                    'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                                    'details': {
                                        'url': current_url,
                                        'reason': 'application_form_detected_after_url_change'
                                    }
                                }
                            except:
                                pass  # Continuer les vérifications
                    except:
                        pass
                
                time.sleep(1)
            except Exception as e:
                logger.warning(f"⚠️ Erreur lors de la vérification de succès #{success_check}: {e}")
                time.sleep(1)
        
        logger.info("⚠️ Formulaire de candidature non trouvé après vérifications - vérification des erreurs...")
        
        # ---------- PRIORITÉ 2: Vérifier les erreurs seulement si le succès n'est pas détecté ----------
        # Vérifier les erreurs avec un contexte spécifique (dans des éléments d'erreur)
        current_url = driver.current_url
        try:
            page_text = driver.find_element(By.TAG_NAME, 'body').text.lower()
            page_html = driver.page_source.lower()
        except:
            page_text = ''
            page_html = ''
        
        # Chercher les messages d'erreur dans des éléments spécifiques d'abord
        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, '.error, .alert, .warning, [role="alert"], .message-error, .form-error, .alert-danger, .alert-error, .popin-error, .modal-error')
            for error_element in error_elements:
                try:
                    error_text = error_element.text.lower()
                    logger.info(f"🔍 Élément d'erreur trouvé, texte: {error_text[:100]}")
                    # Vérifier les messages d'erreur complets dans ces éléments
                    for error_indicator in sorted(config['error_indicators'], key=len, reverse=True):
                        if error_indicator.lower() in error_text:
                            logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans élément d'erreur: '{error_indicator}'")
                            logger.error(f"📄 Texte de l'élément: {error_text[:200]}")
                            
                            # Construire un message d'erreur descriptif
                            if 'email ou mot de passe incorrect' in error_indicator.lower():
                                error_message = 'Connexion échouée: email ou mot de passe incorrect'
                            elif 'tentatives' in error_indicator.lower() or 'vous reste' in error_indicator.lower():
                                error_message = 'Connexion échouée: identifiants incorrects'
                            else:
                                error_message = f'Connexion échouée: {error_indicator}'
                            
                            # Fermer le driver proprement
                            try:
                                driver.quit()
                            except:
                                pass
                            
                            return {
                                'success': False,
                                'message': error_message,
                                'details': {
                                    'url': current_url,
                                    'error_found': error_indicator,
                                    'detection_method': 'error_element'
                                }
                            }
                except Exception as e:
                    logger.warning(f"⚠️ Erreur lors de l'analyse d'un élément: {e}")
                    continue
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la recherche d'éléments d'erreur: {e}")
        
        # Vérifier dans le texte de la page seulement pour les messages complets
        for error_indicator in sorted(config['error_indicators'], key=len, reverse=True):
            # Ne vérifier que les messages complets (plus de 10 caractères) pour éviter les faux positifs
            if len(error_indicator) > 10:
                error_lower = error_indicator.lower()
                if error_lower in page_text:
                    # Vérifier le contexte : le message doit être dans une phrase d'erreur
                    error_pos = page_text.find(error_lower)
                    context = page_text[max(0, error_pos-50):min(len(page_text), error_pos+len(error_indicator)+50)]
                    # Vérifier que c'est bien un message d'erreur (contient "erreur" ou "incorrect" dans le contexte)
                    if 'erreur' in context or 'incorrect' in context or 'tentatives' in context:
                        logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le texte: '{error_indicator}'")
                        logger.error(f"📄 Contexte: {context}")
                        
                        # Construire un message d'erreur descriptif
                        if 'email ou mot de passe incorrect' in error_indicator.lower():
                            error_message = 'Connexion échouée: email ou mot de passe incorrect'
                        elif 'tentatives' in error_indicator.lower() or 'vous reste' in error_indicator.lower():
                            error_message = 'Connexion échouée: identifiants incorrects'
                        else:
                            error_message = f'Connexion échouée: {error_indicator}'
                        
                        # Fermer le driver proprement
                        try:
                            driver.quit()
                        except:
                            pass
                        
                        return {
                            'success': False,
                            'message': error_message,
                            'details': {
                                'url': current_url,
                                'error_found': error_indicator,
                                'detection_method': 'page_text_with_context'
                            }
                        }
        
        # ---------- PRIORITÉ 3: Vérifier si on est toujours sur la page de connexion ----------
        current_url = driver.current_url
        if 'connexion' in current_url.lower() or 'login' in current_url.lower():
            logger.error("❌❌❌ Toujours sur la page de connexion - ÉCHEC")
            # Vérifier si les champs de connexion sont toujours présents
            try:
                email_field = driver.find_elements(By.ID, config['email_id'])
                password_field = driver.find_elements(By.ID, config['password_id'])
                if email_field or password_field:
                    logger.error("❌❌❌ Champs de connexion toujours présents - ÉCHEC")
                    driver.quit()
                    return {
                        'success': False,
                        'message': 'Connexion échouée: identifiants incorrects ou problème de connexion',
                        'details': {
                            'url': current_url,
                            'reason': 'still_on_login_page_with_fields'
                        }
                    }
            except:
                pass
            
            driver.quit()
            return {
                'success': False,
                'message': 'Connexion échouée: identifiants incorrects',
                'details': {
                    'url': current_url,
                    'reason': 'still_on_login_page'
                }
            }
        
        # ---------- Dernière tentative: Vérifier le formulaire de candidature avec timeout court ----------
        logger.info("🔍 Dernière vérification du formulaire de candidature...")
        try:
            success_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, config['success_indicator_id']))
            )
            logger.info("✅✅✅ SUCCÈS ! Formulaire de candidature détecté")
            driver.quit()
            return {
                'success': True,
                'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                'details': {
                    'url': driver.current_url,
                    'reason': 'application_form_detected_final_check'
                }
            }
        except TimeoutException:
            logger.error("❌❌❌ Formulaire de candidature non trouvé - ÉCHEC")
            driver.quit()
            return {
                'success': False,
                'message': 'Connexion échouée: identifiants incorrects (formulaire de candidature non accessible)',
                'details': {
                    'url': driver.current_url,
                    'reason': 'application_form_not_found_timeout'
                }
            }
        
    except TimeoutException as e:
        logger.error(f"❌ Timeout: {str(e)}")
        return {
            'success': False,
            'message': 'Timeout: La page a pris trop de temps à répondre',
            'details': {
                'url': driver.current_url if driver else 'unknown',
                'error': str(e)
            }
        }
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de connexion: {e}")
        return {
            'success': False,
            'message': f'Erreur technique: {str(e)}',
            'details': {
                'error': str(e)
            }
        }
    finally:
        if driver:
            try:
                driver.quit()
            except:
                try:
                    driver.close()
                except:
                    pass


def test_bank_connection(bank_id: str, email: str, password: str, timeout: int = 30) -> Dict:
    """
    Teste la connexion à un site carrière bancaire
    
    Args:
        bank_id: Identifiant de la banque (credit_agricole, societe_generale, deloitte)
        email: Email de connexion
        password: Mot de passe
        timeout: Timeout en secondes
    
    Returns:
        Dict avec 'success' (bool), 'message' (str), et 'details' (dict)
    """
    if bank_id not in BANK_CONFIGS:
        return {
            'success': False,
            'message': f'Banque inconnue: {bank_id}',
            'details': {}
        }
    
    # Pour Crédit Agricole, utiliser la méthode spécifique
    if bank_id == 'credit_agricole':
        return test_credit_agricole_connection(email, password, timeout)
    
    # Pour les autres banques, utiliser une méthode générique (à implémenter si nécessaire)
    config = BANK_CONFIGS[bank_id]
    return {
        'success': False,
        'message': f'Test de connexion pour {config["name"]} non encore implémenté',
        'details': {}
    }


def test_connection_sync(bank_id: str, email: str, password: str, timeout: int = 30) -> Dict:
    """
    Version synchrone pour être appelée depuis Flask
    """
    return test_bank_connection(bank_id, email, password, timeout)


if __name__ == '__main__':
    # Test en ligne de commande
    if len(sys.argv) < 4:
        print("Usage: python test_bank_connection.py <bank_id> <email> <password>")
        print(f"Banques disponibles: {', '.join(BANK_CONFIGS.keys())}")
        sys.exit(1)
    
    bank_id = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    result = test_connection_sync(bank_id, email, password)
    
    print(f"\n{'='*60}")
    print(f"Résultat: {'✅ SUCCÈS' if result['success'] else '❌ ÉCHEC'}")
    print(f"Message: {result['message']}")
    if result['details']:
        print(f"Détails: {result['details']}")
    print(f"{'='*60}\n")
    
    sys.exit(0 if result['success'] else 1)
