# LENLU LLM (emu) - Project Structure Guide

**Version 2.0.0** - Modular Architecture with Menu-Driven Launcher

## 📁 Directory Structure

```
c:\Users\arune\OneDrive\Documents\github files\llm\
│
├── launcher.py                          # ⭐ MAIN ENTRY POINT (Root Level Only)
├── requirements.txt                     # Python dependencies
├── README.md                            # Original project documentation
│
├── modules/                             # All functionality organized here
│   ├── __init__.py                      # Module package marker
│   │
│   ├── web_gui/                         # 💻 Flask Web Interface
│   │   ├── __init__.py
│   │   ├── app.py                       # Flask server (PORT 5000)
│   │   ├── templates/
│   │   │   └── index.html               # Modern web UI
│   │   └── static/                      # CSS, JS (if needed)
│   │
│   ├── terminal_ui/                     # 🖥️ Rich Terminal Interface
│   │   ├── __init__.py
│   │   └── terminal_interface.py        # Rich-styled terminal UI
│   │
│   ├── chat_interfaces/                 # 💬 CLI Chat Options
│   │   ├── __init__.py
│   │   ├── ollama_chat_interface.py     # Python CLI chat
│   │   └── ollama_chat.ps1              # PowerShell chat
│   │
│   └── utils/                           # 🧠 Advanced LLM & Tools
│       ├── __init__.py
│       ├── lenlu_ai_plus.py             # Advanced AI assistant
│       ├── ollama_integration.py        # Ollama integration
│       ├── lenlu_ollama.py              # Ollama utilities
│       ├── setup_ollama.py              # Installation helper
│       ├── verify_ollama_setup.py       # Verification tool
│       └── user_training_system.py      # Learning system
│
├── config/                              # 📋 Configuration & Data
│   ├── conversation_log.json            # Chat history (auto-created)
│   ├── knowledge_base_comprehensive.json # AI knowledge base
│   ├── training_data_expanded.json      # Training data
│   ├── user_learned_knowledge.json      # Learned user info
│   └── ollama_config.json               # Ollama configuration
│
├── uploads/                             # 📤 Export Files
│   └── (PDF exports, JSON exports)
│
├── models/                              # 🤖 Model Files (if local)
│   ├── lenlu-manifest.json
│   ├── lenlu-params.json
│   ├── cache/
│   └── ollama_models/
│
└── templates/                           # Legacy templates (deprecated)


```

## 🚀 How to Use

### Quick Start
1. Open PowerShell or Terminal
2. Navigate to project directory:
   ```powershell
   cd "c:\Users\arune\OneDrive\Documents\github files\llm"
   ```
3. Run launcher:
   ```powershell
   python launcher.py
   ```
4. Choose your interface using numeric menu (0-9)

### Menu Options

#### Main Interfaces
- **[1]** 💻 **Web GUI** - Beautiful browser-based chat interface
  - Opens http://localhost:5000
  - Modern UI with image upload, code copy, PDF export
  
- **[2]** 🖥️ **Terminal UI** - Rich-styled terminal interface
  - Full-featured terminal chat with formatting
  
- **[3]** 💬 **Chat CLI** - Simple command-line chat
  - Quick terminal chat interface
  
- **[4]** 🧠 **Advanced LLM** - Full-featured AI assistant
  - Advanced features and capabilities

#### System Operations
- **[5]** 🚀 **Start Ollama Server** - Launch Ollama backend
  - Keep this window open while chatting
  
- **[6]** 📥 **Install Ollama** - Installation guide
  - Shows setup instructions for your OS
  
- **[7]** 🎯 **Pull Ollama Models** - Download AI models
  - Choose from llama2, mistral, neural-chat, wizardlm, orca-mini
  - Or enter custom model name
  
- **[8]** 📊 **System Information** - Check system status
  - Shows Python, PowerShell, Ollama status
  - Verifies module directories exist

#### Advanced
- **[9]** 🔧 **Advanced Options** - Additional features
  - View conversation history
  - Check installed models
  - Git status
  - Setup dependencies
  - System diagnostics

- **[0]** ❌ **Exit** - Close launcher

## 🔧 Key Features

### Web GUI (Port 5000)
```
Features:
✓ Modern gradient UI with animations
✓ Real-time chat with Ollama
✓ Image upload support
✓ Code copy (hover trigger)
✓ Export to PDF (styled with timestamp)
✓ Export to JSON
✓ Model selector dropdown
✓ Online/Offline status indicator
✓ Conversation history
```

### Configuration
- **Conversation logs** saved to `config/conversation_log.json`
- **User uploads** stored in `uploads/`
- **Model list** updated at runtime
- **All paths** handled automatically

### API Endpoints (Web GUI)
```
POST   /api/chat              - Send message to Ollama
GET    /api/export-pdf        - Export chat as PDF
GET    /api/export            - Export chat as JSON
GET    /api/status            - Check Ollama status
POST   /api/clear-history     - Clear conversations
GET    /api/models            - List available models
```

## 📦 Dependencies

Install with:
```powershell
pip install -r requirements.txt
```

Core packages:
```
Flask                 # Web server
Flask-CORS           # Cross-origin requests
requests             # HTTP library
reportlab            # PDF generation
Pillow               # Image processing
rich                 # Terminal formatting
torch                # ML framework
transformers         # AI models
```

## 💻 System Requirements

- **Python**: 3.7+ (3.10+ recommended)
- **OS**: Windows, macOS, Linux
- **RAM**: 8GB+ (for Ollama models)
- **Disk**: 10GB+ for models
- **Internet**: Required for model download

## 🎯 Typical Workflow

1. **First Time Setup**:
   ```
   launcher.py → [6] Install Ollama → [7] Pull Models
   ```

2. **Start Chat Session**:
   ```
   launcher.py → [5] Start Ollama Server
   (In another terminal)
   launcher.py → [1] Web GUI (or [2]/[3] for terminal)
   ```

3. **Export Conversation**:
   ```
   In Web GUI: Click "Export to PDF" or "Export to JSON"
   Saved in: uploads/ directory
   ```

## 🛠️ Troubleshooting

### Ollama Not Starting
- **Solution**: Use [6] to install Ollama properly
- **Windows**: Download from ollama.ai or use winget

### Models Not Showing
- **Solution**: Use [7] to pull models first
- **Note**: Initial pull takes 5-30 minutes depending on model

### Web GUI Not Loading
- **Check**: http://localhost:5000 (not 5001)
- **Verify**: Flask process running correctly
- **Fix**: Use [8] System Information to diagnose

### Terminal UI Issues
- **Windows**: Run PowerShell as Administrator
- **Linux/Mac**: Use Terminal directly

## 📝 File Management

### Keeping Clean
- **Old logs**: Can delete old conversation_log.json backups
- **PDFs**: Stored in `uploads/` - delete old exports
- **Temporary**: No temp files created (safe!)

### Backing Up
Important files to backup:
- `config/conversation_log.json` - Your chat history
- `config/knowledge_base_comprehensive.json` - AI knowledge
- `config/user_learned_knowledge.json` - Learned patterns

## 🔐 Security Notes

- ✅ All data stored locally (no cloud sync)
- ✅ Ollama runs locally (no remote calls)
- ✅ No user tracking or logging
- ⚠️ PDF exports contain full chat history (be careful sharing)

## 📚 Advanced Usage

### Running Specific Module
```powershell
cd modules/web_gui
python app.py

cd ../terminal_ui
python terminal_interface.py
```

### Viewing Logs
Navigate to `config/conversation_log.json` - plain JSON file

### Custom Models
In launcher menu [7]:
```
Select: [6] Custom model
Enter: ollama-model-name (e.g., neural-chat-7b-v3)
```

## 🎨 Customization

### Web GUI Styling
Edit: `modules/web_gui/templates/index.html`
- Modify colors, fonts, layout
- Adjust gradient, animations
- Change button styles

### Backend Configuration
Edit: `modules/web_gui/app.py`
- Change port (default 5000)
- Adjust chat parameters
- Modify API endpoints

### Terminal UI
Edit: `modules/terminal_ui/terminal_interface.py`
- Colors, prompts, formatting
- Command history
- UI layout

## 📞 Support

For issues:
1. Check System Information ([8])
2. View Advanced Options ([9])
3. Check Ollama status: `ollama serve` in new terminal

## Version History

**v2.0.0** (Current)
- ✅ Modular architecture
- ✅ Menu-driven launcher
- ✅ Organized file structure
- ✅ Centralized configuration
- ✅ CSS improvements
- ✅ PDF export with styling
- ✅ Image upload support
- ✅ Code copy functionality

**v1.5.0**
- Previous monolithic structure

---

**Made with ❤️ by Arune**

LENLU LLM (emu) - Unified AI Interface for Ollama

*Everything You Need in One Place*
