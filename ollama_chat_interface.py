"""
LENLU AI+ Ollama Chat Interface
Styled chat interface with terminal clearing and persistent conversation logging
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich import box
import json
import os
from datetime import datetime
from typing import Optional, List, Dict
import requests
import subprocess
import sys

class OllamaChatInterface:
    """Styled Ollama chat with terminal clearing and history tracking"""
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.console = Console()
        self.ollama_host = ollama_host
        self.conversation_log_file = "conversation_log.json"
        self.chat_history = []
        self.current_model = "lenlu"  # Default model
        self.load_conversation_history()
    
    def clear_screen(self):
        """Clear terminal screen"""
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
    
    def print_header(self, title: str = "LENLU AI+ Ollama Chat"):
        """Print styled header"""
        header = Text(title, style="bold cyan", justify="center")
        panel = Panel(
            header,
            title="[bold magenta]OLLAMA[/]",
            subtitle=f"[yellow]Model: {self.current_model}[/]",
            border_style="bright_blue",
            expand=False,
            padding=(1, 15)
        )
        self.console.print(panel)
    
    def load_conversation_history(self):
        """Load existing conversation history from file"""
        if os.path.exists(self.conversation_log_file):
            try:
                with open(self.conversation_log_file, 'r') as f:
                    self.chat_history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.chat_history = []
    
    def save_conversation_history(self):
        """Save conversation history to file"""
        try:
            with open(self.conversation_log_file, 'w') as f:
                json.dump(self.chat_history, f, indent=2)
        except IOError as e:
            self.console.print(f"[bold red]Error saving history: {e}[/]")
    
    def add_to_history(self, user_input: str, response: str, model: str):
        """Add conversation to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "user": user_input,
            "assistant": response
        }
        self.chat_history.append(entry)
        self.save_conversation_history()
    
    def query_ollama(self, prompt: str) -> Optional[str]:
        """Query Ollama API"""
        try:
            url = f"{self.ollama_host}/api/generate"
            payload = {
                "model": self.current_model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"Error: {response.status_code} - {response.text}"
        
        except requests.exceptions.ConnectionError:
            return "[bold red]Error: Cannot connect to Ollama. Make sure Ollama is running.[/]"
        except Exception as e:
            return f"[bold red]Error: {str(e)}[/]"
    
    def check_ollama_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            url = f"{self.ollama_host}/api/tags"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get("models", []):
                    models.append(model.get("name", "unknown"))
                return models
            else:
                return []
        except:
            return []
    
    def select_model(self):
        """Interactive model selection"""
        self.clear_screen()
        self.print_header("Select Model")
        
        models = self.list_available_models()
        
        if not models:
            self.console.print("[bold red]No models available![/]")
            self.console.print("[yellow]Trying to use 'lenlu' model as default...[/]")
            self.current_model = "lenlu"
            return
        
        self.console.print("[bold cyan]Available Models:[/]\n")
        
        for idx, model in enumerate(models, 1):
            marker = "✓" if model == self.current_model else " "
            self.console.print(f"  [bold cyan][{marker}][/] {idx}. {model}")
        
        self.console.print()
        
        try:
            choice = int(input("[bold yellow]Select model (1-{}): [/]".format(len(models))))
            if 1 <= choice <= len(models):
                self.current_model = models[choice - 1]
                self.console.print(f"[bold green]✓ Selected: {self.current_model}[/]")
            else:
                self.console.print("[bold yellow]Invalid choice, keeping current model[/]")
        except ValueError:
            self.console.print("[bold yellow]Invalid input, keeping current model[/]")
        
        input("[bold yellow]Press Enter to continue...[/]")
    
    def print_message(self, role: str, content: str):
        """Print formatted message"""
        if role.lower() == "user":
            self.console.print(f"\n[bold cyan]You:[/]")
            self.console.print(f"[white]{content}[/]\n")
        elif role.lower() == "assistant":
            self.console.print(f"[bold green]Assistant:[/]")
            self.console.print(f"[cyan]{content}[/]\n")
    
    def show_conversation_summary(self):
        """Display conversation summary"""
        self.clear_screen()
        self.print_header("Conversation Summary")
        
        if not self.chat_history:
            self.console.print("[bold yellow]No conversations yet![/]")
            input("[bold yellow]Press Enter to continue...[/]")
            return
        
        total = len(self.chat_history)
        models_used = set()
        
        for entry in self.chat_history:
            models_used.add(entry.get("model", "unknown"))
        
        self.console.print(f"\n[bold cyan]Total Conversations:[/] {total}")
        self.console.print(f"[bold cyan]Models Used:[/] {', '.join(models_used)}")
        
        self.console.print("\n[bold yellow]Recent Conversations:[/]\n")
        
        for idx, entry in enumerate(self.chat_history[-10:], 1):
            timestamp = entry.get("timestamp", "unknown")
            model = entry.get("model", "unknown")
            user_msg = entry.get("user", "")[:50] + "..." if len(entry.get("user", "")) > 50 else entry.get("user", "")
            
            self.console.print(f"  [bold cyan][{idx}[/]] [{model}] {timestamp}")
            self.console.print(f"      Q: {user_msg}")
        
        input("[bold yellow]Press Enter to continue...[/]")
    
    def view_conversation_history(self):
        """View full conversation history"""
        self.clear_screen()
        self.print_header("Conversation History")
        
        if not self.chat_history:
            self.console.print("[bold yellow]No conversations yet![/]")
            input("[bold yellow]Press Enter to continue...[/]")
            return
        
        for idx, entry in enumerate(self.chat_history, 1):
            timestamp = entry.get("timestamp", "unknown")
            model = entry.get("model", "unknown")
            user_msg = entry.get("user", "")
            assistant_msg = entry.get("assistant", "")
            
            self.console.print(f"\n[bold cyan]Conversation {idx}[/] - [{model}] {timestamp}")
            self.console.print(f"[bold yellow]Q:[/] {user_msg}")
            self.console.print(f"[bold green]A:[/] {assistant_msg[:200]}...\n")
        
        input("[bold yellow]Press Enter to continue...[/]")
    
    def export_conversation(self):
        """Export conversation to formatted file"""
        self.clear_screen()
        self.print_header("Export Conversation")
        
        if not self.chat_history:
            self.console.print("[bold yellow]No conversations to export![/]")
            input("[bold yellow]Press Enter to continue...[/]")
            return
        
        filename = input("[bold yellow]Enter export filename (without .txt): [/]")
        filename = f"{filename}_export.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("LENLU AI+ Ollama Chat Export\n")
                f.write("=" * 80 + "\n\n")
                
                for idx, entry in enumerate(self.chat_history, 1):
                    f.write(f"Conversation {idx}\n")
                    f.write(f"Timestamp: {entry.get('timestamp', 'unknown')}\n")
                    f.write(f"Model: {entry.get('model', 'unknown')}\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"Question:\n{entry.get('user', '')}\n\n")
                    f.write(f"Answer:\n{entry.get('assistant', '')}\n")
                    f.write("=" * 80 + "\n\n")
            
            self.console.print(f"[bold green]✓ Exported to {filename}[/]")
        except IOError as e:
            self.console.print(f"[bold red]✗ Error exporting: {e}[/]")
        
        input("[bold yellow]Press Enter to continue...[/]")
    
    def clear_history(self):
        """Clear conversation history (with confirmation)"""
        self.clear_screen()
        self.print_header("Clear History")
        
        self.console.print("[bold yellow]⚠ WARNING: This will delete all conversation history![/]")
        confirm = input("[bold red]Type 'YES' to confirm: [/]")
        
        if confirm.upper() == "YES":
            self.chat_history = []
            self.save_conversation_history()
            self.console.print("[bold green]✓ Conversation history cleared[/]")
        else:
            self.console.print("[bold yellow]Cancelled[/]")
        
        input("[bold yellow]Press Enter to continue...[/]")
    
    def chat_loop(self):
        """Main chat loop"""
        while True:
            self.clear_screen()
            self.print_header()
            
            self.console.print("[bold cyan]Command Menu:[/]")
            self.console.print("  [bold green]ask[/] - Ask a question")
            self.console.print("  [bold green]model[/] - Change model")
            self.console.print("  [bold green]history[/] - View conversation history")
            self.console.print("  [bold green]summary[/] - View summary")
            self.console.print("  [bold green]export[/] - Export conversations")
            self.console.print("  [bold green]clear[/] - Clear history")
            self.console.print("  [bold green]quit[/] - Exit")
            self.console.print()
            
            command = input("[bold yellow]Enter command: [/]").strip().lower()
            
            if command == "ask":
                self.clear_screen()
                self.print_header()
                user_input = input("[bold cyan]Ask me anything: [/]")
                
                if user_input.strip():
                    self.clear_screen()
                    self.print_header()
                    self.print_message("user", user_input)
                    
                    self.console.print("[bold yellow]Thinking...[/]")
                    response = self.query_ollama(user_input)
                    
                    if response:
                        self.print_message("assistant", response)
                        self.add_to_history(user_input, response, self.current_model)
                    else:
                        self.console.print("[bold red]No response from model[/]")
                    
                    input("[bold yellow]Press Enter to continue...[/]")
            
            elif command == "model":
                self.select_model()
            
            elif command == "history":
                self.view_conversation_history()
            
            elif command == "summary":
                self.show_conversation_summary()
            
            elif command == "export":
                self.export_conversation()
            
            elif command == "clear":
                self.clear_history()
            
            elif command == "quit":
                self.console.print("[bold green]Goodbye![/]\n")
                break
            
            else:
                self.console.print("[bold red]Unknown command[/]")
                input("[bold yellow]Press Enter to continue...[/]")
    
    def run(self):
        """Start the chat interface"""
        # Check if Ollama is running
        if not self.check_ollama_running():
            self.clear_screen()
            self.print_header("Ollama Status Check")
            self.console.print("[bold red]✗ Ollama is not running![/]")
            self.console.print("[bold yellow]Please start Ollama before using this interface[/]")
            self.console.print("\n[bold cyan]To start Ollama:[/]")
            self.console.print("  Windows: ollama serve")
            self.console.print("  Linux/Mac: ollama serve")
            input("[bold yellow]Press Enter to exit...[/]")
            return
        
        self.clear_screen()
        self.print_header()
        self.console.print("[bold green]✓ Ollama is running![/]")
        self.console.print("[bold yellow]Loading interface...[/]")
        
        import time
        time.sleep(1)
        
        self.chat_loop()


def main():
    """Main entry point"""
    chat = OllamaChatInterface()
    chat.run()


if __name__ == "__main__":
    main()
