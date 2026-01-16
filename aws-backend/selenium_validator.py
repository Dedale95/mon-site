#!/usr/bin/env python3
"""
Validateur d'identifiants Crédit Agricole - Version optimisée pour production
Headless, rapide (8-12s), robuste, avec anti-détection
"""

import logging
from typing import Dict, Optional
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configuration logging
logger = logging.getLogger(__name__)


class CreditAgricoleValidator:
    """Validateur d'identifiants Crédit Agricole optimisé pour cloud"""
    
    # Configuration
    LOGIN_URL = 'https://groupecreditagricole.jobs/fr/connexion/'
    TIMEOUT_SHORT = 3  # Cookies, éléments rapides
    TIMEOUT_MEDIUM = 8  # Chargement page, formulaire
    TIMEOUT_LONG = 12  # Vérification post-login
    
    # Sélecteurs
    SELECTORS = {
        'email': 'form-login-email',
        'password': 'form-login-password',
        'submit': 'form-login-submit',
        'cookie_btn': 'button.rgpd-btn-refuse',
        'error_container': '.error, .alert, [role="alert"], .popin[style*="block"]',
    }
    
    ERROR_KEYWORDS = [
        'email ou mot de passe incorrect',
        'identifiant ou mot de passe incorrect',
        'mot de passe incorrect',
        'incorrect',
        'erreur'
    ]
    
    def __init__(self, headless: bool = True):
        """
        Args:
            headless: Mode headless (True pour production)
        """
        self.headless = headless
        self.driver = None
    
    def _get_chrome_options(self) -> Options:
        """Configure Chrome avec anti-détection"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless=new')  # Nouveau mode headless Chrome
            options.add_argument('--disable-gpu')
        
        # Anti-détection de base
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent réaliste
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Performance
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.page_load_strategy = 'eager'  # Ne pas attendre images/CSS
        
        return options
    
    @contextmanager
    def _get_driver(self):
        """Context manager pour gérer le driver proprement"""
        driver = None
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self._get_chrome_options())
            driver.set_page_load_timeout(self.TIMEOUT_MEDIUM)
            
            # Anti-détection JavaScript
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                '''
            })
            
            yield driver
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    logger.warning(f"Erreur fermeture driver: {e}")
    
    def _handle_cookies(self, driver, wait_short):
        """Gère la bannière cookies rapidement"""
        try:
            cookie_btn = wait_short.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELECTORS['cookie_btn']))
            )
            driver.execute_script("arguments[0].click();", cookie_btn)
            logger.debug("Cookies refusés")
        except TimeoutException:
            logger.debug("Pas de bannière cookies")
    
    def _fill_form(self, driver, email: str, password: str):
        """Remplit le formulaire avec JavaScript (plus rapide)"""
        driver.execute_script(f"""
            document.getElementById('{self.SELECTORS['email']}').value = '{email}';
            document.getElementById('{self.SELECTORS['password']}').value = '{password}';
        """)
        logger.debug("Formulaire rempli")
    
    def _submit_form(self, driver):
        """Soumet le formulaire"""
        submit_btn = driver.find_element(By.ID, self.SELECTORS['submit'])
        driver.execute_script("arguments[0].click();", submit_btn)
        logger.debug("Formulaire soumis")
    
    def _check_errors(self, driver) -> Optional[str]:
        """
        Vérifie les messages d'erreur sur la page
        Returns: Message d'erreur si trouvé, None sinon
        """
        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, self.SELECTORS['error_container'])
            
            for elem in error_elements:
                if not elem.is_displayed():
                    continue
                
                text = elem.text.lower().strip()
                if len(text) < 5:
                    continue
                
                for keyword in self.ERROR_KEYWORDS:
                    if keyword in text:
                        logger.info(f"Erreur détectée: {keyword}")
                        return "Identifiants incorrects"
            
        except Exception as e:
            logger.warning(f"Erreur lors de la vérification des erreurs: {e}")
        
        return None
    
    def _verify_success(self, driver, url_before: str) -> bool:
        """
        Vérifie si la connexion a réussi
        Returns: True si succès, False sinon
        """
        current_url = driver.current_url
        
        # 1. URL a changé et ne contient plus "connexion"
        if current_url != url_before and 'connexion' not in current_url.lower():
            logger.info("Succès: URL changée")
            return True
        
        # 2. Les champs de formulaire ne sont plus présents
        try:
            email_fields = driver.find_elements(By.ID, self.SELECTORS['email'])
            password_fields = driver.find_elements(By.ID, self.SELECTORS['password'])
            
            if not email_fields and not password_fields:
                logger.info("Succès: formulaire disparu")
                return True
        except Exception:
            pass
        
        return False
    
    def validate(self, email: str, password: str) -> Dict[str, any]:
        """
        Valide les identifiants Crédit Agricole
        
        Args:
            email: Email de connexion
            password: Mot de passe
        
        Returns:
            Dict avec:
                - success (bool): True si identifiants valides
                - message (str): Message descriptif
                - execution_time (float): Temps d'exécution en secondes
        """
        import time
        start_time = time.time()
        
        try:
            with self._get_driver() as driver:
                wait_short = WebDriverWait(driver, self.TIMEOUT_SHORT)
                wait_medium = WebDriverWait(driver, self.TIMEOUT_MEDIUM)
                
                # 1. Charger la page de connexion
                logger.info(f"Chargement {self.LOGIN_URL}")
                driver.get(self.LOGIN_URL)
                
                # 2. Attendre le formulaire
                wait_medium.until(EC.presence_of_element_located((By.ID, self.SELECTORS['email'])))
                
                # 3. Gérer les cookies
                self._handle_cookies(driver, wait_short)
                
                # 4. Remplir et soumettre le formulaire
                self._fill_form(driver, email, password)
                url_before = driver.current_url
                self._submit_form(driver)
                
                # 5. Attendre la réponse du serveur (court délai)
                wait_short.until(lambda d: d.current_url != url_before or self._check_errors(d))
                
                # 6. Vérifier les erreurs
                error_msg = self._check_errors(driver)
                if error_msg:
                    execution_time = time.time() - start_time
                    return {
                        'success': False,
                        'message': error_msg,
                        'execution_time': round(execution_time, 2)
                    }
                
                # 7. Vérifier le succès
                if self._verify_success(driver, url_before):
                    execution_time = time.time() - start_time
                    return {
                        'success': True,
                        'message': 'Identifiants valides',
                        'execution_time': round(execution_time, 2)
                    }
                
                # 8. Cas ambigu (toujours sur page connexion mais pas d'erreur visible)
                execution_time = time.time() - start_time
                return {
                    'success': False,
                    'message': 'Identifiants incorrects',
                    'execution_time': round(execution_time, 2)
                }
        
        except TimeoutException:
            execution_time = time.time() - start_time
            logger.error("Timeout lors de la validation")
            return {
                'success': False,
                'message': 'Timeout: le site met trop de temps à répondre',
                'execution_time': round(execution_time, 2)
            }
        
        except WebDriverException as e:
            execution_time = time.time() - start_time
            logger.error(f"Erreur WebDriver: {e}")
            return {
                'success': False,
                'message': 'Erreur technique du navigateur',
                'execution_time': round(execution_time, 2)
            }
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Erreur inattendue: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'Erreur technique: {str(e)}',
                'execution_time': round(execution_time, 2)
            }


# Point d'entrée pour tests en ligne de commande
if __name__ == '__main__':
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) < 3:
        print("Usage: python selenium_validator.py <email> <password>")
        sys.exit(1)
    
    validator = CreditAgricoleValidator(headless=False)  # Visible pour debug
    result = validator.validate(sys.argv[1], sys.argv[2])
    
    print(f"\n{'='*60}")
    print(f"Résultat: {'✅ SUCCÈS' if result['success'] else '❌ ÉCHEC'}")
    print(f"Message: {result['message']}")
    print(f"Temps: {result['execution_time']}s")
    print(f"{'='*60}\n")
    
    sys.exit(0 if result['success'] else 1)
