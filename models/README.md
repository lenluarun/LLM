# LENLU Model Structure

This directory contains LENLU AI+ model files in Ollama-compatible format.

## Directory Structure

```
models/
├── lenlu-manifest.json      # Ollama model manifest
├── lenlu-params.json        # Model parameters
├── LICENSE                  # Model license
├── ollama_models/           # Local Ollama models storage
│   ├── llama3.1/            # Ollama llama3.1 model
│   ├── mistral/             # Obtained Ollama models
│   └── ...
└── README.md                # This file
```

## Setting up Ollama Models

### Windows Local Storage Location
- **Default**: `%USERPROFILE%\.ollama\models`
- **Custom**: Use `OLLAMA_MODELS` environment variable

### Usage

1. **Initialize Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama serve
   ```

2. **Pull Models**
   ```bash
   ollama pull llama3.1
   ollama pull mistral
   ```

3. **Verify Installation**
   ```bash
   ollama list
   ```
