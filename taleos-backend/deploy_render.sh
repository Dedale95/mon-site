#!/bin/bash
# Script pour déployer sur Render.com via l'API
# Usage: ./deploy_render.sh

# Configuration
RENDER_API_KEY="rnd_ZG9AMLoiaXln0KtAlhElCQLrqnAL"
SERVICE_NAME="taleos-connection-tester"
REGION="frankfurt"
REPO_URL="https://github.com/Dedale95/mon-site.git"  # À adapter selon votre repo

echo "🚀 Déploiement sur Render.com..."

# Vérifier que curl est installé
if ! command -v curl &> /dev/null; then
    echo "❌ curl n'est pas installé. Installez-le d'abord."
    exit 1
fi

# Vérifier que jq est installé (pour parser JSON)
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq n'est pas installé. Installation recommandée pour parser les réponses JSON."
    echo "   Installer avec: brew install jq (sur macOS)"
    JQ_AVAILABLE=false
else
    JQ_AVAILABLE=true
fi

echo "📋 Étape 1: Vérification de l'API key..."
# Test de l'API key
response=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" https://api.render.com/v1/owners)
if echo "$response" | grep -q "unauthorized\|Unauthorized"; then
    echo "❌ API key invalide ou non autorisée"
    exit 1
fi
echo "✅ API key valide"

echo ""
echo "⚠️  IMPORTANT: Le déploiement via API nécessite plusieurs étapes complexes."
echo "   Il est plus simple d'utiliser l'interface web de Render.com:"
echo ""
echo "   1. Aller sur https://dashboard.render.com"
echo "   2. Cliquer sur 'New +' → 'Web Service'"
echo "   3. Connecter votre repo GitHub"
echo "   4. Render détectera automatiquement render.yaml"
echo "   5. Cliquer sur 'Create Web Service'"
echo ""
echo "📚 Pour utiliser l'API directement, consultez la documentation:"
echo "   https://render.com/docs/api"
echo ""
echo "✅ Tous les fichiers sont prêts pour le déploiement manuel !"
