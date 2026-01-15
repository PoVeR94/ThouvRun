@echo off
REM ========================================
REM Script de génération documentation
REM Thouv'Run - LaTeX + PlantUML
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   DOCUMENTATION - Thouv'Run
echo ========================================
echo.

echo [1] Générer PDF depuis LaTeX (nécessite pdflatex)
echo [2] Ouvrir document LaTeX dans l'éditeur
echo [3] Ouvrir guide de génération
echo [4] Vérifier fichiers PlantUML
echo [5] Quitter
echo.

set /p choix="Choisir une option (1-5): "

if "%choix%"=="1" (
    echo.
    echo [*] Vérification de pdflatex...
    pdflatex --version >nul 2>&1
    
    if errorlevel 1 (
        echo.
        echo [ERREUR] pdflatex n'est pas installé
        echo.
        echo Solution 1 : Installer MiKTeX (https://miktex.org/download)
        echo Solution 2 : Utiliser Overleaf (https://www.overleaf.com/)
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] pdflatex trouvé
    echo.
    echo [*] Compilation du fichier LaTeX...
    pdflatex -interaction=nonstopmode Thouv-Run_Report.tex
    
    if exist Thouv-Run_Report.pdf (
        echo.
        echo [OK] PDF généré avec succès : Thouv-Run_Report.pdf
        echo [*] Ouverture du fichier...
        start Thouv-Run_Report.pdf
    ) else (
        echo.
        echo [ERREUR] Échec de la génération du PDF
    )
    
    pause
    goto :menu
)

if "%choix%"=="2" (
    echo.
    echo [*] Ouverture du fichier LaTeX...
    start notepad Thouv-Run_Report.tex
    goto :menu
)

if "%choix%"=="3" (
    echo.
    echo [*] Affichage du guide...
    type DOCUMENTATION_GENERATION.md
    pause
    goto :menu
)

if "%choix%"=="4" (
    echo.
    echo [*] Vérification des fichiers PlantUML...
    
    if exist Thouv-Run_ClassDiagram.puml (
        echo [OK] Diagramme de classes trouvé
    ) else (
        echo [!] Diagramme de classes manquant
    )
    
    if exist Thouv-Run_SequenceDiagram.puml (
        echo [OK] Diagramme de séquence trouvé
    ) else (
        echo [!] Diagramme de séquence manquant
    )
    
    echo.
    echo Pour générer les images :
    echo 1. Allez sur https://www.plantuml.com/plantuml/uml/
    echo 2. Collez le contenu des fichiers .puml
    echo 3. Exportez en PNG/SVG
    echo.
    pause
    goto :menu
)

if "%choix%"=="5" (
    exit /b 0
)

echo.
echo [ERREUR] Choix invalide
echo.
goto :menu

:menu
cls
goto :debut
