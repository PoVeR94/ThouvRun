@echo off
REM ========================================
REM Synchronise les scores avec le serveur AVANT de faire git push
REM ========================================

cls
echo.
echo ========================================
echo SYNCHRONISATION PRE-PUSH
echo ========================================
echo.

echo [*] Synchronisation des scores avec le serveur...
echo (Cela va telecharger les derniers scores depuis Railway)
echo.

python src/gestion_scores.py

echo.
echo [OK] Synchronisation terminee!
echo.
echo Les scores sont maintenant a jour localement.
echo Maintenant tu peux faire:
echo   git add thouv_scores.json
echo   git commit -m "Update scores"
echo   git push
echo.
pause
