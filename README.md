# 🚀 LENLU LLM (emu) - Unified AI Chat Interface

**A powerful, modular Ollama chat application with multiple interfaces and a menu-driven launcher**

---

## ⚡ Quick Start

```powershell
python launcher.py
```

Choose from **9 interactive menu options** to access web GUI, terminal UI, chat CLI, or manage Ollama.

---

## 📁 Project Structure

```
LENLU LLM (emu)/
│
├── launcher.py              ⭐ MAIN ENTRY POINT - Run this!
├── requirements.txt         📦 Python dependencies
│
├── modules/                 🧩 MODULAR INTERFACES
│   ├── web_gui/            💻 Flask web interface (port 5000)
│   ├── terminal_ui/        🖥️  Rich terminal interface
│   ├── chat_interfaces/    💬 CLI chat options (Python, PowerShell)
│   └── utils/              🧠 Advanced LLM & tools
│
├── config/                  ⚙️  CONFIGURATION & DATA
│   ├── conversation_log.json
│   ├── knowledge_base_comprehensive.json
│   ├── training_data_expanded.json
│   ├── user_learned_knowledge.json
│   └── ollama_config.json
│
├── docs/                    📚 DOCUMENTATION
│   ├── PROJECT_STRUCTURE.md (Complete organization guide)
│   ├── INTERFACE_GUIDE.md
│   ├── OLLAMA_INTEGRATION_GUIDE.md
│   ├── QUICK_START_OLLAMA.md
│   └── (11 more guides)
│
├── scripts/                 🔧 HELPER SCRIPTS
│   ├── launch_interface.bat
│   └── LENLU_Interface.ps1
│
├── uploads/                 📤 EXPORTS
│   └── (PDF & JSON exports)
│
├── models/                  🤖 LOCAL MODELS
│   ├── ollama_models/
│   └── lenlu-params.json
│
└── archive/                 📦 LEGACY FILES
    └── templates_legacy/
```

---

## 🎯 Menu Options (0-9)

### **Interfaces** 
- **[1]** 💻 Web GUI - Beautiful browser interface at http://localhost:5000
- **[2]** 🖥️ Terminal UI - Rich-styled terminal chat
- **[3]** 💬 Chat CLI - Simple command-line chat
- **[4]** 🧠 Advanced LLM - Full-featured AI assistant

### **System Operations**
- **[5]** 🚀 Start Ollama Server
- **[6]** 📥 Install Ollama (platform-specific instructions)
- **[7]** 🎯 Pull Ollama Models
- **[8]** 📊 System Information & diagnostics

### **Advanced**
- **[9]** 🔧 Advanced Options (history, models, update from GitHub, setup dependencies)
- **[0]** ❌ Exit

---

## 💡 Key Features

✅ **Multiple Interfaces**
   - Web UI with modern design
   - Terminal interface with rich formatting
   - CLI chat options
   - Advanced LLM assistant

✅ **Ollama Integration**
   - Auto-connect to local Ollama server
   - Pull & manage models
   - Real-time chat with streaming

✅ **Export & Share**
   - PDF export with styling & timestamps
   - JSON export for data portability
   - Code copy functionality
   - Image upload support

✅ **Organized Architecture**
   - Menu-driven (no command exposure)
   - Modular design (separate interfaces)
   - Centralized config storage
   - Clean file organization

---

## 🔧 Setup

### **1. Install Dependencies**
```powershell
pip install -r requirements.txt
```

### **2. Install Ollama** (if not installed)
```powershell
python launcher.py
# Select [6] Install Ollama
# Follow platform-specific instructions
```

### **3. Pull a Model** (first time)
```powershell
python launcher.py
# Select [7] Pull Ollama Models
# Choose from: llama2, mistral, neural-chat, wizardlm, orca-mini
```

### **4. Start Using!**
```powershell
python launcher.py
# Select [1] for Web GUI, [2] for Terminal, or [3] for CLI
```

---

## 📋 System Requirements

- **Python**: 3.7+ (3.10+ recommended)
- **OS**: Windows, macOS, Linux
- **RAM**: 8GB+ for Ollama
- **Disk**: 10GB+ for ML models
- **Internet**: For model downloads

---

## 📚 Documentation

Complete guides in `/docs/`:
- **PROJECT_STRUCTURE.md** - Full architecture details
- **QUICK_START_OLLAMA.md** - Ollama setup guide
- **INTERFACE_GUIDE.md** - UI usage guide
- **OLLAMA_INTEGRATION_GUIDE.md** - API integration details
- ...and 8 more comprehensive guides

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Ollama not starting** | Use launcher [6] to install Ollama |
| **No models available** | Use launcher [7] to pull models |
| **Web GUI won't load** | Check http://localhost:5000 (verify Flask running) |
| **Terminal UI issues** | Run launcher as Administrator on Windows |
| **Models downloading slowly** | This is normal - first download takes 5-30min depending on model |

---

## 🎨 Web GUI Features

- 🎨 Modern gradient UI with animations
- 📱 Responsive mobile-friendly design
- 💬 Real-time chat with Ollama
- 🖼️ Image upload support
- 📋 Code syntax highlighting with copy button
- 📊 Export to PDF (styled with timestamp)
- 💾 Export to JSON
- 🔄 Model selector dropdown
- 🟢 Online/Offline status indicator
- 📜 Full conversation history

---

## ⚙️ Configuration

All configs stored in `/config/`:
- `conversation_log.json` - Chat history (auto-created)
- `knowledge_base_comprehensive.json` - AI knowledge base
- `training_data_expanded.json` - Training data
- `user_learned_knowledge.json` - Learned user preferences
- `ollama_config.json` - Ollama settings

---

## 🔐 Privacy & Security

✅ **All local** - No cloud, no analytics, no tracking
✅ **No telemetry** - Your data stays on your machine
✅ **Open source** - Transparent, auditable code
⚠️ **Be careful** - PDF exports contain full chat (don't share if sensitive)

---

## 🚀 Advanced Usage

### Run Specific Module Directly
```powershell
cd modules/web_gui
python app.py

cd ../terminal_ui
python terminal_interface.py
```

### Customize Web GUI
Edit: `modules/web_gui/templates/index.html`
- Modify colors, fonts, gradients
- Adjust animations and layout
- Change button styles

### Customize Backend
Edit: `modules/web_gui/app.py`
- Change port (default 5000)
- Modify LLM parameters
- Add new API endpoints

---

## 📦 Dependencies

```
Flask                 # Web framework
Flask-CORS           # API access
requests             # HTTP client
reportlab            # PDF generation
Pillow               # Image processing
rich                 # Terminal styling
torch                # ML framework
transformers         # AI models
```

Full list in `requirements.txt`

---

## 📊 Project Stats

- **Modular Architecture**: 4 separate interfaces
- **API Endpoints**: 6+ REST endpoints
- **Supported Models**: Llama2, Mistral, Neural-Chat, WizardLM, Orca-Mini, Custom
- **Export Formats**: PDF, JSON
- **Menu Options**: 10 (0-9)
- **Documentation**: 12+ guides
- **Lines of Code**: 1500+

---

## 🎯 Use Cases

- 💼 **Business**: Quick local AI for business tasks
- 👨‍💻 **Development**: AI assistant for coding
- 📚 **Education**: Learn AI & machine learning
- 🔬 **Research**: Experiment with LLMs locally
- 🛡️ **Privacy**: Chat without cloud concerns

---

## 🤝 Contributing

This is an active development project. Feel free to:
- Report bugs
- Suggest features
- Submit improvements
- Share feedback

---

## 📝 Version Info

**Version**: 2.0.0  
**Status**: Production Ready  
**Last Updated**: April 2026  
**License**: Open Source

---

## 👤 Author

**Arune** - Creator of LENLU LLM (emu)

---

## 🎓 Learn More

- Ollama Documentation: https://ollama.ai
- Flask Documentation: https://flask.palletsprojects.com
- PyTorch Documentation: https://pytorch.org

---

## 🙏 Acknowledgments

Built with:
- **Ollama** - Local LLM inference
- **Flask** - Web framework
- **PyTorch** - Deep learning
- **Rich** - Terminal formatting

---

**🌟 Start chatting now with `python launcher.py` 🌟**

*Everything You Need in One Place™*
