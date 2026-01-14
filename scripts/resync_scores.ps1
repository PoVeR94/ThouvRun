$API_URL = "https://thouvrun-production.up.railway.app/api/scores"
$SCORES_FILE = "$(Split-Path -Parent (Split-Path -Parent $PSCommandPath))\data\thouv_scores.json"

Write-Host "Chargement des scores..."
$scores = Get-Content $SCORES_FILE -Encoding UTF8 | ConvertFrom-Json

Write-Host "Scores trouves: $($scores.Count)"
Write-Host "Envoi vers l'API..."
Write-Host "======================================================================"

$sent = 0
$errors = 0

for ($i = 0; $i -lt $scores.Count; $i++) {
    $score = $scores[$i]
    
    try {
        $body = $score | ConvertTo-Json -Compress
        
        $resp = Invoke-WebRequest -Uri $API_URL `
            -Method Post `
            -Body $body `
            -ContentType "application/json" `
            -TimeoutSec 2 `
            -UseBasicParsing `
            -ErrorAction Stop
        
        if ($resp.StatusCode -in @(200, 201)) {
            $sent++
        } else {
            $errors++
        }
    }
    catch {
        $errors++
    }
    
    if (($i + 1) % 25 -eq 0) {
        Write-Host "Progress: $($i + 1)/$($scores.Count) (OK: $sent, KO: $errors)"
    }
}

Write-Host "======================================================================"
Write-Host "Synchronisation terminee!"
Write-Host "Envoyes: $sent/$($scores.Count)"
Write-Host "Erreurs: $errors"
$pct = if ($scores.Count -gt 0) { [math]::Round(($sent * 100) / $scores.Count, 1) } else { 0 }
Write-Host "Taux reussite: $pct%"
