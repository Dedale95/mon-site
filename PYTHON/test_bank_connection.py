#!/usr/bin/env python3
"""
Script pour tester les connexions aux sites carrière des banques
Utilise Playwright pour automatiser la connexion et vérifier si elle fonctionne
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

try:
    from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("❌ Playwright n'est pas installé. Installez-le avec: pip install playwright && playwright install")
    sys.exit(1)

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration des banques avec leurs URLs de connexion
BANK_CONFIGS = {
    'credit_agricole': {
        'name': 'Crédit Agricole',
        'base_url': 'https://www.ca-recrute.fr',
        'login_url': 'https://ca-recrute.talent-soft.com/pages/candidat/',
        'email_selector': 'input[type="email"], input[name*="email"], input[id*="email"], input[name*="identifiant"], input[id*="identifiant"], input[name*="login"], input[id*="login"]',
        'password_selector': 'input[type="password"], input[name*="password"], input[id*="password"], input[name*="pass"], input[id*="pass"]',
        'submit_selector': 'button[type="submit"], input[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter"), button:has-text("Connexion"), a:has-text("Connexion")',
        'success_indicators': ['dashboard', 'profil', 'candidatures', 'mon compte', 'espace candidat', 'mes candidatures'],
        'error_indicators': ['erreur', 'incorrect', 'invalid', 'échec', 'identifiant ou mot de passe incorrect'],
        'wait_after_submit': 5  # Attendre plus longtemps pour Crédit Agricole
    },
    'societe_generale': {
        'name': 'Société Générale',
        'base_url': 'https://careers.societegenerale.com',
        'login_url': 'https://careers.societegenerale.com/login',  # À adapter
        'email_selector': 'input[type="email"], input[name*="email"], input[id*="email"], input[name*="username"]',
        'password_selector': 'input[type="password"], input[name*="password"], input[id*="password"]',
        'submit_selector': 'button[type="submit"], input[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter"), button:has-text("Sign in")',
        'success_indicators': ['dashboard', 'profile', 'my account', 'candidatures', 'applications'],
        'error_indicators': ['erreur', 'incorrect', 'invalid', 'failed', 'error']
    },
    'deloitte': {
        'name': 'Deloitte',
        'base_url': 'https://jobs2.deloitte.com',
        'login_url': 'https://jobs2.deloitte.com/login',  # À adapter
        'email_selector': 'input[type="email"], input[name*="email"], input[id*="email"], input[name*="username"]',
        'password_selector': 'input[type="password"], input[name*="password"], input[id*="password"]',
        'submit_selector': 'button[type="submit"], input[type="submit"], button:has-text("Connexion"), button:has-text("Se connecter"), button:has-text("Sign in"), button:has-text("Log in")',
        'success_indicators': ['dashboard', 'profile', 'my account', 'applications', 'jobs'],
        'error_indicators': ['erreur', 'incorrect', 'invalid', 'failed', 'error', 'authentication failed']
    }
}


async def find_login_elements(page: Page, config: Dict) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Trouve les éléments de connexion sur la page
    Retourne (email_selector, password_selector, submit_selector)
    """
    try:
        # Attendre que la page soit chargée
        await page.wait_for_load_state('domcontentloaded', timeout=15000)
        await asyncio.sleep(1)  # Attendre un peu pour les scripts JS
        
        # Chercher les champs email avec plus de variantes
        email_selectors = [
            'input[type="email"]',
            'input[name*="email" i]',
            'input[id*="email" i]',
            'input[name*="username" i]',
            'input[id*="username" i]',
            'input[name*="login" i]',
            'input[id*="login" i]',
            'input[name*="identifiant" i]',
            'input[id*="identifiant" i]',
            'input[name*="user" i]',
            'input[id*="user" i]',
            'input[placeholder*="email" i]',
            'input[placeholder*="identifiant" i]',
            'input[placeholder*="login" i]'
        ]
        
        email_element = None
        for selector in email_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    # Prendre le premier élément visible
                    for elem in elements:
                        is_visible = await elem.is_visible()
                        if is_visible:
                            email_element = selector
                            logger.info(f"✅ Champ email trouvé: {selector}")
                            break
                    if email_element:
                        break
            except Exception as e:
                logger.debug(f"Erreur avec selector {selector}: {e}")
                continue
        
        # Chercher les champs password avec plus de variantes
        password_selectors = [
            'input[type="password"]',
            'input[name*="password" i]',
            'input[id*="password" i]',
            'input[name*="pass" i]',
            'input[id*="pass" i]',
            'input[placeholder*="password" i]',
            'input[placeholder*="mot de passe" i]'
        ]
        
        password_element = None
        for selector in password_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    # Prendre le premier élément visible
                    for elem in elements:
                        is_visible = await elem.is_visible()
                        if is_visible:
                            password_element = selector
                            logger.info(f"✅ Champ password trouvé: {selector}")
                            break
                    if password_element:
                        break
            except Exception as e:
                logger.debug(f"Erreur avec selector {selector}: {e}")
                continue
        
        # Chercher le bouton de soumission avec plus de variantes
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Connexion")',
            'button:has-text("Se connecter")',
            'button:has-text("Sign in")',
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'a:has-text("Connexion")',
            'a:has-text("Se connecter")',
            'button.button-primary',
            'button.btn-primary',
            'button.btn',
            'form button:not([type="button"])',
            'form input[type="submit"]',
            'button[class*="submit"]',
            'button[class*="login"]',
            'button[class*="connect"]'
        ]
        
        submit_element = None
        for selector in submit_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    # Prendre le premier élément visible et cliquable
                    for elem in elements:
                        is_visible = await elem.is_visible()
                        if is_visible:
                            submit_element = selector
                            logger.info(f"✅ Bouton submit trouvé: {selector}")
                            break
                    if submit_element:
                        break
            except Exception as e:
                logger.debug(f"Erreur avec selector {selector}: {e}")
                continue
        
        return email_element, password_element, submit_element
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche des éléments: {e}")
        return None, None, None


async def test_bank_connection(bank_id: str, email: str, password: str, timeout: int = 30) -> Dict:
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
    
    config = BANK_CONFIGS[bank_id]
    logger.info(f"🔍 Test de connexion pour {config['name']} avec {email}")
    
    try:
        async with async_playwright() as p:
            # Lancer le navigateur en mode headless
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            try:
                # Pour Crédit Agricole, aller directement sur la page de login
                if bank_id == 'credit_agricole' and 'login_url' in config:
                    logger.info(f"📡 Connexion directe à la page de login: {config['login_url']}")
                    await page.goto(config['login_url'], wait_until='domcontentloaded', timeout=timeout * 1000)
                else:
                    # Aller sur la page de base
                    logger.info(f"📡 Connexion à {config['base_url']}")
                    await page.goto(config['base_url'], wait_until='domcontentloaded', timeout=timeout * 1000)
                    
                    # Chercher un lien de connexion si on n'est pas déjà sur la page de login
                    current_url = page.url
                    if 'login' not in current_url.lower() and 'signin' not in current_url.lower() and 'candidat' not in current_url.lower():
                        # Chercher un lien de connexion
                        login_links = await page.query_selector_all('a:has-text("Connexion"), a:has-text("Se connecter"), a:has-text("Sign in"), a:has-text("Login"), a[href*="login"], a[href*="candidat"]')
                        if login_links:
                            logger.info(f"🔗 Clic sur le lien de connexion")
                            await login_links[0].click()
                            await page.wait_for_load_state('domcontentloaded', timeout=15000)
                            await asyncio.sleep(2)  # Attendre le chargement
                
                # Trouver les éléments de connexion
                email_selector, password_selector, submit_selector = await find_login_elements(page, config)
                
                if not email_selector or not password_selector:
                    return {
                        'success': False,
                        'message': 'Impossible de trouver les champs de connexion sur la page',
                        'details': {
                            'url': page.url,
                            'email_found': email_selector is not None,
                            'password_found': password_selector is not None
                        }
                    }
                
                # Remplir les champs
                logger.info("✍️  Remplissage des champs de connexion")
                await page.fill(email_selector, email, timeout=5000)
                await asyncio.sleep(0.5)  # Petite pause entre les champs
                await page.fill(password_selector, password, timeout=5000)
                await asyncio.sleep(0.5)
                
                # Soumettre le formulaire
                logger.info("📤 Soumission du formulaire...")
                if submit_selector:
                    await page.click(submit_selector, timeout=5000)
                else:
                    # Essayer d'appuyer sur Enter dans le champ password
                    logger.info("⌨️  Utilisation de la touche Enter")
                    await page.press(password_selector, 'Enter')
                
                # Attendre la réponse (soit succès, soit erreur)
                logger.info("⏳ Attente de la réponse...")
                wait_time = config.get('wait_after_submit', 3)
                await asyncio.sleep(wait_time)  # Attendre que la page réagisse
                
                # Attendre le chargement de la page
                try:
                    await page.wait_for_load_state('domcontentloaded', timeout=15000)
                except:
                    logger.warning("Timeout lors de l'attente du chargement, continuation...")
                
                # Attendre un peu plus pour que les messages d'erreur/succès apparaissent
                await asyncio.sleep(2)
                
                # Vérifier le résultat
                current_url_after = page.url
                logger.info(f"📍 URL après soumission: {current_url_after}")
                page_text = await page.inner_text('body')
                page_text_lower = page_text.lower()
                
                # Vérifier les indicateurs d'erreur
                for error_indicator in config['error_indicators']:
                    if error_indicator.lower() in page_text_lower:
                        # Vérifier si c'est vraiment une erreur de connexion
                        error_elements = await page.query_selector_all(
                            '.error, .alert-danger, [class*="error"], [id*="error"], [class*="alert"], [class*="message"]'
                        )
                        if error_elements:
                            # Vérifier le texte des éléments d'erreur
                            for error_elem in error_elements:
                                error_text = await error_elem.inner_text()
                                if error_indicator.lower() in error_text.lower():
                                    logger.warning(f"❌ Erreur détectée: {error_text[:100]}")
                                    return {
                                        'success': False,
                                        'message': f'Connexion échouée: identifiants incorrects ou compte invalide',
                                        'details': {
                                            'url': current_url_after,
                                            'error_found': error_indicator,
                                            'error_text': error_text[:200]
                                        }
                                    }
                
                # Vérifier les indicateurs de succès
                for success_indicator in config['success_indicators']:
                    if success_indicator.lower() in page_text_lower:
                        # Vérifier si on est vraiment connecté (pas juste sur une page qui contient le mot)
                        if current_url_after != config['base_url'] or 'login' not in current_url_after.lower():
                            return {
                                'success': True,
                                'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                                'details': {
                                    'url': current_url_after,
                                    'success_indicator': success_indicator
                                }
                            }
                
                # Si on a changé d'URL et qu'on n'est plus sur la page de login, c'est probablement un succès
                if 'login' not in current_url_after.lower() and current_url_after != config['base_url']:
                    return {
                        'success': True,
                        'message': f'Connexion réussie ! Votre compte {config["name"]} est maintenant lié.',
                        'details': {
                            'url': current_url_after,
                            'reason': 'url_changed'
                        }
                    }
                
                # Si on est toujours sur la page de login, c'est probablement un échec
                if 'login' in current_url_after.lower() or current_url_after == config['base_url']:
                    return {
                        'success': False,
                        'message': 'Connexion échouée: identifiants incorrects ou problème de connexion',
                        'details': {
                            'url': current_url_after,
                            'reason': 'still_on_login_page'
                        }
                    }
                
                # Cas indéterminé
                return {
                    'success': False,
                    'message': 'Impossible de déterminer si la connexion a réussi. Veuillez vérifier manuellement.',
                    'details': {
                        'url': current_url_after
                    }
                }
                
            except PlaywrightTimeoutError:
                return {
                    'success': False,
                    'message': 'Timeout: La page a pris trop de temps à répondre',
                    'details': {'url': page.url}
                }
            except Exception as e:
                logger.error(f"Erreur lors du test de connexion: {e}")
                return {
                    'success': False,
                    'message': f'Erreur technique: {str(e)}',
                    'details': {'error': str(e)}
                }
            finally:
                await browser.close()
                
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        return {
            'success': False,
            'message': f'Erreur critique: {str(e)}',
            'details': {'error': str(e)}
        }


def test_connection_sync(bank_id: str, email: str, password: str, timeout: int = 30) -> Dict:
    """
    Version synchrone pour être appelée depuis Flask
    """
    return asyncio.run(test_bank_connection(bank_id, email, password, timeout))


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
