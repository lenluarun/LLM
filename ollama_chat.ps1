# LENLU AI+ Ollama Chat PowerShell Interface
# Styled chat interface with terminal clearing and persistent logging

# Configuration
$OLLAMA_HOST = "http://localhost:11434"
$CONVERSATION_LOG = "conversation_log.json"
$CurrentModel = "lenlu"
$ChatHistory = @()

# Color definitions
$Colors = @{
    Header = "Cyan"
    Success = "Green"
    Error = "Red"
    Warning = "Yellow"
    Info = "Blue"
    Accent = "Magenta"
}

# ===================== UTILITY FUNCTIONS =====================

function Write-ClearHeader {
    param([string]$Title = "LENLU AI+ Ollama Chat")
    Clear-Host
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  $($Title.PadRight(60))║" -ForegroundColor Cyan
    Write-Host "║  Model: $($CurrentModel.PadRight(53))║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host "`n"
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# ===================== HISTORY MANAGEMENT =====================

function Load-ConversationHistory {
    if (Test-Path $CONVERSATION_LOG) {
        try {
            $Script:ChatHistory = Get-Content $CONVERSATION_LOG | ConvertFrom-Json
        } catch {
            Write-Warning-Custom "Could not load conversation history"
            $Script:ChatHistory = @()
        }
    } else {
        $Script:ChatHistory = @()
    }
}

function Save-ConversationHistory {
    try {
        $ChatHistory | ConvertTo-Json -Depth 10 | Set-Content $CONVERSATION_LOG
        Write-Success "Conversation saved"
    } catch {
        Write-Error-Custom "Failed to save conversation"
    }
}

function Add-ToHistory {
    param(
        [string]$UserInput,
        [string]$Response,
        [string]$Model
    )
    
    $Entry = @{
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        model = $Model
        user = $UserInput
        assistant = $Response
    }
    
    $Script:ChatHistory += $Entry
    Save-ConversationHistory
}

# ===================== OLLAMA OPERATIONS =====================

function Check-OllamaRunning {
    try {
        $response = Invoke-RestMethod -Uri "$OLLAMA_HOST/api/tags" -TimeoutSec 5 -ErrorAction SilentlyContinue
        return $null -ne $response
    } catch {
        return $false
    }
}

function Get-OllamaModels {
    try {
        $response = Invoke-RestMethod -Uri "$OLLAMA_HOST/api/tags" -TimeoutSec 5
        return @($response.models | ForEach-Object { $_.name })
    } catch {
        return @()
    }
}

function Query-Ollama {
    param([string]$Prompt)
    
    try {
        Write-Info "Querying Ollama..."
        
        $Body = @{
            model = $CurrentModel
            prompt = $Prompt
            stream = $false
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$OLLAMA_HOST/api/generate" `
                                      -Method Post `
                                      -Body $Body `
                                      -ContentType "application/json" `
                                      -TimeoutSec 300
        
        return $response.response
    } catch {
        Write-Error-Custom "Failed to query Ollama: $_"
        return $null
    }
}

# ===================== INTERACTIVE FUNCTIONS =====================

function Show-CommandMenu {
    Write-ClearHeader
    Write-Host "╭─ Commands ─────────────────────────────────────────────────╮" -ForegroundColor Cyan
    Write-Host "│                                                            │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "ask" -ForegroundColor Green -NoNewline
    Write-Host "       - Ask Ollama a question                     │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "model" -ForegroundColor Green -NoNewline
    Write-Host "     - Change Ollama model                         │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "history" -ForegroundColor Green -NoNewline
    Write-Host "    - View conversation history                  │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "summary" -ForegroundColor Green -NoNewline
    Write-Host "    - View conversation summary                  │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "export" -ForegroundColor Green -NoNewline
    Write-Host "    - Export conversations to file               │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "clear" -ForegroundColor Green -NoNewline
    Write-Host "     - Clear conversation history (permanent)    │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "status" -ForegroundColor Green -NoNewline
    Write-Host "    - Check Ollama status                        │" -ForegroundColor Cyan
    Write-Host "│  " -NoNewline -ForegroundColor Cyan
    Write-Host "quit" -ForegroundColor Green -NoNewline
    Write-Host "      - Exit the chat                             │" -ForegroundColor Cyan
    Write-Host "│                                                            │" -ForegroundColor Cyan
    Write-Host "╰────────────────────────────────────────────────────────────╯" -ForegroundColor Cyan
    Write-Host "`n"
}

function Invoke-AskCommand {
    Write-ClearHeader
    Write-Host "[Enter your question or type 'back' to return]" -ForegroundColor Yellow
    Write-Host "`n"
    
    $userInput = Read-Host "Question"
    
    if ($userInput -eq "back") {
        return
    }
    
    if ([string]::IsNullOrWhiteSpace($userInput)) {
        Write-Warning-Custom "Empty question!"
        Read-Host "Press Enter to continue"
        return
    }
    
    Write-ClearHeader
    Write-Host "[bold cyan]You:[/]" -ForegroundColor Cyan
    Write-Host "$userInput`n" -ForegroundColor White
    
    $response = Query-Ollama $userInput
    
    if ($null -ne $response) {
        Write-Host "Assistant:" -ForegroundColor Green
        Write-Host "$response`n" -ForegroundColor Cyan
        
        Add-ToHistory $userInput $response $CurrentModel
        Write-Success "Response saved to history"
    } else {
        Write-Error-Custom "No response from model"
    }
    
    Read-Host "Press Enter to continue"
}

function Invoke-ModelSelection {
    Write-ClearHeader "Select Model"
    
    $models = Get-OllamaModels
    
    if ($models.Count -eq 0) {
        Write-Warning-Custom "No models available!"
        Read-Host "Press Enter to continue"
        return
    }
    
    Write-Host "Available Models:`n" -ForegroundColor Yellow
    for ($i = 0; $i -lt $models.Count; $i++) {
        $marker = if ($models[$i] -eq $CurrentModel) { "✓" } else { " " }
        Write-Host "  [$marker] $($i+1). $($models[$i])" -ForegroundColor Cyan
    }
    
    Write-Host "`n"
    $choice = Read-Host "Select model (1-$($models.Count))"
    
    if ($choice -ge 1 -and $choice -le $models.Count) {
        $Script:CurrentModel = $models[$choice - 1]
        Write-Success "Model changed to: $CurrentModel"
    } else {
        Write-Warning-Custom "Invalid choice"
    }
    
    Read-Host "Press Enter to continue"
}

function Show-ConversationHistory {
    Write-ClearHeader "Conversation History"
    
    if ($ChatHistory.Count -eq 0) {
        Write-Warning-Custom "No conversations yet!"
        Read-Host "Press Enter to continue"
        return
    }
    
    for ($i = 0; $i -lt $ChatHistory.Count; $i++) {
        $entry = $ChatHistory[$i]
        Write-Host "╭─ Conversation $($i+1) ──────────────────────────────────╮" -ForegroundColor Cyan
        Write-Host "│ Timestamp: $($entry.timestamp) │" -ForegroundColor Blue
        Write-Host "│ Model: $($entry.model)" -ForegroundColor Blue
        Write-Host "├────────────────────────────────────────────────────────┤" -ForegroundColor Cyan
        Write-Host "Q: $($entry.user)" -ForegroundColor Yellow
        Write-Host "`nA: $($entry.assistant.Substring(0, [Math]::Min(200, $entry.assistant.Length)))..." -ForegroundColor Green
        Write-Host "╰────────────────────────────────────────────────────────╯`n" -ForegroundColor Cyan
    }
    
    Read-Host "Press Enter to continue"
}

function Show-ConversationSummary {
    Write-ClearHeader "Conversation Summary"
    
    if ($ChatHistory.Count -eq 0) {
        Write-Warning-Custom "No conversations yet!"
        Read-Host "Press Enter to continue"
        return
    }
    
    $modelsUsed = @($ChatHistory | ForEach-Object { $_.model } | Select-Object -Unique)
    
    Write-Host "Total Conversations: " -NoNewline -ForegroundColor Cyan
    Write-Host "$($ChatHistory.Count)" -ForegroundColor Yellow
    
    Write-Host "Models Used: " -NoNewline -ForegroundColor Cyan
    Write-Host ($modelsUsed -join ", ") -ForegroundColor Yellow
    
    Write-Host "`nRecent Conversations:`n" -ForegroundColor Yellow
    
    $recent = $ChatHistory | Select-Object -Last 10
    for ($i = 0; $i -lt $recent.Count; $i++) {
        $entry = $recent[$i]
        $userPreview = if ($entry.user.Length -gt 50) { $entry.user.Substring(0, 50) + "..." } else { $entry.user }
        Write-Host "  [$($i+1)] [$($entry.model)] $($entry.timestamp)" -ForegroundColor Cyan
        Write-Host "      Q: $userPreview" -ForegroundColor White
    }
    
    Read-Host "`nPress Enter to continue"
}

function Export-Conversations {
    Write-ClearHeader "Export Conversations"
    
    if ($ChatHistory.Count -eq 0) {
        Write-Warning-Custom "No conversations to export!"
        Read-Host "Press Enter to continue"
        return
    }
    
    $filename = Read-Host "Enter export filename (without extension)"
    $fullPath = "$filename`_export.txt"
    
    try {
        $content = @()
        $content += "=" * 80
        $content += "LENLU AI+ Ollama Chat Export"
        $content += "=" * 80
        $content += ""
        
        for ($i = 0; $i -lt $ChatHistory.Count; $i++) {
            $entry = $ChatHistory[$i]
            $content += "Conversation $($i+1)"
            $content += "Timestamp: $($entry.timestamp)"
            $content += "Model: $($entry.model)"
            $content += "-" * 80
            $content += "Question:"
            $content += $entry.user
            $content += "`nAnswer:"
            $content += $entry.assistant
            $content += "=" * 80
            $content += ""
        }
        
        $content | Set-Content $fullPath
        Write-Success "Exported to $fullPath"
    } catch {
        Write-Error-Custom "Export failed: $_"
    }
    
    Read-Host "Press Enter to continue"
}

function Clear-ConversationHistory {
    Write-ClearHeader "Clear History"
    
    Write-Warning-Custom "WARNING: This will delete all conversation history!"
    $confirm = Read-Host "Type 'YES' to confirm"
    
    if ($confirm -eq "YES") {
        $Script:ChatHistory = @()
        Save-ConversationHistory
        Write-Success "Conversation history cleared"
    } else {
        Write-Info "Cancelled"
    }
    
    Read-Host "Press Enter to continue"
}

function Show-OllamaStatus {
    Write-ClearHeader "Ollama Status"
    
    if (Check-OllamaRunning) {
        Write-Success "Ollama is running"
        Write-Info "Host: $OLLAMA_HOST"
        Write-Info "Current Model: $CurrentModel"
        
        $models = Get-OllamaModels
        Write-Info "Available Models: $($models -join ', ')"
    } else {
        Write-Error-Custom "Ollama is not running!"
        Write-Warning-Custom "Please start Ollama before using this interface"
        Write-Host "`nTo start Ollama:" -ForegroundColor Cyan
        Write-Host "  Windows/Linux/Mac: ollama serve" -ForegroundColor Green
    }
    
    Read-Host "`nPress Enter to continue"
}

# ===================== MAIN LOOP =====================

function Start-ChatInterface {
    Load-ConversationHistory
    
    # Check Ollama status
    if (-not (Check-OllamaRunning)) {
        Write-ClearHeader
        Write-Error-Custom "Ollama is not running!"
        Write-Warning-Custom "Please start Ollama before using this interface"
        Write-Host "`nTo start Ollama:" -ForegroundColor Cyan
        Write-Host "  ollama serve" -ForegroundColor Green
        Read-Host "`nPress Enter to exit"
        return
    }
    
    Write-ClearHeader
    Write-Success "Ollama is connected!"
    Write-Info "Loading interface..."
    Start-Sleep -Seconds 1
    
    # Main loop
    $running = $true
    while ($running) {
        Show-CommandMenu
        
        $command = Read-Host "Enter command"
        
        switch ($command.ToLower()) {
            "ask" {
                Invoke-AskCommand
            }
            "model" {
                Invoke-ModelSelection
            }
            "history" {
                Show-ConversationHistory
            }
            "summary" {
                Show-ConversationSummary
            }
            "export" {
                Export-Conversations
            }
            "clear" {
                Clear-ConversationHistory
            }
            "status" {
                Show-OllamaStatus
            }
            "quit" {
                Write-ClearHeader
                Write-Success "Thank you for using LENLU AI+ Ollama Chat!"
                Write-Info "Conversations saved to $CONVERSATION_LOG"
                $running = $false
            }
            default {
                Write-ClearHeader
                Write-Error-Custom "Unknown command: $command"
                Read-Host "Press Enter to continue"
            }
        }
    }
}

# Entry point
Start-ChatInterface
