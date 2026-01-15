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
        
        # ---------- Aller DIRECTEMENT sur la page de connexion ----------
        login_url = 'https://groupecreditagricole.jobs/fr/connexion/'
        logger.info(f"📡 Ouverture directe de la page de connexion: {login_url}")
        driver.get(login_url)
        time.sleep(2)
        
        # ---------- Gérer les cookies (si présents) ----------
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config['cookie_button_selector']))
            )
            safe_click(driver, cookie_button)
            time.sleep(1)
            logger.info("✅ Bannière de cookies refusée")
        except (TimeoutException, NoSuchElementException):
            logger.info("⚠️ Bannière de cookies non trouvée")
        
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
        
        # ---------- PRIORITÉ 1: Vérifier les ERREURS IMMÉDIATEMENT (elles apparaissent en 1-2 secondes) ----------
        logger.info("🔍 Vérification IMMÉDIATE des erreurs...")
        
        # Attendre 1 seconde que le message d'erreur apparaisse
        time.sleep(1)
        
        # Vérifier plusieurs fois avec des intervalles courts (max 4 secondes)
        max_error_checks = 4
        check_interval = 1
        
        for error_check in range(1, max_error_checks + 1):
            logger.info(f"🔍 Vérification erreurs #{error_check}/{max_error_checks} (après {error_check * check_interval}s)...")
            
            current_url = driver.current_url
            
            # Récupérer le texte de la page
            try:
                page_text = driver.find_element(By.TAG_NAME, 'body').text.lower()
                page_html = driver.page_source.lower()
            except:
                page_text = ''
                page_html = ''
            
            # Chercher les messages d'erreur dans des éléments spécifiques d'abord
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, 
                    '.error, .alert, .warning, [role="alert"], .message-error, .form-error, '
                    '.alert-danger, .alert-error, .popin-error, .modal-error, '
                    '.popin, .modal, [class*="error"], [class*="alert"], [id*="error"], [id*="alert"]')
                
                for error_element in error_elements:
                    try:
                        # Vérifier si l'élément est visible
                        if not error_element.is_displayed():
                            continue
                        
                        error_text = error_element.text.lower()
                        if not error_text or len(error_text.strip()) < 5:
                            continue
                        
                        logger.info(f"🔍 Élément d'erreur visible trouvé (check #{error_check}), texte: {error_text[:150]}")
                        
                        # Vérifier les messages d'erreur complets dans ces éléments
                        for error_indicator in sorted(config['error_indicators'], key=len, reverse=True):
                            if error_indicator.lower() in error_text:
                                logger.error(f"❌❌❌ ERREUR DÉTECTÉE (check #{error_check}): '{error_indicator}'")
                                logger.error(f"📄 Texte complet: {error_text[:300]}")
                                
                                # Construire un message d'erreur descriptif
                                if 'email ou mot de passe incorrect' in error_indicator.lower():
                                    error_message = 'Connexion échouée: email ou mot de passe incorrect'
                                elif 'tentatives' in error_indicator.lower() or 'vous reste' in error_indicator.lower():
                                    error_message = 'Connexion échouée: identifiants incorrects'
                                else:
                                    error_message = f'Connexion échouée: {error_indicator}'
                                
                                final_url = driver.current_url
                                
                                # Fermer le driver proprement
                                try:
                                    driver.quit()
                                except Exception as e:
                                    logger.warning(f"⚠️ Erreur lors de la fermeture du driver: {e}")
                                    try:
                                        driver.close()
                                    except:
                                        pass
                                
                                logger.error(f"❌❌❌ ARRÊT IMMÉDIAT après {error_check} seconde(s)")
                                return {
                                    'success': False,
                                    'message': error_message,
                                    'details': {
                                        'url': final_url,
                                        'error_found': error_indicator,
                                        'detection_method': 'error_element',
                                        'check_number': error_check,
                                        'element_text': error_text[:200]
                                    }
                                }
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur lors de l'analyse d'un élément: {e}")
                        continue
            except Exception as e:
                logger.warning(f"⚠️ Erreur lors de la recherche d'éléments d'erreur: {e}")
            
            # Si on a trouvé une erreur, on arrête
            # Sinon, vérifier aussi dans le texte de la page pour les messages complets
            for error_indicator in sorted(config['error_indicators'], key=len, reverse=True):
                if len(error_indicator) > 10:  # Messages complets uniquement
                    error_lower = error_indicator.lower()
                    if error_lower in page_text:
                        error_pos = page_text.find(error_lower)
                        context = page_text[max(0, error_pos-50):min(len(page_text), error_pos+len(error_indicator)+50)]
                        if 'erreur' in context or 'incorrect' in context or 'tentatives' in context:
                            logger.error(f"❌❌❌ ERREUR DÉTECTÉE dans le texte (check #{error_check}): '{error_indicator}'")
                            
                            if 'email ou mot de passe incorrect' in error_indicator.lower():
                                error_message = 'Connexion échouée: email ou mot de passe incorrect'
                            elif 'tentatives' in error_indicator.lower() or 'vous reste' in error_indicator.lower():
                                error_message = 'Connexion échouée: identifiants incorrects'
                            else:
                                error_message = f'Connexion échouée: {error_indicator}'
                            
                            final_url = driver.current_url
                            
                            try:
                                driver.quit()
                            except Exception as e:
                                logger.warning(f"⚠️ Erreur lors de la fermeture du driver: {e}")
                                try:
                                    driver.close()
                                except:
                                    pass
                            
                            logger.error(f"❌❌❌ ARRÊT IMMÉDIAT après {error_check} seconde(s)")
                            return {
                                'success': False,
                                'message': error_message,
                                'details': {
                                    'url': final_url,
                                    'error_found': error_indicator,
                                    'detection_method': 'page_text_with_context',
                                    'check_number': error_check
                                }
                            }
            
            # Vérifier si l'URL a changé (signe de succès potentiel)
            if current_url != url_before_submit and 'connexion' not in current_url.lower() and 'login' not in current_url.lower():
                logger.info(f"✅ URL a changé et ne contient pas 'connexion' - probable succès, arrêt des vérifications d'erreur")
                break
            
            if error_check < max_error_checks:
                time.sleep(check_interval)
        
        logger.info("✅ Aucune erreur détectée après vérifications - vérification du succès...")
        
        # ---------- PRIORITÉ 2: Vérifier le SUCCÈS ----------
        # Après une connexion réussie, on est redirigé (vers la page d'accueil ou une autre page)
        # On ne cherche PAS le formulaire de candidature car on n'a pas cliqué sur "Je postule"
        # Le succès se détecte par :
        # 1. URL a changé et ne contient plus "connexion" ni "login"
        # 2. Champs de connexion ne sont plus présents
        # 3. Optionnel: présence d'éléments indiquant qu'on est connecté
        
        current_url = driver.current_url
        logger.info(f"🔍 Vérification du succès - URL actuelle: {current_url}")
        
        # Vérifier si on est toujours sur la page de connexion
        if 'connexion' in current_url.lower() or 'login' in current_url.lower():
            logger.error("❌❌❌ Toujours sur la page de connexion - ÉCHEC")
            # Vérifier si les champs de connexion sont toujours présents
            try:
                email_field = driver.find_elements(By.ID, config['email_id'])
                password_field = driver.find_elements(By.ID, config['password_id'])
                if email_field or password_field:
                    logger.error("❌❌❌ Champs de connexion toujours présents - ÉCHEC")
                    final_url = driver.current_url
                    try:
                        driver.quit()
                    except:
                        try:
                            driver.close()
                        except:
                            pass
                    return {
                        'success': False,
                        'message': 'Connexion échouée: identifiants incorrects ou problème de connexion',
                        'details': {
                            'url': final_url,
                            'reason': 'still_on_login_page_with_fields'
                        }
                    }
            except:
                pass
            
            final_url = driver.current_url
            try:
                driver.quit()
            except:
                try:
                    driver.close()
                except:
                    pass
            return {
                'success': False,
                'message': 'Connexion échouée: identifiants incorrects',
                'details': {
                    'url': final_url,
                    'reason': 'still_on_login_page'
                }
            }
        
        # Si l'URL a changé et ne contient plus "connexion" ni "login", c'est un bon signe
        logger.info("✅ URL a changé et ne contient pas 'connexion' - vérification des champs de connexion...")
        
        # Vérifier que les champs de connexion ne sont plus présents
        try:
            email_field = driver.find_elements(By.ID, config['email_id'])
            password_field = driver.find_elements(By.ID, config['password_id'])
            
            if not email_field and not password_field:
                logger.info("✅ Champs de connexion absents - SUCCÈS confirmé !")
                final_url = driver.current_url
                
                # Optionnel: vérifier la présence d'éléments indiquant qu'on est connecté
                try:
                    # Chercher des éléments communs qui indiquent qu'on est connecté
                    # (profil, déconnexion, menu utilisateur, etc.)
                    connected_indicators = driver.find_elements(By.CSS_SELECTOR, 
                        '[href*="deconnexion"], [href*="logout"], [href*="profil"], '
                        '[href*="profile"], [href*="mon-compte"], [href*="mon-compte"], '
                        '.user-menu, .account-menu, [class*="user"], [id*="user"]')
                    
                    if connected_indicators:
                        logger.info(f"✅ Éléments de profil/utilisateur trouvés: {len(connected_indicators)} - SUCCÈS confirmé !")
                except:
                    pass  # Ce n'est pas critique si on ne trouve pas ces éléments
                
                try:
                    driver.quit()
                except:
                    try:
                        driver.close()
                    except:
                        pass
                
                return {
                    'success': True,
                    'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                    'details': {
                        'url': final_url,
                        'reason': 'redirected_from_login_and_fields_absent'
                    }
                }
            else:
                logger.warning(f"⚠️ Champs de connexion encore présents - email: {len(email_field)}, password: {len(password_field)}")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la vérification des champs: {e}")
        
        # Si on arrive ici, essayer quand même de vérifier le formulaire de candidature (au cas où on serait passé par "Je postule")
        logger.info("🔍 Vérification optionnelle du formulaire de candidature (si on a cliqué sur 'Je postule')...")
        try:
            success_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, config['success_indicator_id']))
            )
            if success_element.is_displayed():
                logger.info("✅✅✅ SUCCÈS ! Formulaire de candidature détecté")
                final_url = driver.current_url
                try:
                    driver.quit()
                except:
                    try:
                        driver.close()
                    except:
                        pass
                return {
                    'success': True,
                    'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                    'details': {
                        'url': final_url,
                        'reason': 'application_form_detected'
                    }
                }
        except TimeoutException:
            # Ce n'est pas un échec si le formulaire n'est pas trouvé car on n'a pas forcément cliqué sur "Je postule"
            logger.info("ℹ️ Formulaire de candidature non trouvé (normal si on n'a pas cliqué sur 'Je postule')")
        
        # Si on arrive ici sans succès ni échec clair, c'est suspect
        logger.warning("⚠️ État ambigu - vérification finale...")
        final_url = driver.current_url
        
        # Si l'URL ne contient pas "connexion" et qu'on n'est pas sur une page d'erreur, considérer comme succès
        if 'connexion' not in final_url.lower() and 'login' not in final_url.lower():
            logger.info("✅ URL ne contient pas 'connexion' - considéré comme SUCCÈS")
            try:
                driver.quit()
            except:
                try:
                    driver.close()
                except:
                    pass
            return {
                'success': True,
                'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                'details': {
                    'url': final_url,
                    'reason': 'url_changed_no_login_keywords'
                }
            }
        
        # Si rien ne fonctionne, échec
        logger.error("❌❌❌ Impossible de déterminer le statut de la connexion - ÉCHEC")
        try:
            driver.quit()
        except:
            try:
                driver.close()
            except:
                pass
        return {
            'success': False,
            'message': 'Connexion échouée: impossible de déterminer le statut de la connexion',
            'details': {
                'url': final_url,
                'reason': 'ambiguous_state'
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
