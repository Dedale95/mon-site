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

# Configuration du logging (silencieux)
logging.basicConfig(level=logging.WARNING, format='%(message)s')
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
    # Configuration Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        # Initialiser le driver Chrome
        if ChromeDriverManager:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        wait = WebDriverWait(driver, timeout)
        config = BANK_CONFIGS['credit_agricole']
        
        # Aller directement sur la page de connexion
        login_url = 'https://groupecreditagricole.jobs/fr/connexion/'
        driver.get(login_url)
        
        # Attendre que la page soit chargée (pas de time.sleep)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, config['email_id'])))
        
        # Gérer les cookies IMMÉDIATEMENT (timeout court)
        try:
            cookie_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config['cookie_button_selector']))
            )
            driver.execute_script("arguments[0].click();", cookie_button)  # JavaScript = plus rapide
        except (TimeoutException, NoSuchElementException):
            pass  # Pas de bannière cookies
        
        # Remplir le formulaire avec JavaScript (plus rapide)
        email_field = wait.until(EC.presence_of_element_located((By.ID, config['email_id'])))
        password_field = driver.find_element(By.ID, config['password_id'])
        
        driver.execute_script("arguments[0].value = ''; arguments[0].value = arguments[1];", email_field, email)
        driver.execute_script("arguments[0].value = ''; arguments[0].value = arguments[1];", password_field, password)
        
        # Soumettre le formulaire
        url_before_submit = driver.current_url
        submit_button = driver.find_element(By.ID, config['submit_id'])
        driver.execute_script("arguments[0].click();", submit_button)  # JavaScript = plus rapide
        
        # Vérifier les erreurs immédiatement (intervalles courts)
        time.sleep(0.5)  # Attendre que la page réagisse
        
        max_error_checks = 3
        check_interval = 0.5  # Réduit de 1s à 0.5s
        
        for error_check in range(max_error_checks):
            current_url = driver.current_url
            
            # Chercher les erreurs dans les éléments spécifiques
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, 
                    '.error, .alert, .warning, [role="alert"], .popin, .modal, [class*="error"], [class*="alert"]')
                
                for error_element in error_elements:
                    try:
                        if not error_element.is_displayed():
                            continue
                        error_text = error_element.text.lower()
                        if len(error_text.strip()) < 5:
                            continue
                        
                        # Vérifier les messages d'erreur
                        for error_indicator in sorted(config['error_indicators'], key=len, reverse=True):
                            if error_indicator.lower() in error_text:
                                if 'email ou mot de passe incorrect' in error_indicator.lower():
                                    error_message = 'Connexion échouée: email ou mot de passe incorrect'
                                else:
                                    error_message = 'Connexion échouée: identifiants incorrects'
                                
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
                                    'message': error_message,
                                    'details': {'url': final_url}
                                }
                    except:
                        continue
            except:
                pass
            
            # Vérifier si l'URL a changé (succès)
            if current_url != url_before_submit and 'connexion' not in current_url.lower() and 'login' not in current_url.lower():
                break
            
            if error_check < max_error_checks - 1:
                time.sleep(check_interval)
        
        # Vérifier le succès
        current_url = driver.current_url
        
        # Si toujours sur la page de connexion → échec
        if 'connexion' in current_url.lower() or 'login' in current_url.lower():
            try:
                email_field = driver.find_elements(By.ID, config['email_id'])
                password_field = driver.find_elements(By.ID, config['password_id'])
                if email_field or password_field:
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
                        'details': {'url': final_url}
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
                'details': {'url': final_url}
            }
        
        # Vérifier que les champs de connexion ne sont plus présents
        try:
            email_field = driver.find_elements(By.ID, config['email_id'])
            password_field = driver.find_elements(By.ID, config['password_id'])
            
            if not email_field and not password_field:
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
                    'details': {'url': final_url}
                }
        except:
            pass
        
        # Formulaire de candidature (si on a cliqué sur "Je postule")
        try:
            success_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, config['success_indicator_id']))
            )
            if success_element.is_displayed():
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
                    'details': {'url': final_url}
                }
        except:
            pass
        
        # Si URL a changé (pas de "connexion") → succès
        final_url = driver.current_url
        if 'connexion' not in final_url.lower() and 'login' not in final_url.lower():
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
                'details': {'url': final_url}
            }
        
        # Échec par défaut
        try:
            driver.quit()
        except:
            try:
                driver.close()
            except:
                pass
        return {
            'success': False,
            'message': 'Connexion échouée: impossible de déterminer le statut',
            'details': {'url': final_url}
        }
        
    except TimeoutException as e:
        return {
            'success': False,
            'message': 'Timeout: La page a pris trop de temps à répondre',
            'details': {'url': driver.current_url if driver else 'unknown'}
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erreur technique: {str(e)}',
            'details': {'error': str(e)}
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
