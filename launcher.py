"""
LENLU LLM (emu) - Master Launcher
Central hub for all modules and interfaces
Everything executes through menu options - NO direct command execution
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Official & popular Ollama models: category -> list of {ref, disk, detail}
# ref is the full `model:tag` for `ollama pull` (disk sizes are approximate Q4 where noted).
OLLAMA_INSTALL_CATALOG = [
    {
        "id": "general",
        "title": "General purpose & chat",
        "models": [
            {"ref": "llama3.2:1b", "disk": "~1.3GB", "detail": "Meta Llama 3.2 — fast, edge-friendly"},
            {"ref": "llama3.2:3b", "disk": "~2.0GB", "detail": "Meta Llama 3.2 — balanced lightweight"},
            {"ref": "llama3.1:8b", "disk": "~4.7GB", "detail": "Meta Llama 3.1 — strong daily driver"},
            {"ref": "llama3.1:70b", "disk": "~40GB+", "detail": "Meta Llama 3.1 — high quality, heavy RAM"},
            {"ref": "llama3.1:405b", "disk": "~230GB+", "detail": "Meta Llama 3.1 — flagship, very large"},
            {"ref": "mistral", "disk": "~4.1GB", "detail": "Mistral 7B class — use library tags for v0.3 / instruct"},
            {"ref": "gemma2:2b", "disk": "~1.6GB", "detail": "Google Gemma 2 — tiny"},
            {"ref": "gemma2:9b", "disk": "~5GB+", "detail": "Google Gemma 2 — capable mid-size"},
            {"ref": "gemma2:27b", "disk": "~16GB", "detail": "Google Gemma 2 — larger variant"},
            {"ref": "qwen2.5:0.5b", "disk": "~390MB", "detail": "Qwen 2.5 — minimal footprint"},
            {"ref": "qwen2.5:1.5b", "disk": "~1GB+", "detail": "Qwen 2.5 — small, multilingual"},
            {"ref": "qwen2.5:7b", "disk": "~4.5GB+", "detail": "Qwen 2.5 — popular mid-size"},
            {"ref": "qwen2.5:14b", "disk": "~9GB+", "detail": "Qwen 2.5 — stronger reasoning"},
            {"ref": "qwen2.5:32b", "disk": "~19GB+", "detail": "Qwen 2.5 — large context family"},
            {"ref": "qwen2.5:72b", "disk": "~47GB", "detail": "Qwen 2.5 — top open tier"},
            {"ref": "phi3.5:latest", "disk": "~2.3GB", "detail": "Microsoft Phi 3.5 Mini — small but strong"},
        ],
    },
    {
        "id": "reasoning",
        "title": "Reasoning, math & logic",
        "models": [
            {"ref": "deepseek-r1:1.5b", "disk": "~1.1GB", "detail": "DeepSeek-R1 — tiny reasoning"},
            {"ref": "deepseek-r1:7b", "disk": "~4.5GB+", "detail": "DeepSeek-R1 — practical local"},
            {"ref": "deepseek-r1:14b", "disk": "~9GB+", "detail": "DeepSeek-R1 — stronger"},
            {"ref": "deepseek-r1:32b", "disk": "~19GB+", "detail": "DeepSeek-R1 — large"},
            {"ref": "deepseek-r1:70b", "disk": "~40GB+", "detail": "DeepSeek-R1 — very large"},
            {"ref": "deepseek-r1:671b", "disk": "~400GB+", "detail": "DeepSeek-R1 — flagship MoE"},
            {"ref": "qwen2.5-math:1.5b", "disk": "~1.1GB", "detail": "Qwen 2.5 Math — compact"},
            {"ref": "qwen2.5-math:7b", "disk": "~4.5GB+", "detail": "Qwen 2.5 Math — standard"},
            {"ref": "qwen2.5-math:72b", "disk": "~47GB", "detail": "Qwen 2.5 Math — maximum"},
        ],
    },
    {
        "id": "coding",
        "title": "Coding & development",
        "models": [
            {"ref": "qwen2.5-coder:0.5b", "disk": "~390MB", "detail": "Qwen 2.5 Coder — minimal"},
            {"ref": "qwen2.5-coder:1.5b", "disk": "~1GB+", "detail": "Qwen 2.5 Coder — small"},
            {"ref": "qwen2.5-coder:7b", "disk": "~4.5GB+", "detail": "Qwen 2.5 Coder — recommended"},
            {"ref": "qwen2.5-coder:14b", "disk": "~9GB+", "detail": "Qwen 2.5 Coder — stronger"},
            {"ref": "qwen2.5-coder:32b", "disk": "~19GB", "detail": "Qwen 2.5 Coder — large"},
            {"ref": "codellama:7b", "disk": "~4.8GB", "detail": "Code Llama — FIM-friendly"},
            {"ref": "codellama:13b", "disk": "~7GB+", "detail": "Code Llama — mid"},
            {"ref": "codellama:34b", "disk": "~20GB", "detail": "Code Llama — large"},
            {"ref": "codellama:70b", "disk": "~39GB", "detail": "Code Llama — top Code Llama"},
            {"ref": "codestral:latest", "disk": "~13GB", "detail": "Mistral Codestral — 22B-class coding"},
            {"ref": "deepseek-coder-v2:16b", "disk": "~8.9GB", "detail": "DeepSeek Coder V2 — MoE coding"},
            {"ref": "deepseek-coder-v2:236b", "disk": "~133GB+", "detail": "DeepSeek Coder V2 — huge MoE"},
        ],
    },
    {
        "id": "vision",
        "title": "Vision & multimodal",
        "models": [
            {"ref": "llama3.2-vision:11b", "disk": "~7.9GB", "detail": "Llama 3.2 Vision — image + text"},
            {"ref": "llama3.2-vision:90b", "disk": "~55GB+", "detail": "Llama 3.2 Vision — large"},
            {"ref": "llava:7b", "disk": "~4.7GB", "detail": "LLaVA — classic VLM"},
            {"ref": "llava:13b", "disk": "~8GB+", "detail": "LLaVA — stronger"},
            {"ref": "llava:34b", "disk": "~20GB", "detail": "LLaVA — large"},
            {"ref": "moondream:latest", "disk": "~1.2GB", "detail": "Moondream — tiny, fast vision"},
        ],
    },
    {
        "id": "creative",
        "title": "Uncensored & creative / roleplay",
        "models": [
            {"ref": "dolphin-llama3:8b", "disk": "~4.7GB", "detail": "Dolphin Llama 3 — uncensored Llama 3"},
            {"ref": "dolphin-mistral:7b", "disk": "~4.1GB", "detail": "Dolphin Mistral — uncensored Mistral"},
            {"ref": "nous-hermes2:latest", "disk": "~6.5GB+", "detail": "Nous Hermes 2 — instruct / RP (check tags on library)"},
            {"ref": "nous-hermes2:34b", "disk": "~20GB", "detail": "Nous Hermes 2 — 34B class"},
        ],
    },
    {
        "id": "embedding",
        "title": "Embeddings (RAG / vector DB)",
        "models": [
            {"ref": "nomic-embed-text:latest", "disk": "~274MB", "detail": "Nomic Embed — 8k context, fast"},
            {"ref": "mxbai-embed-large:latest", "disk": "~669MB", "detail": "Mixedbread large embeddings"},
            {"ref": "all-minilm:l6-v2", "disk": "~45MB", "detail": "MiniLM — very small"},
            {"ref": "all-minilm:l12-v2", "disk": "~120MB", "detail": "MiniLM — slightly larger"},
        ],
    },
]


def run_ollama_pull(model_ref: str) -> int:
    """Run `ollama pull <ref>` and return process exit code."""
    print(f"\n⏳ Pulling {model_ref} ...")
    print("(This can take a long time. Ensure `ollama serve` is running.)\n")
    proc = subprocess.run(
        ["ollama", "pull", model_ref],
        shell=False,
    )
    return proc.returncode

def clear_screen():
    """Clear terminal"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def print_header():
    """Print styled header"""
    clear_screen()
    print("=" * 70)
    print("  LENLU LLM (emu) - by Arunesh".center(70))
    print("  Ollama Chat - All-in-One Interface".center(70))
    print("=" * 70)
    print()

def print_menu():
    """Print main menu"""
    print_header()
    print("MAIN MENU - Choose Your Interface:\n")
    print("  [1] 💻 Web GUI        - Beautiful browser interface")
    print("  [2] 🖥️  Terminal UI   - Rich terminal interface")
    print("  [3] 💬 Chat CLI      - Simple command-line chat")
    print("  [4] 🧠 Advanced LLM  - Full-featured AI assistant\n")
    print("System Operations:\n")
    print("  [5] 🚀 Start Ollama Server")
    print("  [6] 📥 Install Ollama")
    print("  [7] 🎯 Pull Ollama Models")
    print("  [8] 📊 System Information")
    print("  [9] 🔧 Advanced Options")
    print("  [0] ❌ Exit\n")

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_powershell():
    """Check if PowerShell is available"""
    if sys.platform != 'win32':
        return False
    try:
        result = subprocess.run(['powershell', '-Command', 'echo test'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_files():
    """Check if required files exist"""
    return Path('modules/web_gui/app.py').exists()

def launch_web_gui():
    """Launch Flask web GUI"""
    clear_screen()
    print_header()
    print("🌐 Launching Web GUI Server...\n")
    
    try:
        web_gui_path = Path('modules/web_gui')
        if not web_gui_path.exists():
            print("❌ Web GUI module not found!")
            input("Press Enter to continue...")
            return
        
        print("Starting Flask server...")
        print("📍 Open browser to: http://localhost:5000\n")
        
        os.chdir(web_gui_path)
        os.system('python app.py')
        os.chdir('../..')
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def launch_terminal_ui():
    """Launch Terminal UI"""
    clear_screen()
    print_header()
    print("🖥️  Launching Terminal Interface...\n")
    
    try:
        terminal_path = Path('modules/terminal_ui')
        if not terminal_path.exists():
            print("❌ Terminal UI module not found!")
            input("Press Enter to continue...")
            return
        
        print("Starting terminal interface...\n")
        os.chdir(terminal_path)
        os.system('python terminal_interface.py')
        os.chdir('../..')
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def launch_chat_cli():
    """Launch Chat CLI"""
    clear_screen()
    print_header()
    print("💬 Launching Chat CLI...\n")
    
    try:
        chat_path = Path('modules/chat_interfaces')
        if not chat_path.exists():
            print("❌ Chat interfaces module not found!")
            input("Press Enter to continue...")
            return
        
        print("Starting chat interface...\n")
        os.chdir(chat_path)
        os.system('python ollama_chat_interface.py')
        os.chdir('../..')
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def launch_advanced_llm():
    """Launch Advanced LLM"""
    clear_screen()
    print_header()
    print("🧠 Launching Advanced LLM Assistant...\n")
    
    try:
        utils_path = Path('modules/utils')
        if not utils_path.exists():
            print("❌ Advanced LLM module not found!")
            input("Press Enter to continue...")
            return
        
        print("Starting advanced LLM assistant...\n")
        os.chdir(utils_path)
        os.system('python lenlu_ai_plus.py')
        os.chdir('../..')
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def start_ollama_server():
    """Start Ollama server"""
    clear_screen()
    print_header()
    print("🚀 Starting Ollama Server...\n")
    print("Keep this window open to maintain the Ollama service.")
    print("Open another terminal to use chat interfaces.\n")
    print("=" * 70 + "\n")
    
    try:
        os.system('ollama serve')
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter when done...")

def install_ollama():
    """Install Ollama automatically based on OS"""
    clear_screen()
    print_header()
    print("📥 Ollama Installation & Setup\n")
    
    try:
        # Check if Ollama is already installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama is already installed: {result.stdout.strip()}\n")
            print("Moving to available models...\n")
            input("Press Enter to continue...")
            fetch_online_models()
            return
    except:
        pass
    
    print("Installing Ollama...\n")
    print("=" * 70)
    
    if sys.platform == 'win32':
        print("\n🪟 Windows Installation:\n")
        print("Attempting to install via winget...\n")
        os.system('winget install Ollama.Ollama')
        print("\n" + "=" * 70)
        print("\n✅ Installation completed!")
        print("\nNext steps:")
        print("  1. Restart your terminal/computer")
        print("  2. Run: ollama serve")
        print("  3. In another terminal, use the chat interfaces")
        
    elif sys.platform == 'darwin':
        print("\n🍎 macOS Installation:\n")
        print("Attempting to install via Homebrew...\n")
        os.system('brew install ollama')
        print("\n" + "=" * 70)
        print("\n✅ Installation completed!")
        print("\nNext steps:")
        print("  1. Run: ollama serve")
        print("  2. In another terminal, use the chat interfaces")
        
    else:
        print("\n🐧 Linux Installation:\n")
        print("Attempting to install via curl...\n")
        os.system('curl -fsSL https://ollama.ai/install.sh | sh')
        print("\n" + "=" * 70)
        print("\n✅ Installation completed!")
        print("\nNext steps:")
        print("  1. Run: ollama serve")
        print("  2. In another terminal, use the chat interfaces")
    
    print("\n" + "=" * 70)
    print("\nFetching available models from online library...\n")
    input("Press Enter to see available models...")
    fetch_online_models()

def fetch_online_models():
    """Show curated official/popular Ollama models and optional installer."""
    clear_screen()
    print_header()
    print("🌐 Ollama model catalog (curated)\n")
    print("Install: ollama pull <model>:<tag>   Chat after download: ollama run <model>:<tag>")
    print("Exact on-disk sizes: run  ollama list  (with Ollama running).\n")

    for cat in OLLAMA_INSTALL_CATALOG:
        print("=" * 70)
        print(f"  {cat['title']}")
        print("=" * 70)
        print(f"{'REF':<38} {'~SIZE':<12} DETAIL")
        print("-" * 70)
        for m in cat["models"]:
            ref = m["ref"]
            disk = m.get("disk", "")
            detail = m.get("detail", "")
            ref_disp = ref[:37] + "…" if len(ref) > 37 else ref
            print(f"{ref_disp:<38} {disk:<12} {detail}")
        print()

    print("=" * 70)
    print("Community library: https://ollama.com/library (thousands of community models)\n")

    while True:
        print("What next?")
        print("  [1] Open model installer (pick category + number → ollama pull)")
        print("  [2] Show installation / usage tips")
        print("  [3] Return to main menu\n")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            pull_ollama_models()
            break
        if choice == "2":
            clear_screen()
            print_header()
            print("📥 Tips\n")
            print("  • Start Ollama:  ollama serve  (or launcher [5])")
            print("  • Download only:  ollama pull <model>:<tag>")
            print("  • Download + chat:  ollama run <model>:<tag>")
            print("  • See installed models & sizes:  ollama list\n")
            print("Then use this launcher: Web GUI [1], Terminal [2], Chat CLI [3], Advanced [4].\n")
            input("Press Enter to continue...")
            break
        if choice == "3":
            break
        print("❌ Invalid choice. Please try again.")

def pull_ollama_models():
    """Numbered installer: category → variant → `ollama pull`."""
    while True:
        clear_screen()
        print_header()
        print("🎯 Ollama model installer\n")
        print("Pick a category, then a model by number. Runs:  ollama pull <ref>\n")
        print("After install, use  ollama list  for exact sizes.\n")

        print("  [0] Return to main menu")
        for i, cat in enumerate(OLLAMA_INSTALL_CATALOG, 1):
            n = len(cat["models"])
            print(f"  [{i}] {cat['title']} ({n} variants)")
        last = len(OLLAMA_INSTALL_CATALOG) + 1
        print(f"  [{last}] Custom model (type name:tag)\n")

        try:
            c = input(f"Category (0-{last}): ").strip()
        except (EOFError, KeyboardInterrupt):
            return

        if c == "0":
            return

        if c == str(last):
            ref = input("Enter full model ref (e.g. llama3.2:3b or mistral): ").strip()
            if not ref:
                print("❌ Empty input.")
                input("\nPress Enter to continue...")
                continue
            code = run_ollama_pull(ref)
            if code == 0:
                print("\n✅ Pull finished successfully.")
                print("Run  ollama list  to see exact sizes.\n")
            else:
                print(f"\n❌ ollama pull exited with code {code}. Is Ollama running?")
            input("\nPress Enter to continue...")
            continue

        if not c.isdigit():
            print("❌ Enter a number.")
            input("\nPress Enter to continue...")
            continue

        ci = int(c)
        if ci < 1 or ci > len(OLLAMA_INSTALL_CATALOG):
            print("❌ Invalid category.")
            input("\nPress Enter to continue...")
            continue

        cat = OLLAMA_INSTALL_CATALOG[ci - 1]
        clear_screen()
        print_header()
        print(f"🎯 {cat['title']}\n")
        print(f"{'#':<4} {'MODEL REF':<40} {'~DISK':<12} DETAIL")
        print("=" * 70)
        for j, m in enumerate(cat["models"], 1):
            ref = m["ref"]
            ref_disp = ref[:39] + "…" if len(ref) > 39 else ref
            print(f"{j:<4} {ref_disp:<40} {m.get('disk', ''):<12} {m.get('detail', '')}")
        print("=" * 70)
        print("  [0] Back to categories\n")

        try:
            v = input("Variant number (0 = back): ").strip()
        except (EOFError, KeyboardInterrupt):
            continue

        if v == "0":
            continue
        if not v.isdigit():
            print("❌ Enter a number.")
            input("\nPress Enter to continue...")
            continue
        vi = int(v)
        if vi < 1 or vi > len(cat["models"]):
            print("❌ Invalid variant.")
            input("\nPress Enter to continue...")
            continue

        ref = cat["models"][vi - 1]["ref"]
        print(f"\nSelected: {ref}")
        print("  [1] Pull only (ollama pull) — recommended")
        print("  [2] Pull and open chat (ollama run) — starts interactive session here\n")
        mode = input("Choose (1-2, default 1): ").strip() or "1"

        if mode == "2":
            print(f"\n⏳ Starting ollama run {ref} ...\n")
            subprocess.run(["ollama", "run", ref], shell=False)
        else:
            code = run_ollama_pull(ref)
            if code == 0:
                print("\n✅ Pull finished successfully.")
                print("Run  ollama list  to see exact sizes.")
                print(f"Chat:  ollama run {ref}\n")
            else:
                print(f"\n❌ ollama pull exited with code {code}. Is Ollama installed and serving?")

        input("\nPress Enter to continue...")


def show_system_info():
    """Show system information"""
    clear_screen()
    print_header()
    print("📊 System Information:\n")
    
    print(f"Python Available:    {'✅ Yes' if check_python() else '❌ No'}")
    print(f"PowerShell Available: {'✅ Yes' if check_powershell() else '❌ No (Windows only)'}")
    print(f"Ollama Running:       {'✅ Yes' if check_ollama() else '❌ No'}")
    print()
    
    print("Project Structure:")
    print(f"  modules/web_gui/          {'✅' if Path('modules/web_gui').exists() else '❌'}")
    print(f"  modules/terminal_ui/      {'✅' if Path('modules/terminal_ui').exists() else '❌'}")
    print(f"  modules/chat_interfaces/  {'✅' if Path('modules/chat_interfaces').exists() else '❌'}")
    print(f"  modules/utils/            {'✅' if Path('modules/utils').exists() else '❌'}")
    print(f"  config/                   {'✅' if Path('config').exists() else '❌'}")
    print(f"  uploads/                  {'✅' if Path('uploads').exists() else '❌'}")
    print()
    
    input("Press Enter to return to menu...")

def show_advanced_menu():
    """Show advanced options menu"""
    while True:
        clear_screen()
        print_header()
        print("🔧 Advanced Options:\n")
        print("  [1] View Conversation History")
        print("  [2] Check Ollama Models")
        print("  [3] Update from GitHub")
        print("  [4] View System Information")
        print("  [5] Setup Dependencies")
        print("  [6] Return to Main Menu\n")
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                view_conversation_history()
            elif choice == '2':
                check_ollama_models()
            elif choice == '3':
                update_from_github()
            elif choice == '4':
                show_system_info()
            elif choice == '5':
                setup_dependencies()
            elif choice == '6':
                break
            else:
                input("\n❌ Invalid choice. Press Enter to try again...")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue...")

def check_ollama_models():
    """Check available Ollama models (API + `ollama list` for sizes)"""
    clear_screen()
    print_header()
    print("Checking available Ollama models...\n")

    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print("From API (localhost:11434):")
                for model in models:
                    print(f"  • {model.get('name', 'Unknown')}")
            else:
                print("❌ No models in API response. Use [7] to pull models.")
        else:
            print("❌ Could not fetch models from API")
    except Exception as e:
        print(f"❌ API error: {e}")

    print()
    try:
        vr = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if vr.returncode == 0 and vr.stdout.strip():
            print("Exact names & sizes (`ollama list`):")
            print(vr.stdout.rstrip())
        elif vr.returncode != 0:
            print("Could not run `ollama list` (is Ollama installed and in PATH?)")
            if vr.stderr.strip():
                print(vr.stderr.strip())
    except FileNotFoundError:
        print("`ollama` CLI not found in PATH.")
    except Exception as e:
        print(f"`ollama list` error: {e}")

    input("\nPress Enter to continue...")

def update_from_github():
    """Update repository from GitHub"""
    clear_screen()
    print_header()
    print("📥 Updating from GitHub...\n")
    
    try:
        print("Pulling latest changes from origin...")
        os.system('git pull origin main')
        print("\n✅ Update completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def view_conversation_history():
    """View recent conversations"""
    clear_screen()
    print_header()
    print("📜 Recent Conversations:\n")
    
    try:
        history_file = Path('config/conversation_log.json')
        if history_file.exists():
            import json
            with open(history_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    recent = data[-5:] if len(data) > 5 else data
                    for i, entry in enumerate(recent, 1):
                        if isinstance(entry, dict):
                            msg = entry.get('user', 'Unknown')[:60]
                            timestamp = entry.get('timestamp', 'Unknown')
                            print(f"{i}. [{timestamp}]")
                            print(f"   User: {msg}...\n")
                    print(f"   Total conversations: {len(data)}\n")
                else:
                    print("❌ No conversations yet")
        else:
            print("❌ Conversation history not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("Press Enter to continue...")

def setup_dependencies():
    """Setup dependencies"""
    clear_screen()
    print_header()
    print("Setting up dependencies...\n")
    
    print("Installing Python packages...")
    print("  pip install -r requirements.txt\n")
    
    try:
        os.system('pip install -r requirements.txt')
        print("\n✅ Dependencies installed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def main():
    """Main launcher loop"""
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == '0':
                clear_screen()
                print("\n✨ Thank you for using LENLU LLM (emu)! ✨\n")
                break
            elif choice == '1':
                launch_web_gui()
            elif choice == '2':
                launch_terminal_ui()
            elif choice == '3':
                launch_chat_cli()
            elif choice == '4':
                launch_advanced_llm()
            elif choice == '5':
                start_ollama_server()
            elif choice == '6':
                install_ollama()
            elif choice == '7':
                pull_ollama_models()
            elif choice == '8':
                show_system_info()
            elif choice == '9':
                show_advanced_menu()
            else:
                input("\n❌ Invalid choice. Press Enter to try again...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n\n✨ Thank you for using LENLU LLM (emu)! ✨\n")
            print("ARUNESH ON INSTAGRAM: @lenlu_arun & @lenluarun\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

