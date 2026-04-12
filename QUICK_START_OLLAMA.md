# LENLU AI+ with Ollama - Quick Start (5 Minutes)

## ✅ What You Get

- LENLU LLM running locally
- Optional Ollama support (llama3.1, mistral, etc.)
- Hybrid mode: T5 + Knowledge Base + Ollama
- Streaming responses
- Full learning capabilities

## 🚀 Quick Setup

### Step 1: Install Ollama (Optional)
```bash
# Windows: Download from https://ollama.ai/download/windows
# macOS: brew install ollama
# Linux: curl https://ollama.ai/install.sh | sh
```

### Step 2: Install Python Packages
```bash
python setup_ollama.py

# Or manually:
pip install requests rich transformers torch
```

### Step 3: Start Ollama Server (If using Ollama)
```bash
# In a separate terminal
ollama serve
```

### Step 4: Run LENLU
```bash
# Default mode (T5 + Knowledge Base - No dependencies)
python lenlu_ollama.py

# With Ollama (requires server running)
python lenlu_ollama.py --ollama

# Or specific model
python lenlu_ollama.py --ollama --model mistral
```

## 📝 Usage Examples

### Interactive Mode
```bash
python lenlu_ollama.py

# Type your question
LENLU> What is binary search?
# Get instant answer from training data

# Toggle Ollama
LENLU> ollama
# Now switching to Ollama model for better responses

# List available models
LENLU> models

# Exit
LENLU> quit
```

### Single Query
```bash
python lenlu_ollama.py --query "What is OOP?"
python lenlu_ollama.py --ollama --query "Explain Docker"
```

### Streaming Response
```bash
python lenlu_ollama.py --ollama --query "What is machine learning?" --stream
```

## 🎯 Mode Comparison

| Feature | T5 Mode | Ollama Mode |
|---------|---------|-------------|
| **Startup** | Instant | 3-5 seconds |
| **Memory** | 2GB | 6-8GB |
| **Quality** | Good | Excellent |
| **Dependencies** | None | Ollama server |
| **Speed** | Fast | Medium |
| **Learning** | Yes | Yes |

**Default**: T5 Mode (start instantly)
**Recommended**: Ollama Mode for better responses

## 📦 Available Models

Pull any of these:
```bash
ollama pull llama3.1        # Best quality (8GB)
ollama pull mistral         # Fast (7GB)
ollama pull neural-chat     # Conversation (7GB)
ollama pull orca-mini       # Lightweight (3GB)
```

## 📂 Storage Locations

**Windows:**
- Models: `C:\Users\<username>\.ollama\models`
- Config: `./ollama_config.json`

**macOS/Linux:**
- Models: `~/.ollama/models`
- Config: `./ollama_config.json`

## 🔧 Common Issues

### "Ollama server not running"
```bash
# Start Ollama
ollama serve

# In new terminal, run LENLU
python lenlu_ollama.py --ollama
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.1

# Verify
ollama list
```

### "Out of Memory"
```bash
# Use smaller model
python lenlu_ollama.py --ollama --model orca-mini
```

## 💡 Tips

1. **Start with T5 mode** - Works instantly, no setup
2. **Add Ollama later** - Switch anytime with `ollama` command
3. **Check models** - Use `ollama list` to see what's installed
4. **Stream responses** - Great for long answers
5. **Hybrid mode** - Switches automatically based on question complexity

## 📚 Learn More

- Full guide: `OLLAMA_INTEGRATION_GUIDE.md`
- Ollama docs: https://ollama.ai
- LENLU features: `ENHANCEMENT_SUMMARY.md`

## ⚡ Performance

- **T5 Response**: 0.5-2 seconds
- **Ollama Response**: 2-10 seconds (depending on model)
- **Training Impact**: Minimal (<100ms overhead)

---

**Ready?** Start with: `python lenlu_ollama.py`

**Need Ollama?** https://ollama.ai/download

**Questions?** Check troubleshooting section in full guide.
