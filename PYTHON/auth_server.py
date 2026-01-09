#!/usr/bin/env python3
"""
Serveur Flask pour l'authentification
Gère l'inscription, la connexion et la vérification d'email
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
import os
from functools import wraps
import jwt

app = Flask(__name__)
# Configuration CORS pour permettre les requêtes depuis GitHub Pages
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://dedale95.github.io",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "file://"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "users.db"
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration email (à adapter selon votre fournisseur)
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')  # Votre email
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Votre mot de passe ou app password
EMAIL_FROM = os.environ.get('EMAIL_FROM', SMTP_USER)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

def init_db():
    """Initialise la base de données des utilisateurs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email_verified INTEGER DEFAULT 0,
            verification_token TEXT,
            verification_token_expires TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            civility TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            address TEXT,
            postal_code TEXT,
            city TEXT,
            country TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Migration : ajouter les nouvelles colonnes si elles n'existent pas
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN first_name TEXT")
    except sqlite3.OperationalError:
        pass  # La colonne existe déjà
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN last_name TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN phone TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN address TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN postal_code TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN city TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE profiles ADD COLUMN country TEXT")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_verification_token():
    """Génère un token de vérification"""
    return secrets.token_urlsafe(32)

def send_verification_email(email, token):
    """Envoie un email de vérification"""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"⚠️ SMTP non configuré. Token de vérification pour {email}: {token}")
        print(f"   URL de vérification: {BASE_URL}/api/verify?token={token}")
        return False
    
    try:
        verification_url = f"{BASE_URL}/api/verify?token={token}"
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Vérification de votre email - Taleos'
        msg['From'] = EMAIL_FROM
        msg['To'] = email
        
        text = f"""
Bonjour,

Merci de vous être inscrit sur Taleos !

Pour activer votre compte, veuillez cliquer sur le lien suivant :
{verification_url}

Ce lien est valide pendant 24 heures.

Si vous n'avez pas créé de compte sur Taleos, vous pouvez ignorer cet email.

Cordialement,
L'équipe Taleos
        """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Bienvenue sur Taleos !</h2>
        <p>Merci de vous être inscrit sur Taleos.</p>
        <p>Pour activer votre compte, veuillez cliquer sur le bouton ci-dessous :</p>
        <a href="{verification_url}" class="button">Vérifier mon email</a>
        <p>Ou copiez ce lien dans votre navigateur :</p>
        <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
        <p><strong>Ce lien est valide pendant 24 heures.</strong></p>
        <p>Si vous n'avez pas créé de compte sur Taleos, vous pouvez ignorer cet email.</p>
        <div class="footer">
            <p>Cordialement,<br>L'équipe Taleos</p>
        </div>
    </div>
</body>
</html>
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email: {e}")
        return False

def generate_jwt_token(user_id, email):
    """Génère un token JWT pour l'authentification"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@app.route('/api/signup', methods=['POST'])
def signup():
    """Endpoint d'inscription"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not email or '@' not in email:
            return jsonify({'error': 'Adresse email invalide'}), 400
        
        if not password or len(password) < 8:
            return jsonify({'error': 'Le mot de passe doit contenir au moins 8 caractères'}), 400
        
        # Vérifier les critères du mot de passe
        if not any(c.isupper() for c in password):
            return jsonify({'error': 'Le mot de passe doit contenir au moins une majuscule'}), 400
        if not any(c.islower() for c in password):
            return jsonify({'error': 'Le mot de passe doit contenir au moins une minuscule'}), 400
        if not any(c.isdigit() for c in password):
            return jsonify({'error': 'Le mot de passe doit contenir au moins un chiffre'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400
        
        # Créer l'utilisateur
        password_hash = hash_password(password)
        verification_token = generate_verification_token()
        token_expires = datetime.utcnow() + timedelta(hours=24)
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, verification_token, verification_token_expires)
            VALUES (?, ?, ?, ?)
        """, (email, password_hash, verification_token, token_expires))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        # Envoyer l'email de vérification
        send_verification_email(email, verification_token)
        
        return jsonify({
            'message': 'Inscription réussie. Un email de vérification a été envoyé.',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        print(f"❌ Erreur lors de l'inscription: {e}")
        return jsonify({'error': 'Une erreur est survenue lors de l\'inscription'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de connexion"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, email, password_hash, email_verified
            FROM users WHERE email = ?
        """, (email,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        user_id, user_email, password_hash, email_verified = user
        
        # Vérifier le mot de passe
        if hash_password(password) != password_hash:
            conn.close()
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        # Vérifier si l'email est vérifié
        if not email_verified:
            conn.close()
            return jsonify({'error': 'Veuillez vérifier votre email avant de vous connecter. Consultez votre boîte mail.'}), 403
        
        # Mettre à jour la dernière connexion
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.utcnow(), user_id))
        conn.commit()
        conn.close()
        
        # Générer le token JWT
        token = generate_jwt_token(user_id, user_email)
        
        return jsonify({
            'message': 'Connexion réussie',
            'token': token,
            'email': user_email
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la connexion'}), 500

@app.route('/api/verify', methods=['GET'])
def verify_email():
    """Endpoint de vérification d'email"""
    try:
        token = request.args.get('token')
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, email, verification_token_expires
            FROM users WHERE verification_token = ?
        """, (token,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'Token invalide'}), 400
        
        user_id, email, token_expires = user
        
        # Vérifier si le token n'a pas expiré
        if datetime.fromisoformat(token_expires) < datetime.utcnow():
            conn.close()
            return jsonify({'error': 'Le token de vérification a expiré. Veuillez demander un nouveau lien.'}), 400
        
        # Marquer l'email comme vérifié
        cursor.execute("""
            UPDATE users 
            SET email_verified = 1, verification_token = NULL, verification_token_expires = NULL
            WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Email vérifié avec succès ! Vous pouvez maintenant vous connecter.'
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la vérification'}), 500

def verify_token(f):
    """Décorateur pour vérifier le token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Récupérer le token depuis les headers
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Token invalide'}), 401
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        
        try:
            # Décoder le token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user_email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401
        
        return f(current_user_id, current_user_email, *args, **kwargs)
    
    return decorated

@app.route('/api/profile', methods=['GET'])
@verify_token
def get_profile(user_id, user_email):
    """Récupère le profil de l'utilisateur"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT civility, first_name, last_name, phone, address, postal_code, city, country, updated_at
            FROM profiles WHERE user_id = ?
        """, (user_id,))
        
        profile = cursor.fetchone()
        conn.close()
        
        if profile:
            return jsonify({
                'profile': {
                    'civility': profile['civility'],
                    'first_name': profile['first_name'],
                    'last_name': profile['last_name'],
                    'phone': profile['phone'],
                    'address': profile['address'],
                    'postal_code': profile['postal_code'],
                    'city': profile['city'],
                    'country': profile['country'],
                    'updated_at': profile['updated_at']
                }
            }), 200
        else:
            return jsonify({'profile': None}), 200
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        return jsonify({'error': 'Une erreur est survenue'}), 500

@app.route('/api/profile', methods=['POST'])
@verify_token
def save_profile(user_id, user_email):
    """Sauvegarde le profil de l'utilisateur"""
    try:
        data = request.get_json()
        civility = data.get('civility', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        postal_code = data.get('postal_code', '').strip()
        city = data.get('city', '').strip()
        country = data.get('country', '').strip()
        
        # Validation
        if civility and civility not in ['Madame', 'Monsieur', 'Ne souhaite pas se prononcer']:
            return jsonify({'error': 'Civilité invalide'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier si le profil existe déjà
        cursor.execute("SELECT user_id FROM profiles WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Mettre à jour
            cursor.execute("""
                UPDATE profiles 
                SET civility = ?, first_name = ?, last_name = ?, phone = ?, 
                    address = ?, postal_code = ?, city = ?, country = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (civility, first_name, last_name, phone, address, postal_code, city, country, user_id))
        else:
            # Créer
            cursor.execute("""
                INSERT INTO profiles (user_id, civility, first_name, last_name, phone, address, postal_code, city, country)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, civility, first_name, last_name, phone, address, postal_code, city, country))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Profil enregistré avec succès',
            'profile': {
                'civility': civility,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'address': address,
                'postal_code': postal_code,
                'city': city,
                'country': country
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du profil: {e}")
        return jsonify({'error': 'Une erreur est survenue lors de l\'enregistrement'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que le serveur fonctionne"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    print("=" * 80)
    print("🚀 SERVEUR D'AUTHENTIFICATION TALEOS")
    print("=" * 80)
    print(f"📁 Base de données: {DB_PATH}")
    print(f"🌐 URL: {BASE_URL}")
    if SMTP_USER:
        print(f"📧 Email configuré: {SMTP_USER}")
    else:
        print("⚠️  SMTP non configuré - les emails ne seront pas envoyés")
        print("   Configurez SMTP_USER et SMTP_PASSWORD pour activer l'envoi d'emails")
    print("=" * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
