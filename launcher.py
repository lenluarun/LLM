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

def clear_screen():
    """Clear terminal"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def print_header():
    """Print styled header"""
    clear_screen()
    print("=" * 70)
    print("  LENLU LLM (emu) - Master Launcher".center(70))
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
    """Install Ollama"""
    clear_screen()
    print_header()
    print("📥 Ollama Installation Guide\n")
    
    if sys.platform == 'win32':
        print("Windows Installation:")
        print("  1. Download from: https://ollama.ai")
        print("  2. Or use Winget: winget install Ollama.Ollama")
        print("  3. Or use Chocolatey: choco install ollama\n")
    elif sys.platform == 'darwin':
        print("macOS Installation:")
        print("  1. Using Homebrew: brew install ollama")
        print("  2. Or download from: https://ollama.ai\n")
    else:
        print("Linux Installation:")
        print("  1. Run: curl -fsSL https://ollama.ai/install.sh | sh")
        print("  2. Or visit: https://ollama.ai\n")
    
    print("=" * 70)
    print("\nAfter installation:")
    print("  1. Open a terminal and run: ollama serve")
    print("  2. In another terminal: ollama pull llama2")
    print("  3. Then use the chat interfaces!")
    print("=" * 70 + "\n")
    
    input("Press Enter to continue...")

def pull_ollama_models():
    """Pull/Install Ollama models"""
    clear_screen()
    print_header()
    print("🎯 Ollama Model Installer\n")
    print("Available models:\n")
    print("  [1] llama2        - Meta's Llama 2 (70B parameters)")
    print("  [2] mistral       - Mistral 7B (fastest)")
    print("  [3] neural-chat   - Intel's Neural Chat")
    print("  [4] wizardlm      - WizardLM 13B")
    print("  [5] orca-mini     - Small but capable")
    print("  [6] Custom model (enter name)")
    print("  [0] Return to menu\n")
    
    try:
        choice = input("Select model to pull (0-6): ").strip()
        
        models = {
            '1': 'llama2',
            '2': 'mistral',
            '3': 'neural-chat',
            '4': 'wizardlm',
            '5': 'orca-mini'
        }
        
        if choice in models:
            model_name = models[choice]
            print(f"\n⏳ Pulling {model_name}... This may take several minutes.\n")
            os.system(f'ollama pull {model_name}')
            print("\n✅ Model downloaded successfully!")
        elif choice == '6':
            model_name = input("\nEnter model name (e.g., dolphin-mixtral): ").strip()
            if model_name:
                print(f"\n⏳ Pulling {model_name}... This may take several minutes.\n")
                os.system(f'ollama pull {model_name}')
                print("\n✅ Model download completed!")
        elif choice != '0':
            print("\n❌ Invalid choice!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
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
        print("  [3] Git Status")
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
                show_git_status()
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
    """Check available Ollama models"""
    clear_screen()
    print_header()
    print("Checking available Ollama models...\n")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print("Available Models:")
                for model in models:
                    print(f"  • {model.get('name', 'Unknown')}")
            else:
                print("❌ No models found. Use option [7] to pull models.")
        else:
            print("❌ Could not fetch models")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def show_git_status():
    """Show git repository status"""
    clear_screen()
    print_header()
    print("Git Repository Status:\n")
    
    try:
        os.system('git status')
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

