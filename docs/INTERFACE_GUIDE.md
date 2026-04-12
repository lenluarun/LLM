# LENLU AI+ Complete Interface Guide

## Overview

LENLU AI+ now offers **FOUR different interfaces** for interacting with Ollama:

1. **🌐 Web GUI** - Beautiful localhost web interface
2. **💻 Terminal CLI** - Rich-styled Python terminal interface
3. **🔷 PowerShell CLI** - Windows PowerShell interface
4. **⚡ Quick Chat** - Simple Python Ollama chat

---

## Quick Start

### Method 1: Unified Launcher (Recommended)
```bash
python launcher.py
```

Select your preferred interface from the menu:
- Option 1: Web GUI (http://localhost:5000)
- Option 2: Terminal CLI
- Option 3: PowerShell CLI
- Option 4: Quick Chat

### Method 2: Direct Launch

**Web GUI:**
```bash
python app.py
```

**Terminal CLI:**
```bash
python terminal_interface.py
```

**PowerShell CLI:**
```powershell
powershell -ExecutionPolicy Bypass -File ollama_chat.ps1
```

**Quick Chat:**
```bash
python ollama_chat_interface.py
```

---

## Interface Details

### 1. 🌐 Web GUI (Flask Application)

**File:** `app.py`  
**Port:** http://localhost:5000  
**Features:**
- Beautiful gradient UI
- Real-time chat with Ollama
- Conversation history with persistence
- Model switching
- Export conversations to JSON
- Statistics dashboard
- Responsive design
- Session management

**How to Use:**
1. Start the launcher and select option 1
2. Or run: `python app.py`
3. Open browser to `http://localhost:5000`
4. Select a model from dropdown
5. Type your message and press Send
6. View history, export, or start new session

**Features:**
- ✓ Auto-saves all conversations
- ✓ Multiple concurrent sessions
- ✓ Model selection
- ✓ Chat history viewer
- ✓ JSON export
- ✓ Statistics display
- ✓ Responsive mobile UI

---

### 2. 💻 Terminal CLI (Rich)

**File:** `terminal_interface.py`  
**Features:**
- Rich color styling
- Interactive menu system
- Progress bars
- Formatted tables
- Module information
- Status monitoring

**Commands:**
1. View Module Information
2. Quick Commands Reference
3. System Status
4. Run Training
5. Ollama Management
6. Exit

---

### 3. 🔷 PowerShell CLI

**File:** `ollama_chat.ps1`  
**Features:**
- Color-coded terminal output
- Interactive 8-item menu
- Conversation logging
- Model switching
- History export
- Box-drawing UI

**Menu Options:**
1. Ask Question
2. Change Model
3. View History
4. Show Summary
5. Export Chat
6. Clear History
7. Status
8. Exit

---

### 4. ⚡ Quick Chat

**File:** `ollama_chat_interface.py`  
**Features:**
- Simple Python CLI
- Terminal clearing between commands
- JSON conversation logging
- Malleable interface

---

## System Requirements

### For Web GUI
- Python 3.7+
- Flask (`pip install flask`)
- Flask-CORS (`pip install flask-cors`)
- Requests (`pip install requests`)
- Ollama running (`ollama serve`)

### For Terminal CLI
- Python 3.7+
- Rich library (in requirements.txt)
- Ollama running

### For PowerShell CLI
- Windows OS
- PowerShell 5.1+
- Ollama running

### For Quick Chat
- Python 3.7+
- Requests library
- Ollama running

---

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Ollama (in another terminal)
```bash
ollama serve
```

### Step 3: Launch Interface
```bash
python launcher.py
```

---

## Web GUI Details

### UI Components

**Sidebar:**
- Model selector dropdown
- Ollama status indicator
- Action buttons (New Session, History, Export)
- Statistics cards
- Danger zone (Clear History)

**Main Content:**
- Header with title and refresh button
- Chat area with messages
- Input area with typing support
- Auto-scrolling to latest message

**Features:**
- Auto-resize textarea
- Send on Enter (Shift+Enter for newline)
- Real-time status checking
- Conversation persistence
- Session management
- HTML export ready

### API Endpoints

```
GET  /                    - Serve web interface
GET  /api/status          - Check Ollama status
POST /api/chat            - Send message to Ollama
GET  /api/history         - Get all conversations
GET  /api/history/<id>    - Get session history
GET  /api/summary         - Get statistics
GET  /api/export          - Export conversations
POST /api/clear-history   - Clear history (confirmation required)
```

---

## Data Persistence

### Conversation Storage
All conversations are automatically saved to:
```
conversation_log.json
```

**Structure:**
```json
{
  "timestamp": "2024-04-12T10:30:45",
  "model": "lenlu",
  "session_id": "session_xxxx",
  "user": "Your question",
  "assistant": "Assistant response"
}
```

---

## Keyboard Shortcuts

### Web GUI
- **Send:** Click button or use send button
- **New Line:** Shift + Enter in textarea
- **Tab Management:** Use browser tabs for multiple sessions

### Terminal CLI
- **Menu Selection:** Type number and Enter
- **Exit:** Type 'quit' or use Ctrl+C
- **Back:** Type 'back' from prompts

### PowerShell CLI
- **Menu Selection:** Type number and Enter
- **Exit:** Select option 8
- **Cancel:** Press Ctrl+C

---

## Troubleshooting

### Web GUI Not Loading
```bash
# Install missing dependencies
pip install flask flask-cors

# Check if Ollama is running
# Should see: http://localhost:11434/api/tags returns 200

# Try restarting
python app.py
```

### Terminal Interface Errors
```bash
# Make sure Rich is installed
pip install rich

# Check Python version (3.7+)
python --version

# Run with verbosity
python -u terminal_interface.py
```

### PowerShell Script Won't Run
```powershell
# Check execution policy
Get-ExecutionPolicy

# Bypass for current session
powershell -ExecutionPolicy Bypass -File ollama_chat.ps1

# Or set permanently (requires admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Ollama Connection Issues
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags

# Check firewall if on network
# Ollama default port: 11434
```

---

## Performance Tips

1. **Web GUI:** Use modern browser (Chrome, Firefox, Edge)
2. **Terminal:** Larger terminal window for better layout
3. **PowerShell:** Windows 10/11 recommended
4. **General:** Keep Ollama model in memory (don't unload)

---

## Advanced Usage

### Custom Ollama Host
Set environment variable before launching:
```bash
# Linux/Mac
export OLLAMA_HOST="http://192.168.1.100:11434"

# Windows
set OLLAMA_HOST=http://192.168.1.100:11434
```

### Export Conversations
**Web GUI:** Click "Export Chat" button
**Terminal:** Select export option from menu
**PowerShell:** Select option 5 for "Export Chat"

### Clear History
**Warning:** This permanently deletes all conversations!

**Web GUI:** Click "Clear All History" in sidebar
**Terminal:** Select "Clear History" from menu
**PowerShell:** Select option 6

---

## File Structure

```
llm/
├── app.py                          # Flask application
├── launcher.py                     # Unified launcher
├── terminal_interface.py           # Terminal CLI
├── ollama_chat_interface.py        # Quick chat CLI
├── ollama_chat.ps1                 # PowerShell CLI
├── requirements.txt                # Python dependencies
├── conversation_log.json           # Chat history (auto-generated)
├── templates/
│   └── index.html                  # Web UI template
└── uploads/                        # Export directory
```

---

## Security Notes

- ✓ All functionality local only
- ✓ No data sent externally
- ✓ Conversation data stored locally
- ✓ No authentication required (local only)
- ✓ SSL not needed for localhost

---

## Performance Metrics

- **Web GUI Load Time:** < 1 second
- **Chat Response Time:** Depends on Ollama model
- **History Load:** Instant (unless > 10K messages)
- **Export Time:** < 1 second

---

## Support & Troubleshooting

### Common Issues

**"Ollama is not running"**
- Solution: Run `ollama serve` in another terminal

**"Flask not found"**
- Solution: Run `pip install flask flask-cors`

**"Model not showing"**
- Solution: Wait for Ollama to initialize or pull model with `ollama pull modelname`

**"Port 5000 already in use"**
- Solution: Kill existing Flask process or change port in app.py

---

## Credits

**LENLU AI+** - Powered by @lenlu_arun & @lenluarun

Built with:
- Flask (Web framework)
- Rich (Terminal styling)
- Ollama (AI Models)
- PyTorch (ML Framework)

---

## License

Same as LENLU AI+ Project

---

## Next Steps

1. Choose your preferred interface
2. Start Ollama service
3. Run the launcher
4. Enjoy chatting with AI!

```bash
# Quick start
ollama serve &  # Start Ollama in background
python launcher.py  # Launch interface chooser
```

---

**Enjoy using LENLU AI+! 🚀**
