@echo off
REM Lanceur Thouv'Run - Version Graphique
REM Lance le jeu en Pygame sans fenêtre console

cd /d "%~dp0"
python main.py %*
exit /b
