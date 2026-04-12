# LENLU AI+ Styled Terminal Interfaces

## Overview

This project now includes multiple styled terminal interfaces for a better user experience:

1. **Python Terminal Interface** - Rich-based interactive CLI
2. **PowerShell Interface** - Windows PowerShell styled management tool
3. **Batch Launcher** - Quick launch wrapper for Windows

---

## Features

### 🎨 Rich Terminal Interface (`terminal_interface.py`)

**Requirements**: `rich` library (already in requirements.txt)

**Features**:
- Colored output with styled panels
- Interactive menu system
- Progress bars for long-running tasks
- Styled tables for data display
- Module information display
- System status monitoring
- Project dashboard

**Usage**:
```bash
python terminal_interface.py
```

**Or with PowerShell flag**:
```bash
python terminal_interface.py --powershell
```

---

### 🔷 PowerShell Interface (`LENLU_Interface.ps1`)

**Requirements**: PowerShell 5.1+ (Windows built-in)

**Features**:
- Color-coded status messages
- System information display
- Project file structure visualization
- Quick action menu
- Command reference
- Git integration
- Requirement installation
- Python interface launcher

**Usage - Method 1 (Direct)**:
```powershell
& "C:\path\to\LENLU_Interface.ps1"
```

**Usage - Method 2 (Execution Policy)**:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\path\to\LENLU_Interface.ps1"
```

**Usage - Method 3 (From project directory)**:
```powershell
./LENLU_Interface.ps1
```

---

### 🚀 Batch Launcher (`launch_interface.bat`)

**Requirements**: Windows 7+ (built-in)

**Features**:
- Single-click launch
- Automatic environment detection
- Error checking
- PowerShell wrapper

**Usage**:
```batch
launch_interface.bat
```

**Or double-click the file in Windows Explorer**

---

## Features Overview

### Python Terminal Interface

```
┌─ Main Menu ─┐
├─ View Module Information
├─ Quick Commands Reference
├─ System Status
├─ Run Training
├─ Ollama Management
└─ Exit
```

**Available Options**:
1. **View Module Information** - See all project modules
2. **Quick Commands** - Display commonly used commands
3. **System Status** - Check Python path, directories, timestamps
4. **Run Training** - Start AI model training with progress
5. **Ollama Management** - Manage Ollama models
6. **Exit** - Close the interface

### PowerShell Interface

**Menu Options**:
1. View Project Information
2. Show System Status
3. List Available Commands
4. Show File Structure
5. Install Requirements
6. Run Terminal Interface (launches Python interface)
7. Git Status Check
8. Exit

---

## Examples

### Example 1: Launch from Python
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run terminal interface
python terminal_interface.py
```

### Example 2: Launch from PowerShell
```powershell
# From project directory
.\LENLU_Interface.ps1

# Or with explicit execution policy
powershell -ExecutionPolicy Bypass -File LENLU_Interface.ps1
```

### Example 3: Quick launch from batch
```batch
# Double-click launch_interface.bat in Windows Explorer
# Or run from cmd.exe
launch_interface.bat
```

---

## Terminal Output Examples

### Success Message
```
✓ Training completed successfully
```

### Error Message
```
✗ Failed to connect to Ollama service
```

### Info Message
```
ℹ Starting AI+ training...
```

### Warning Message
```
⚠ GPU memory usage approaching limit
```

---

## Styling Elements

### Color Scheme
- **Cyan** - Headers, primary information
- **Yellow** - Menu options, section titles
- **Green** - Success messages, available items
- **Red** - Error messages, warnings
- **Blue** - Info messages, secondary info
- **White** - Main content text

### Visual Elements
- Box drawing characters (╔═╗║╚╝)
- Progress bars (█░░░)
- Checkmarks (✓) and X marks (✗)
- Info symbols (ℹ) and warning symbols (⚠)
- Arrows (► ➜ →)
- Dividers (━ ─)

---

## System Requirements

### For Python Interface:
- Python 3.7+
- `rich` library
- Any terminal that supports ANSI colors

### For PowerShell Interface:
- Windows OS
- PowerShell 5.1+
- No additional dependencies

### For Batch Launcher:
- Windows OS
- PowerShell (should be pre-installed)

---

## Installation & Setup

### Quick Setup

1. **Ensure requirements are installed**:
```bash
pip install -r requirements.txt
```

2. **Activate virtual environment**:
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1

# or CMD
.\.venv\Scripts\activate.bat
```

3. **Run any of the interfaces**:
```bash
# Python Terminal Interface
python terminal_interface.py

# or PowerShell Interface
./LENLU_Interface.ps1

# or Batch Launcher
launch_interface.bat
```

---

## Keyboard Shortcuts

### In Python Interface
- Enter number to select menu option
- Ctrl+C to exit (from most menus)

### In PowerShell Interface
- Enter number to select menu option
- Ctrl+C to exit
- Clear-Host (cls in PowerShell) to clear screen

---

## Troubleshooting

### Python Interface Not Running
```bash
# Install rich library if missing
pip install rich

# Run with verbose output
python -u terminal_interface.py
```

### PowerShell Script Won't Run
```powershell
# Check execution policy
Get-ExecutionPolicy

# Set if needed (requires admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for this run
powershell -ExecutionPolicy Bypass -File LENLU_Interface.ps1
```

### Batch File Not Finding PowerShell
```batch
# Verify PowerShell is in system PATH
where powershell

# If not found, use full path in launch_interface.bat
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

---

## File Descriptions

| File | Type | Purpose |
|------|------|---------|
| `terminal_interface.py` | Python | Rich-based interactive CLI interface |
| `LENLU_Interface.ps1` | PowerShell | Windows PowerShell styled menu system |
| `launch_interface.bat` | Batch | Windows batch launcher wrapper |

---

## Integration with Main Project

These interfaces provide user-friendly access to:
- AI model training
- Ollama integration
- Knowledge base management
- System monitoring
- Git operations
- Requirement installation

They complement the main project files:
- `lenlu_ai_plus.py` - Core AI implementation
- `lenlu_ollama.py` - Ollama integration
- `user_training_system.py` - Training tools

---

## Future Enhancements

Potential additions:
- Web dashboard interface
- Real-time model training visualization
- Advanced logging view
- Configuration editor
- Performance metrics display
- Model comparison tools

---

## Support

For issues or enhancements:
1. Check the troubleshooting section
2. Verify Python/PowerShell versions
3. Ensure all dependencies are installed
4. Check project documentation (OLLAMA_INTEGRATION_GUIDE.md)

---

## License

Part of LENLU AI+ Project
