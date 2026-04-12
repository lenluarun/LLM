# LENLU AI+ PowerShell Interface Script
# Enhanced PowerShell interface with styled output

# Color definitions
$ColorHeader = "Cyan"
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Blue"

# Banner
function Show-Banner {
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                   LENLU AI+ PowerShell                     ║" -ForegroundColor Cyan
    Write-Host "║            Advanced Terminal Interface Management           ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host "`n"
}

# Section header
function Write-Section {
    param([string]$Title)
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host ("━" * 70) -ForegroundColor Cyan
    Write-Host "▶ $Title" -ForegroundColor Yellow
    Write-Host ("━" * 70) -ForegroundColor Cyan
    Write-Host "`n"
}

# Status messages
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

# Project information
function Show-ProjectInfo {
    Write-Section "Project Information"
    
    $projects = @(
        @{Name="LENLU AI Plus"; Desc="Advanced AI model training with PyTorch"},
        @{Name="Ollama Integration"; Desc="Seamless Ollama model management"},
        @{Name="Knowledge Base"; Desc="Comprehensive knowledge management"},
        @{Name="User Training System"; Desc="Personalized model training"},
        @{Name="Verification Tools"; Desc="Setup verification utilities"}
    )
    
    foreach ($project in $projects) {
        Write-Host "  ► " -ForegroundColor Cyan -NoNewline
        Write-Host $project.Name -ForegroundColor Yellow
        Write-Host "    $($project.Desc)" -ForegroundColor Gray
    }
}

# System status
function Show-SystemStatus {
    Write-Section "System Status"
    
    $status = @(
        @{Property="PowerShell Version"; Value=$PSVersionTable.PSVersion.ToString()},
        @{Property="OS"; Value=[System.Environment]::OSVersion.VersionString},
        @{Property="Current Directory"; Value=$(Get-Location)},
        @{Property="Python Available"; Value=$((Get-Command python -ErrorAction SilentlyContinue) ? "Yes" : "No")},
        @{Property="Git Available"; Value=$((Get-Command git -ErrorAction SilentlyContinue) ? "Yes" : "No")},
        @{Property="Timestamp"; Value=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")}
    )
    
    foreach ($item in $status) {
        Write-Host ("{0,-25}" -f $item.Property) -ForegroundColor Cyan -NoNewline
        Write-Host " : " -NoNewline
        Write-Host $item.Value -ForegroundColor Yellow
    }
}

# Available commands
function Show-Commands {
    Write-Section "Available Commands"
    
    $commands = @(
        @{Cmd="python lenlu_ai_plus.py"; Desc="Start AI+ training"},
        @{Cmd="python lenlu_ollama.py"; Desc="Run Ollama integration"},
        @{Cmd="python verify_ollama_setup.py"; Desc="Verify Ollama setup"},
        @{Cmd="python setup_ollama.py"; Desc="Setup Ollama automatically"},
        @{Cmd="python terminal_interface.py"; Desc="Launch styled terminal interface"},
        @{Cmd="git pull origin main"; Desc="Update from GitHub"},
        @{Cmd="git push origin main"; Desc="Push changes to GitHub"}
    )
    
    foreach ($cmd in $commands) {
        Write-Host "  " -NoNewline
        Write-Host "$ " -ForegroundColor Green -NoNewline
        Write-Host $cmd.Cmd -ForegroundColor Cyan
        Write-Host "    └─ $($cmd.Desc)" -ForegroundColor Gray
    }
}

# File structure
function Show-FileStructure {
    Write-Section "Project File Structure"
    
    Write-Host "llm/" -ForegroundColor Cyan
    Write-Host "├── Core Modules" -ForegroundColor Yellow
    Write-Host "│   ├── lenlu_ai_plus.py" -ForegroundColor Green
    Write-Host "│   ├── lenlu_ollama.py" -ForegroundColor Green
    Write-Host "│   └── ollama_integration.py" -ForegroundColor Green
    Write-Host "│" -ForegroundColor Gray
    Write-Host "├── Tools & Utilities" -ForegroundColor Yellow
    Write-Host "│   ├── setup_ollama.py" -ForegroundColor Green
    Write-Host "│   ├── verify_ollama_setup.py" -ForegroundColor Green
    Write-Host "│   ├── user_training_system.py" -ForegroundColor Green
    Write-Host "│   └── terminal_interface.py" -ForegroundColor Green
    Write-Host "│" -ForegroundColor Gray
    Write-Host "├── Configuration" -ForegroundColor Yellow
    Write-Host "│   ├── requirements.txt" -ForegroundColor Green
    Write-Host "│   ├── ollama_config.json" -ForegroundColor Green
    Write-Host "│   └── README.md" -ForegroundColor Green
    Write-Host "│" -ForegroundColor Gray
    Write-Host "├── Data Files" -ForegroundColor Yellow
    Write-Host "│   ├── knowledge_base_comprehensive.json" -ForegroundColor Green
    Write-Host "│   ├── training_data_expanded.json" -ForegroundColor Green
    Write-Host "│   ├── user_learned_knowledge.json" -ForegroundColor Green
    Write-Host "│   └── conversation_log.json" -ForegroundColor Green
    Write-Host "│" -ForegroundColor Gray
    Write-Host "├── Documentation" -ForegroundColor Yellow
    Write-Host "│   ├── OLLAMA_INTEGRATION_GUIDE.md" -ForegroundColor Green
    Write-Host "│   ├── OLLAMA_SETUP_COMPLETE.md" -ForegroundColor Green
    Write-Host "│   └── LENLU_AI_PLUS_SUMMARY.md" -ForegroundColor Green
    Write-Host "│" -ForegroundColor Gray
    Write-Host "└── Models" -ForegroundColor Yellow
    Write-Host "    ├── lenlu-manifest.json" -ForegroundColor Green
    Write-Host "    ├── lenlu-params.json" -ForegroundColor Green
    Write-Host "    └── cache/" -ForegroundColor Green
}

# Quick actions menu
function Show-QuickActions {
    Write-Section "Quick Actions"
    
    $actions = @(
        "1. View Project Information",
        "2. Show System Status",
        "3. List Available Commands",
        "4. Show File Structure",
        "5. Install Requirements",
        "6. Run Terminal Interface",
        "7. Update from GitHub",
        "8. Exit"
    )
    
    $actions | ForEach-Object { Write-Host "  $_" -ForegroundColor Cyan }
}

# Execute Python terminal interface
function Invoke-TerminalInterface {
    Write-Info "Launching styled terminal interface..."
    & python terminal_interface.py
}

# Install requirements
function Install-Requirements {
    Write-Section "Installing Requirements"
    
    if (Test-Path "requirements.txt") {
        Write-Info "Installing packages from requirements.txt..."
        & pip install -r requirements.txt
        Write-Success "Installation completed!"
    } else {
        Write-Error-Custom "requirements.txt not found!"
    }
}

# Update from GitHub
function Update-FromGitHub {
    Write-Section "Update from GitHub"
    
    if (Test-Path ".git") {
        Write-Info "Pulling latest changes from origin..."
        & git pull origin main
        Write-Success "Update completed successfully!"
    } else {
        Write-Error-Custom "Git repository not initialized!"
    }
}

# Main menu loop
function Show-MainMenu {
    do {
        Clear-Host
        Show-Banner
        
        Write-Host "Welcome to LENLU LLM (emu) - PowerShell Interface" -ForegroundColor Cyan
        Write-Host "==========================================" -ForegroundColor Cyan
        
        Show-SystemStatus
        Show-QuickActions
        
        Write-Host "`n"
        $choice = Read-Host "Enter your choice (1-8)"
        
        switch ($choice) {
            "1" { 
                Clear-Host
                Show-Banner
                Show-ProjectInfo
                Read-Host "Press Enter to continue"
            }
            "2" { 
                Clear-Host
                Show-Banner
                Show-SystemStatus
                Read-Host "Press Enter to continue"
            }
            "3" { 
                Clear-Host
                Show-Banner
                Show-Commands
                Read-Host "Press Enter to continue"
            }
            "4" { 
                Clear-Host
                Show-Banner
                Show-FileStructure
                Read-Host "Press Enter to continue"
            }
            "5" { 
                Clear-Host
                Show-Banner
                Install-Requirements
                Read-Host "Press Enter to continue"
            }
            "6" { 
                Invoke-TerminalInterface
            }
            "7" { 
                Clear-Host
                Show-Banner
                Update-FromGitHub
                Read-Host "Press Enter to continue"
            }
            "8" { 
                Write-Success "Thank you for using LENLU AI+!"
                exit
            }
            default { 
                Write-Error-Custom "Invalid choice. Please try again."
                Start-Sleep -Seconds 2
            }
        }
    } while ($true)
}

# Entry point
Show-MainMenu
