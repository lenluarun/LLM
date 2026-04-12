"""
LENLU AI+ with Ollama Integration
Advanced LLM with local Ollama model support and hybrid response generation
"""

import json
import os
from typing import Optional

from ollama_integration import OllamaIntegration, LenluOllamaAdapter, setup_ollama_environment

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

if HAS_RICH:
    console = Console()


class LenluWithOllama:
    """LENLU AI+ with Ollama model integration"""
    
    def __init__(self, use_ollama: bool = False, ollama_model: str = "llama3.1"):
        """
        Initialize LENLU with optional Ollama support
        
        Args:
            use_ollama: Enable Ollama model usage
            ollama_model: Model to use from Ollama
        """
        self.use_ollama = use_ollama
        self.ollama_model = ollama_model
        self.config = self._load_config()
        self.ollama = None
        self.ollama_adapter = None
        
        # Initialize original LENLU if not using Ollama only
        self.lenlu = None
        if not use_ollama:
            from lenlu_ai_plus import AIEnhancedLENLU
            self.lenlu = AIEnhancedLENLU(model_name="t5-base", use_learning=True)
        
        # Initialize Ollama if requested
        if use_ollama:
            self._setup_ollama()
    
    def _print(self, text: str):
        """Print text with Rich or fallback"""
        if HAS_RICH:
            console.print(text)
        else:
            print(text)
    
    def _input(self, prompt: str) -> str:
        """Get user input with Rich or fallback"""
        if HAS_RICH:
            return console.input(prompt).strip()
        else:
            return input(prompt).strip()
    
    def _load_config(self) -> dict:
        """Load Ollama configuration"""
        try:
            with open("ollama_config.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
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
    
    def _setup_ollama(self) -> bool:
        """Set up Ollama integration"""
        self._print("[cyan]Setting up Ollama integration...[/cyan]")
        
        # Initialize environment
        env_setup = setup_ollama_environment()
        self._print(f"[green]✓ Models directory:[/green] {env_setup['models_dir']}")
        
        # Create Ollama integration
        self.ollama = OllamaIntegration(
            base_url=self.config["ollama"]["server_url"],
            timeout=self.config["ollama"]["timeout"]
        )
        
        # Check/start Ollama server
        if not self.ollama.check_ollama_running():
            self._print("[yellow]⚠ Ollama server not running[/yellow]")
            if self.config["ollama"]["auto_start"] and self.ollama.start_ollama_server():
                self._print("[green]✓ Ollama server started[/green]")
            else:
                self._print("[red]✗ Could not start Ollama[/red]")
                return False
        else:
            self._print("[green]✓ Ollama server running[/green]")
        
        # Check models
        models = self.ollama.list_models()
        self._print(f"[cyan]Available models: {', '.join(models) if models else 'None'}[/cyan]")
        
        # Pull model if needed
        if self.ollama_model not in models:
            self._print(f"[yellow]Pulling model {self.ollama_model}...[/yellow]")
            if not self.ollama.pull_model(self.ollama_model):
                self._print(f"[red]✗ Failed to pull {self.ollama_model}[/red]")
                return False
            self._print(f"[green]✓ Model {self.ollama_model} ready[/green]")
        
        # Create adapter
        self.ollama_adapter = LenluOllamaAdapter(self.ollama, self.ollama_model)
        return True
    
    def display_welcome(self):
        """Display welcome banner"""
        if HAS_RICH:
            mode = "Ollama" if self.use_ollama else "T5"
            banner = Panel(
                Text(f"🤖 LENLU AI+ with {mode} 🤖\n", style="bold magenta") +
                Text(f"Advanced LLM | {self.ollama_model if self.use_ollama else 't5-base'}\n", style="dim magenta") +
                Text("4GB+ Knowledge • AI Learning • Hybrid Mode", style="cyan"),
                border_style="magenta"
            )
            console.print(banner)
            
            status = Text()
            status.append("Status: ", style="bold cyan")
            status.append("Ollama Online ✓" if self.use_ollama else "T5 Active ✓", style="green")
            console.print(Align.center(status))
            console.print()
    
    def generate_response(self, query: str) -> str:
        """Generate response using optimal strategy"""
        if self.use_ollama and self.ollama_adapter:
            # Use Ollama model
            context = self._get_context(query) if hasattr(self, 'lenlu') and self.lenlu else ""
            return self.ollama_adapter.answer_question(query, context)
        elif self.lenlu:
            # Fall back to T5 + knowledge base
            return self.lenlu.generate_response(query)
        else:
            return "Error: No language model available"
    
    def _get_context(self, query: str) -> str:
        """Get context from LENLU's knowledge base"""
        if self.lenlu:
            return self.lenlu.retrieve_intelligent_context(query)
        return ""
    
    def stream_response(self, query: str):
        """Stream response from Ollama model"""
        if self.use_ollama and self.ollama_adapter:
            context = self._get_context(query)
            yield from self.ollama_adapter.stream_answer(query, context)
        else:
            yield self.generate_response(query)
    
    def run_interactive(self):
        """Run interactive chat mode"""
        self.display_welcome()
        
        commands = "\n💡 Commands:\n  • Ask question | 'ollama' - Toggle | 'models' - List | 'quit' - Exit"
        self._print(commands)
        
        while True:
            try:
                user_input = self._input("[bold magenta]LENLU> [/bold magenta]" if HAS_RICH else "LENLU> ")
                
                if not user_input:
                    continue
                
                if user_input.lower() == "quit":
                    break
                elif user_input.lower() == "models" and self.ollama:
                    models = self.ollama.list_models()
                    self._print("[cyan]Available Ollama Models:[/cyan]")
                    for model in models:
                        self._print(f"  • {model}")
                elif user_input.lower() == "ollama":
                    self.use_ollama = not self.use_ollama
                    mode = "Ollama" if self.use_ollama else "T5"
                    self._print(f"[cyan]Switched to {mode} mode[/cyan]")
                    if self.use_ollama and not self.ollama:
                        self._setup_ollama()
                else:
                    response = self.generate_response(user_input)
                    if HAS_RICH:
                        response_panel = Panel(
                            Text(response, style="white"),
                            title="[bold magenta]🤖 LENLU[/bold magenta]",
                            border_style="magenta",
                            padding=(1, 2)
                        )
                        console.print(response_panel)
                    else:
                        print(f"\nLENLU: {response}\n")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                self._print(f"[red]Error: {str(e)}[/red]" if HAS_RICH else f"Error: {str(e)}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LENLU AI+ with Ollama Integration")
    parser.add_argument("--ollama", action="store_true", help="Use Ollama models")
    parser.add_argument("--model", default="llama3.1", help="Ollama model to use")
    parser.add_argument("--query", help="Single query mode (no interactive mode)")
    parser.add_argument("--stream", action="store_true", help="Stream responses")
    
    args = parser.parse_args()
    
    # Create LENLU instance
    lenlu = LenluWithOllama(use_ollama=args.ollama, ollama_model=args.model)
    
    # Single query mode
    if args.query:
        if args.stream and lenlu.use_ollama:
            for chunk in lenlu.stream_response(args.query):
                print(chunk, end="", flush=True)
            print()
        else:
            response = lenlu.generate_response(args.query)
            print(response)
    else:
        # Interactive mode
        lenlu.run_interactive()


if __name__ == "__main__":
    main()
