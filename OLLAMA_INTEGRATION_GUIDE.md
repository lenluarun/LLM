# LENLU AI+ with Ollama Integration - Complete Guide

## Overview

LENLU AI+ now has full Ollama integration, allowing you to:
- Use local Ollama models (llama3.1, mistral, neural-chat, etc.)
- Combine Ollama with LENLU's training data and knowledge base
- Switch between T5 and Ollama models seamlessly
- Stream responses for real-time output
- Maintain full learning and training capabilities

## Architecture

```
LENLU AI+ 
├── T5 Model (Default)
│   ├── Training Data (139 Q&A pairs)
│   ├── Knowledge Base (1000+ concepts)
│   └── Learning System
│
└── Ollama Integration (Optional)
    ├── Local Ollama Server
    ├── Multiple Models Support
    ├── Embedding Generation
    └── Streaming Output
```

## Installation

### 1. Install Ollama

**Windows:**
```bash
# Download from https://ollama.ai
# Or use Winget
winget install JanDeDobbeleer.Ollama

# Start Ollama
ollama serve
```

**macOS:**
```bash
# Download from https://ollama.ai
# Or use Homebrew
brew install ollama

# Start Ollama
ollama serve
```

**Linux:**
```bash
# Install
curl https://ollama.ai/install.sh | sh

# Start
ollama serve
```

### 2. Install Python Dependencies

```bash
# Run setup script
python setup_ollama.py

# Or install manually
pip install requests rich transformers torch
```

### 3. Pull Ollama Models

```bash
# In another terminal (while ollama serve is running)
ollama pull llama3.1
ollama pull mistral
ollama pull neural-chat
```

## Quick Start

### Mode 1: Default T5 Mode
```bash
python lenlu_ollama.py
```
- Uses T5 model with LENLU knowledge base
- No external dependencies
- Instant startup

### Mode 2: Ollama Mode
```bash
# Start Ollama server first (in another terminal)
ollama serve

# In your terminal
python lenlu_ollama.py --ollama
```
- Uses Ollama's llama3.1 model
- Better quality responses
- Requires Ollama running

### Mode 3: Custom Model
```bash
python lenlu_ollama.py --ollama --model mistral
```
- Use any Ollama model
- Models auto-download if needed

### Mode 4: Single Query
```bash
python lenlu_ollama.py --query "What is binary search?"
python lenlu_ollama.py --ollama --query "Explain React hooks"
```

### Mode 5: Streaming Response
```bash
python lenlu_ollama.py --ollama --query "What is OOP?" --stream
```

## Interactive Commands

When running LENLU, use these commands:

```
LENLU> ask any question
  → Generates response using current mode

LENLU> models
  → List available Ollama models

LENLU> ollama
  → Toggle between T5 and Ollama mode

LENLU> stats
  → View learning statistics (T5 mode)

LENLU> quit
  → Exit program
```

## Configuration

Edit `ollama_config.json` to customize:

```json
{
  "ollama": {
    "enabled": false,              // Start with Ollama disabled
    "server_url": "http://localhost:11434",
    "auto_start": true,            // Auto-start Ollama server
    "default_model": "llama3.1",   // Default model
    "timeout": 30                  // Request timeout
  },
  "generation": {
    "temperature": 0.7,            // Creativity (0-2)
    "top_p": 0.9,                  // Nucleus sampling
    "num_predict": 256             // Max tokens
  }
}
```

## Available Models

### Popular Ollama Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.1 | 8B | Fast | Excellent | General purpose, coding |
| mistral | 7B | Very Fast | Good | Quick responses |
| neural-chat | 7B | Fast | Good | Conversation |
| orca-mini | 3B | Very Fast | Fair | Low-resource |
| dolphin-mixtral | 47B | Slow | Excellent | Complex reasoning |

### Get More Models

```bash
ollama list              # Show installed models
ollama pull llama3.1     # Download model
ollama show llama3.1     # Get model info
ollama pull neural-chat  # Get another model
```

## Hybrid Mode Features

When both T5 and Ollama are available, LENLU uses hybrid approach:

1. **Search Training Data** (139 Q&A pairs)
   - Fast, high-confidence answers
   - Example: "What is binary search?"

2. **Extract Knowledge Base** (1000+ concepts)
   - Comprehensive, verified information
   - Example: "Explain database normalization"

3. **Ollama Model Generation** (if enabled)
   - For complex questions needing reasoning
   - Creative responses

4. **Fallback to Templates**
   - Category-based responses
   - Always provides helpful output

## Performance Comparison

### T5 Mode (Default)
- **Startup Time**: < 1 second
- **Response Time**: 0.5-2 seconds
- **Memory**: ~2GB
- **Quality**: Good (training-data-first)
- **External Deps**: None

### Ollama Mode (llama3.1)
- **Startup Time**: 3-5 seconds (first run), instant (subsequent)
- **Response Time**: 2-10 seconds
- **Memory**: 6-8GB
- **Quality**: Excellent (reasoning-based)
- **External Deps**: Ollama server

### Ollama Mode (mistral)
- **Startup Time**: < 1 second
- **Response Time**: 1-3 seconds
- **Memory**: 4-6GB
- **Quality**: Very Good (fast)
- **External Deps**: Ollama server

## Advanced Usage

### Python API

```python
from lenlu_ollama import LenluWithOllama

# Create instance
lenlu = LenluWithOllama(use_ollama=True, ollama_model="llama3.1")

# Generate response
response = lenlu.generate_response("What is OOP?")
print(response)

# Stream response
for chunk in lenlu.stream_response("Explain design patterns"):
    print(chunk, end="", flush=True)
```

### Direct Ollama Integration

```python
from ollama_integration import OllamaIntegration

ollama = OllamaIntegration()
ollama.list_models()
ollama.pull_model("mistral")

response = ollama.generate_completion(
    "llama3.1",
    "What is binary search?",
    temperature=0.7
)
print(response)
```

### Embeddings

```python
from ollama_integration import OllamaIntegration

ollama = OllamaIntegration()

# Generate embeddings
embeddings = ollama.embed_text("llama3.1", "machine learning")
print(len(embeddings))  # Usually 4096
```

## Troubleshooting

### Ollama Server Not Running
```bash
# Windows: Start Ollama from Start Menu or:
"C:\Program Files\Ollama\ollama.exe" serve

# macOS: Open Ollama app or:
ollama serve

# Linux:
ollama serve
```

### Model Not Found
```bash
# Pull the model first
ollama pull llama3.1
ollama pull mistral

# Verify
ollama list
```

### Out of Memory
```bash
# Use smaller model
python lenlu_ollama.py --ollama --model orca-mini

# Or reduce generation length
# Edit ollama_config.json and set "num_predict": 128
```

### Slow Responses
```bash
# Check if using CPU (should be GPU)
ollama show mistral  # Check parameters

# Use faster model
ollama pull mistral   # 7B, very fast

# Reduce temperature for faster generation
# Edit ollama_config.json: "temperature": 0.5
```

## Storage Information

### Windows
- **Models**: `%USERPROFILE%\.ollama\models`
- **Cache**: `%USERPROFILE%\.ollama\cache`

### macOS/Linux
- **Models**: `~/.ollama/models`
- **Cache**: `~/.ollama/cache`

### Project Local
- **Models**: `./models/ollama_models`
- **Config**: `./ollama_config.json`
- **Cache**: `./models/cache`

## File Structure

```
llm/
├── lenlu_ai_plus.py              # Original LENLU
├── lenlu_ollama.py               # Ollama integration
├── ollama_integration.py          # Ollama API wrapper
├── ollama_config.json             # Configuration
├── setup_ollama.py                # Setup script
├── models/
│   ├── lenlu-manifest.json        # LENLU model manifest
│   ├── lenlu-params.json          # LENLU parameters
│   ├── ollama_models/             # Local models
│   └── cache/                     # Cached models
├── training_data_expanded.json    # 139 Q&A pairs
├── knowledge_base_comprehensive.json  # 1000+ concepts
└── ollama_config.json             # Ollama config
```

## License

LENLU AI+ with Ollama Integration is released under MIT License.
See `./models/LICENSE` for details.

## Support

- **Issues**: Create issue with platform (Windows/macOS/Linux)
- **Models**: Check https://ollama.ai for available models
- **Ollama**: Visit https://ollama.ai for documentation

---

**Version**: 1.0.0
**Last Updated**: 2026-04-11
**Status**: ✅ Production Ready
