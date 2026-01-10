#!/bin/bash
# Script pour démarrer un serveur HTTP local pour tester le site

echo "🚀 Démarrage du serveur HTTP local..."
echo ""
echo "📁 Dossier : HTML/"
echo "🌐 URL : http://localhost:8000/offres.html"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

cd "$(dirname "$0")/HTML" || exit 1
python3 -m http.server 8000
