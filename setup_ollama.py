"""
Setup script for LENLU AI+ with Ollama Integration
Installs dependencies and configures environment
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path


def install_ollama():
    """Guide user to install Ollama"""
    print("\n" + "="*60)
    print("OLLAMA INSTALLATION")
    print("="*60)
    
    if platform.system() == "Windows":
        print("\nFor Windows:")
        print("1. Download from: https://ollama.ai/download/windows")
        print("2. Run the installer")
        print("3. Ollama will start automatically")
        print("4. Or use: winget install JanDeDobbeleer.Ollama")
    
    elif platform.system() == "Darwin":  # macOS
        print("\nFor macOS:")
        print("1. Download from: https://ollama.ai/download/mac")
        print("2. Run the installer")
        print("3. Or use: brew install ollama")
    
    else:  # Linux
        print("\nFor Linux:")
        print("1. Run: curl https://ollama.ai/install.sh | sh")
        print("2. Or: snap install ollama")
    
    print("\nVerify installation:")
    print("  ollama --version")


def install_python_dependencies():
    """Install required Python packages"""
    print("\n" + "="*60)
    print("INSTALLING PYTHON DEPENDENCIES")
    print("="*60)
    
    packages = [
        "requests>=2.31.0",
        "rich>=13.0.0",
        "transformers>=4.30.0",
        "torch>=2.0.0"
    ]
    
    print("\nInstalling packages...")
    for package in packages:
        print(f"  Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", package], check=True)
            print(f"    ✓ {package}")
        except subprocess.CalledProcessError:
            print(f"    ✗ Failed: {package}")
            return False
    
    print("\n✓ All dependencies installed")
    return True


def setup_directories():
    """Create necessary directories"""
    print("\n" + "="*60)
    print("SETTING UP DIRECTORIES")
    print("="*60)
    
    directories = [
        "./models",
        "./models/ollama_models",
        "./models/cache",
        "./data",
        "./logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")


def setup_environment():
    """Set up environment variables"""
    print("\n" + "="*60)
    print("ENVIRONMENT SETUP")
    print("="*60)
    
    # Determine Ollama models directory
    if platform.system() == "Windows":
        models_dir = os.path.expanduser("~\\.ollama\\models")
    else:
        models_dir = os.path.expanduser("~/.ollama/models")
    
    print(f"\nOllama models directory: {models_dir}")
    
    # Create .env file
    env_content = f"""# LENLU AI+ Environment Configuration

# Ollama Settings
OLLAMA_MODELS={models_dir}
OLLAMA_HOST=localhost:11434

# Python Settings
PYTHONUNBUFFERED=1

# Model Settings
DEFAULT_MODEL=t5-base
OLLAMA_MODEL=llama3.1
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("  ✓ Created .env file")


def create_configs():
    """Ensure configuration files exist"""
    print("\n" + "="*60)
    print("CONFIGURATION FILES")
    print("="*60)
    
    config_file = "ollama_config.json"
    
    if not os.path.exists(config_file):
        default_config = {
            "ollama": {
                "enabled": False,
                "server_url": "http://localhost:11434",
                "auto_start": True,
                "default_model": "llama3.1",
                "timeout": 30
            },
            "generation": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 256
            }
        }
        
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)
        
        print(f"  ✓ Created {config_file}")
    else:
        print(f"  • {config_file} already exists")


def verify_installation():
    """Verify installation"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    checks = []
    
    # Check Python packages
    packages = ["requests", "rich", "transformers", "torch"]
    for package in packages:
        try:
            __import__(package)
            checks.append((package, True))
        except ImportError:
            checks.append((package, False))
    
    # Check directories
    dirs = ["models", "models/ollama_models", "models/cache"]
    for directory in dirs:
        exists = os.path.exists(directory)
        checks.append((f"Directory: {directory}", exists))
    
    # Check config files
    checks.append((".env", os.path.exists(".env")))
    checks.append(("ollama_config.json", os.path.exists("ollama_config.json")))
    
    print()
    for name, status in checks:
        symbol = "✓" if status else "✗"
        print(f"  [{symbol}] {name}")
    
    return all(status for _, status in checks)


def main():
    """Run setup"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║  LENLU AI+ with Ollama - Setup Wizard                   ║")
    print("╚" + "="*58 + "╝")
    
    steps = [
        ("Install Python Dependencies", install_python_dependencies),
        ("Create Directories", setup_directories),
        ("Setup Environment", setup_environment),
        ("Create Configurations", create_configs),
    ]
    
    for step_name, step_func in steps:
        print(f"\n[Step] {step_name}")
        try:
            step_func()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    # Verification
    print()
    if verify_installation():
        print("\n" + "="*60)
        print("✓ SETUP COMPLETE")
        print("="*60)
        
        print("\nNext steps:")
        print("  1. Install Ollama from https://ollama.ai")
        print("  2. Run 'ollama serve' to start the server")
        print("  3. Run 'python lenlu_ollama.py' to start LENLU")
        print("  4. Use '--ollama' flag to enable Ollama mode")
        
        print("\nUsage examples:")
        print("  Interactive mode:")
        print("    python lenlu_ollama.py")
        print("  With Ollama:")
        print("    python lenlu_ollama.py --ollama")
        print("  Single query:")
        print("    python lenlu_ollama.py --query 'What is binary search?'")
        
        return True
    else:
        print("\n✗ Some checks failed. Please review the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
