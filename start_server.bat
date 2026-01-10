@echo off
REM Script Windows pour démarrer un serveur HTTP local

echo 🚀 Démarrage du serveur HTTP local...
echo.
echo 📁 Dossier : HTML/
echo 🌐 URL : http://localhost:8000/offres.html
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

cd HTML
python -m http.server 8000
