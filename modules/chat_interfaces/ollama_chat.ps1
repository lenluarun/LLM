# LENLU AI+ Ollama Chat - PowerShell Edition
# Simple terminal interface with conversation logging

param()

$OLLAMA_HOST = "http://localhost:11434"
$CONVERSATION_LOG = "conversation_log.json"
$CurrentModel = "lenlu"
$ChatHistory = @()

# Utility functions
function Write-Success {
    Write-Host "[OK] $_" -ForegroundColor Green
}

function Load-History {
    if (Test-Path $CONVERSATION_LOG) {
        try {
            $Script:ChatHistory = Get-Content $CONVERSATION_LOG | ConvertFrom-Json
        } catch {
            $Script:ChatHistory = @()
        }
    }
}

function Save-History {
    $ChatHistory | ConvertTo-Json -Depth 10 | Set-Content $CONVERSATION_LOG
}

function Add-Entry {
    param([string]$Q, [string]$A, [string]$Model)
    $Script:ChatHistory += @{
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        model = $Model
        user = $Q
        assistant = $A
    }
    Save-History
}

function Check-Ollama {
    try {
        Invoke-RestMethod -Uri "$OLLAMA_HOST/api/tags" -TimeoutSec 5 -ErrorAction SilentlyContinue | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Get-Models {
    try {
        $r = Invoke-RestMethod -Uri "$OLLAMA_HOST/api/tags" -TimeoutSec 5
        return @($r.models | ForEach-Object { $_.name })
    } catch {
        return @()
    }
}

function Query {
    param([string]$P)
    try {
        $b = @{model = $CurrentModel; prompt = $P; stream = $false} | ConvertTo-Json
        $r = Invoke-RestMethod -Uri "$OLLAMA_HOST/api/generate" -Method Post -Body $b -ContentType "application/json" -TimeoutSec 300
        return $r.response
    } catch {
        return $null
    }
}

function Show-Menu {
    Clear-Host
    Write-Host "===================================="
    Write-Host "LENLU AI+ Ollama Chat"
    Write-Host "Model: $CurrentModel"
    Write-Host "===================================="
    Write-Host ""
    Write-Host "1. Ask Question"
    Write-Host "2. Change Model"
    Write-Host "3. View History"
    Write-Host "4. Show Summary"
    Write-Host "5. Export Chat"
    Write-Host "6. Clear History"
    Write-Host "7. Status"
    Write-Host "8. Exit"
    Write-Host ""
}

function Ask-Question {
    Clear-Host
    Write-Host "Ask Ollama" -ForegroundColor Green
    Write-Host "Type 'back' to return"
    Write-Host ""
    $q = Read-Host "Question"
    
    if ($q -eq "back") { return }
    if ([string]::IsNullOrWhiteSpace($q)) { return }
    
    Clear-Host
    Write-Host "You: $q" -ForegroundColor Cyan
    Write-Host ""
    
    $a = Query $q
    if ($a) {
        Write-Host "Assistant:" -ForegroundColor Green
        Write-Host "$a" -ForegroundColor White
        Add-Entry $q $a $CurrentModel
        Write-Host ""
        Write-Host "Chat saved!" -ForegroundColor Green
    }
    
    Read-Host "Press Enter"
}

function Change-Model {
    Clear-Host
    $models = Get-Models
    if ($models.Count -eq 0) {
        Write-Host "No models found" -ForegroundColor Red
        Read-Host "Press Enter"
        return
    }
    
    Write-Host "Available Models:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $models.Count; $i++) {
        Write-Host "$($i+1). $($models[$i])"
    }
    
    $choice = Read-Host "Select (1-$($models.Count))"
    if ($choice -ge 1 -and $choice -le $models.Count) {
        $Script:CurrentModel = $models[$choice - 1]
        Write-Host "Model set to: $CurrentModel" -ForegroundColor Green
    }
    Read-Host "Press Enter"
}

function Show-History {
    Clear-Host
    if ($ChatHistory.Count -eq 0) {
        Write-Host "No conversations" -ForegroundColor Yellow
        Read-Host "Press Enter"
        return
    }
    
    Write-Host "Conversation History" -ForegroundColor Green
    Write-Host ""
    
    for ($i = 0; $i -lt $ChatHistory.Count; $i++) {
        $e = $ChatHistory[$i]
        Write-Host "$($i+1). [$($e.model)] $($e.timestamp)" -ForegroundColor Cyan
        Write-Host "   Q: $(if($e.user.Length -gt 60){ $e.user.Substring(0, 60) + '...' } else { $e.user })"
        Write-Host "   A: $(if($e.assistant.Length -gt 60){ $e.assistant.Substring(0, 60) + '...' } else { $e.assistant })"
        Write-Host ""
    }
    
    Read-Host "Press Enter"
}

function Show-Summary {
    Clear-Host
    if ($ChatHistory.Count -eq 0) {
        Write-Host "No conversations" -ForegroundColor Yellow
        Read-Host "Press Enter"
        return
    }
    
    $models = @($ChatHistory | ForEach-Object { $_.model } | Select-Object -Unique)
    
    Write-Host "Chat Summary" -ForegroundColor Green
    Write-Host "Total: $($ChatHistory.Count)" -ForegroundColor Cyan
    Write-Host "Models: $($models -join ', ')" -ForegroundColor Cyan
    Write-Host ""
    
    $recent = $ChatHistory | Select-Object -Last 5
    Write-Host "Recent:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $recent.Count; $i++) {
        Write-Host "  $($i+1). $($recent[$i].timestamp)" -ForegroundColor White
    }
    
    Read-Host "Press Enter"
}

function Export-Chat {
    Clear-Host
    if ($ChatHistory.Count -eq 0) {
        Write-Host "No chats to export" -ForegroundColor Yellow
        Read-Host "Press Enter"
        return
    }
    
    $name = Read-Host "Filename (no ext)"
    $file = "${name}_export.txt"
    
    $out = @()
    $out += "LENLU AI+ Chat Export"
    $out += "=" * 60
    $out += ""
    
    for ($i = 0; $i -lt $ChatHistory.Count; $i++) {
        $e = $ChatHistory[$i]
        $out += "Chat $($i+1) [$($e.model)] $($e.timestamp)"
        $out += "Q: $($e.user)"
        $out += "A: $($e.assistant)"
        $out += ""
    }
    
    $out | Set-Content $file
    Write-Host "Exported to: $file" -ForegroundColor Green
    Read-Host "Press Enter"
}

function Clear-History {
    Clear-Host
    Write-Host "Clear all conversations?" -ForegroundColor Red
    $confirm = Read-Host "Type YES to confirm"
    
    if ($confirm -eq "YES") {
        $Script:ChatHistory = @()
        Save-History
        Write-Host "Cleared!" -ForegroundColor Green
    }
    Read-Host "Press Enter"
}

function Show-Status {
    Clear-Host
    Write-Host "Ollama Status" -ForegroundColor Green
    Write-Host ""
    
    if (Check-Ollama) {
        Write-Host "Status: RUNNING" -ForegroundColor Green
        Write-Host "Host: $OLLAMA_HOST" -ForegroundColor Cyan
        Write-Host "Model: $CurrentModel" -ForegroundColor Cyan
        $m = Get-Models
        Write-Host "Models: $($m -join ', ')" -ForegroundColor Cyan
    } else {
        Write-Host "Status: STOPPED" -ForegroundColor Red
        Write-Host "Start with: ollama serve" -ForegroundColor Yellow
    }
    
    Read-Host "Press Enter"
}

# Main
Load-History

if (-not (Check-Ollama)) {
    Clear-Host
    Write-Host "ERROR: Ollama not running!" -ForegroundColor Red
    Write-Host "Start with: ollama serve" -ForegroundColor Yellow
    Read-Host "Press Enter"
    exit
}

$running = $true
while ($running) {
    Show-Menu
    $choice = Read-Host "Select (1-8)"
    
    switch ($choice) {
        "1" { Ask-Question }
        "2" { Change-Model }
        "3" { Show-History }
        "4" { Show-Summary }
        "5" { Export-Chat }
        "6" { Clear-History }
        "7" { Show-Status }
        "8" {
            Clear-Host
            Write-Host "Goodbye!" -ForegroundColor Green
            $running = $false
        }
        default {
            Clear-Host
            Write-Host "Invalid choice" -ForegroundColor Red
            Read-Host "Press Enter"
        }
    }
}
