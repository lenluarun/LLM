"""
LENLU AI+ Interface Launcher
Choose between Web GUI, Terminal CLI, or PowerShell Interface
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
    print("  LENLU AI+ Interface Launcher".center(70))
    print("  Ollama Chat - Multiple Interface Options".center(70))
    print("=" * 70)
    print()

def print_menu():
    """Print main menu"""
    print_header()
    print("Select your preferred interface:\n")
    print("  [1] Web GUI        - Beautiful localhost web interface")
    print("  [2] Terminal CLI   - Python Rich styled terminal interface")
    print("  [3] PowerShell CLI - Windows PowerShell styled interface")
    print("  [4] Quick Chat     - Simple Ollama chat (Terminal)")
    print("  [5] Exit\n")

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass
    return False

def check_powershell():
    """Check if PowerShell is available"""
    try:
        result = subprocess.run(['powershell', '-Command', 'echo test'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass
    return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def install_flask():
    """Install Flask if not available"""
    try:
        import flask
        return True
    except ImportError:
        print("\n⚠️  Flask not installed. Installing...")
        os.system('pip install flask flask-cors')
        return True

def launch_web_gui():
    """Launch Flask web GUI"""
    clear_screen()
    print("Starting Web GUI...")
    print("=" * 70)
    
    if not install_flask():
        print("❌ Failed to install Flask")
        return
    
    if not check_ollama():
        print("⚠️  Ollama doesn't appear to be running!")
        print("Start Ollama with: ollama serve")
        input("\nPress Enter to continue...")
        return
    
    print("✓ Ollama is running")
    print("✓ Starting Flask server on http://localhost:5000")
    print("\nOpen your browser and navigate to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        time.sleep(1)
        os.system('python app.py')
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")

def launch_terminal_cli():
    """Launch Terminal Interface"""
    clear_screen()
    print("Starting Terminal Interface...")
    print("=" * 70)
    print()
    
    if not check_ollama():
        print("⚠️  Ollama doesn't appear to be running!")
        print("Start Ollama with: ollama serve")
        input("\nPress Enter to continue...")
        return
    
    print("✓ Starting LENLU Terminal Interface\n")
    time.sleep(1)
    
    try:
        os.system('python terminal_interface.py')
    except Exception as e:
        print(f"Error: {e}")

def launch_powershell_cli():
    """Launch PowerShell Interface"""
    clear_screen()
    print("Starting PowerShell Interface...")
    print("=" * 70)
    print()
    
    if not check_powershell():
        print("❌ PowerShell not available on this system")
        input("\nPress Enter to continue...")
        return
    
    if not check_ollama():
        print("⚠️  Ollama doesn't appear to be running!")
        print("Start Ollama with: ollama serve")
        input("\nPress Enter to continue...")
        return
    
    print("✓ Starting PowerShell Interface\n")
    time.sleep(1)
    
    try:
        os.system('powershell -ExecutionPolicy Bypass -File ollama_chat.ps1')
    except Exception as e:
        print(f"Error: {e}")

def launch_quick_chat():
    """Launch quick Ollama chat"""
    clear_screen()
    print("Starting Quick Chat...")
    print("=" * 70)
    print()
    
    if not check_ollama():
        print("⚠️  Ollama is not running!")
        print("Start Ollama with: ollama serve")
        input("\nPress Enter to continue...")
        return
    
    print("✓ Starting Ollama Chat\n")
    time.sleep(1)
    
    try:
        os.system('python ollama_chat_interface.py')
    except Exception as e:
        print(f"Error: {e}")

def show_system_info():
    """Show system information"""
    clear_screen()
    print_header()
    print("System Information:")
    print()
    
    print(f"Python Available:    {'✓ Yes' if check_python() else '✗ No'}")
    print(f"PowerShell Available: {'✓ Yes' if check_powershell() else '✗ No'}")
    print(f"Ollama Running:       {'✓ Yes' if check_ollama() else '✗ No (Run: ollama serve)'}")
    print()
    
    # Check files exist
    print("Interface Files:")
    print(f"  app.py:                    {'✓' if Path('app.py').exists() else '✗'}")
    print(f"  terminal_interface.py:     {'✓' if Path('terminal_interface.py').exists() else '✗'}")
    print(f"  ollama_chat_interface.py:  {'✓' if Path('ollama_chat_interface.py').exists() else '✗'}")
    print(f"  ollama_chat.ps1:           {'✓' if Path('ollama_chat.ps1').exists() else '✗'}")
    print()
    
    input("Press Enter to return to menu...")

def main():
    """Main launcher loop"""
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                launch_web_gui()
            elif choice == '2':
                launch_terminal_cli()
            elif choice == '3':
                launch_powershell_cli()
            elif choice == '4':
                launch_quick_chat()
            elif choice == '5':
                clear_screen()
                print("\n✨ Thank you for using LENLU AI+! ✨\n")
                break
            else:
                input("\n❌ Invalid choice. Press Enter to try again...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n\n✨ Thank you for using LENLU AI+! ✨\n")
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
