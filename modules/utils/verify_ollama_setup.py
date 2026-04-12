#!/usr/bin/env python3
"""
Verify LENLU AI+ Ollama Integration Setup
Check all files and configurations
"""

import os
import json
from pathlib import Path


def verify_files():
    """Verify all required files exist"""
    required_files = {
        "Core Integration": [
            "ollama_integration.py",
            "lenlu_ollama.py",
            "setup_ollama.py",
            "demo_ollama.py"
        ],
        "Configuration": [
            "ollama_config.json"
        ],
        "Documentation": [
            "OLLAMA_INTEGRATION_GUIDE.md",
            "QUICK_START_OLLAMA.md",
            "OLLAMA_SETUP_COMPLETE.md"
        ],
        "Model Files": [
            "models/lenlu-manifest.json",
            "models/lenlu-params.json",
            "models/LICENSE",
            "models/README.md"
        ],
        "Data Files": [
            "training_data_expanded.json",
            "knowledge_base_comprehensive.json"
        ]
    }
    
    print("\n" + "="*60)
    print("LENLU AI+ OLLAMA INTEGRATION VERIFICATION")
    print("="*60)
    
    all_good = True
    
    for category, files in required_files.items():
        print(f"\n[{category}]")
        for file in files:
            exists = os.path.exists(file)
            status = "✓" if exists else "✗"
            print(f"  [{status}] {file}")
            if not exists:
                all_good = False
    
    return all_good


def verify_config():
    """Verify configuration files"""
    print("\n" + "="*60)
    print("CONFIGURATION VERIFICATION")
    print("="*60)
    
    try:
        with open("ollama_config.json", 'r') as f:
            config = json.load(f)
        
        print("\n✓ ollama_config.json is valid JSON")
        
        required_keys = ["ollama", "generation"]
        for key in required_keys:
            if key in config:
                print(f"  ✓ Section: {key}")
            else:
                print(f"  ✗ Missing section: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"\n✗ Error reading config: {e}")
        return False


def verify_directories():
    """Verify required directories"""
    print("\n" + "="*60)
    print("DIRECTORY VERIFICATION")
    print("="*60)
    
    dirs = [
        "./models",
        "./models/ollama_models",
        "./models/cache"
    ]
    
    all_exist = True
    for directory in dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} (will be created on first run)")
            os.makedirs(directory, exist_ok=True)
    
    return True


def check_imports():
    """Check if required packages can be imported"""
    print("\n" + "="*60)
    print("PACKAGE VERIFICATION")
    print("="*60)
    
    packages = {
        "requests": "HTTP client",
        "rich": "Terminal formatting",
        "transformers": "HuggingFace models",
        "torch": "PyTorch"
    }
    
    missing = []
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package} ({description})")
        except ImportError:
            print(f"  ✗ {package} ({description}) - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\nTo install missing packages:")
        print(f"  python setup_ollama.py")
        print(f"  # or")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def show_quick_commands():
    """Show quick start commands"""
    print("\n" + "="*60)
    print("QUICK START COMMANDS")
    print("="*60)
    
    commands = [
        ("One-time setup", "python setup_ollama.py"),
        ("Run demos", "python demo_ollama.py"),
        ("Start LENLU (default)", "python lenlu_ollama.py"),
        ("Start LENLU with Ollama", "python lenlu_ollama.py --ollama"),
        ("Single query", "python lenlu_ollama.py --query 'What is OOP?'"),
        ("Streaming response", "python lenlu_ollama.py --ollama --query 'test' --stream"),
        ("With specific model", "python lenlu_ollama.py --ollama --model mistral"),
    ]
    
    for description, command in commands:
        print(f"\n{description}:")
        print(f"  $ {command}")


def show_file_tree():
    """Show file tree structure"""
    print("\n" + "="*60)
    print("NEW FILES CREATED")
    print("="*60)
    
    new_files = [
        "ollama_integration.py",
        "lenlu_ollama.py",
        "setup_ollama.py",
        "demo_ollama.py",
        "ollama_config.json",
        "OLLAMA_INTEGRATION_GUIDE.md",
        "QUICK_START_OLLAMA.md",
        "OLLAMA_SETUP_COMPLETE.md",
        "models/lenlu-manifest.json",
        "models/lenlu-params.json",
        "models/LICENSE",
        "models/README.md",
    ]
    
    print("\nNew files and directories added:")
    for file in new_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ○ {file}")


def show_next_steps():
    """Show next steps"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    steps = [
        ("1. Setup", "python setup_ollama.py"),
        ("2. Read Quick Start", "cat QUICK_START_OLLAMA.md"),
        ("3. Try Demos", "python demo_ollama.py"),
        ("4. Start LENLU", "python lenlu_ollama.py"),
        ("5. (Optional) Install Ollama", "https://ollama.ai/download"),
        ("6. (Optional) Enable Ollama", "python lenlu_ollama.py --ollama"),
    ]
    
    for step, action in steps:
        print(f"\n{step}")
        print(f"  → {action}")


def main():
    """Run all verifications"""
    results = {
        "Files": verify_files(),
        "Config": verify_config(),
        "Directories": verify_directories(),
        "Packages": check_imports(),
    }
    
    show_file_tree()
    show_quick_commands()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for check, result in results.items():
        status = "✓" if result else "✗"
        print(f"  [{status}] {check}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n" + "🎉 "*15)
        print("✓ ALL CHECKS PASSED - LENLU AI+ OLLAMA INTEGRATION READY!")
        print("🎉 "*15)
    else:
        print("\n⚠ Some checks failed. Run: python setup_ollama.py")
    
    show_next_steps()
    
    print("\n" + "="*60)
    print("For more information:")
    print("  • Quick Start: QUICK_START_OLLAMA.md")
    print("  • Full Guide: OLLAMA_INTEGRATION_GUIDE.md")
    print("  • Setup Info: OLLAMA_SETUP_COMPLETE.md")
    print("="*60 + "\n")
    
    return all_ok


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
