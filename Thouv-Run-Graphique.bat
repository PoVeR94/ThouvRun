@echo off
REM ========================================
REM Thouv'Run - Jeu Graphique (Pygame)
REM ========================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Verifier que les dependances sont installees
python -c "import pygame, requests, flask" >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] Les dependances ne sont pas installees
    echo.
    echo Lancement du SETUP...
    echo.
    call SETUP.bat
    if errorlevel 1 (
        echo Installation echouee. Impossible de demarrer le jeu.
        pause
        exit /b 1
    )
)

REM Lancer le jeu graphique
python src/main_graphique.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le jeu n'a pas pu demarrer
    echo.
    pause
)
