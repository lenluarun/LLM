"""
Stylized Terminal Interface for LENLU LLM (emu) Project
Enhanced CLI with Rich library for better UX
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.text import Text
from rich.syntax import Syntax
from rich import box
import time
from datetime import datetime
from typing import Optional, List, Dict
import os

class StyledTerminal:
    """Enhanced terminal interface with rich styling"""
    
    def __init__(self):
        self.console = Console()
        self.width = 100
        
    def print_header(self, title: str, subtitle: Optional[str] = None):
        """Print a styled header"""
        header_text = Text(title, style="bold cyan", justify="center")
        panel = Panel(
            header_text,
            title="[bold magenta]LENLU LLM (emu)[/]",
            subtitle=f"[yellow]{subtitle}[/]" if subtitle else None,
            border_style="bright_blue",
            expand=False,
            padding=(1, 10)
        )
        self.console.print(panel)
    
    def print_section(self, title: str):
        """Print a styled section header"""
        divider = "━" * self.width
        self.console.print(f"\n[bold cyan]{divider}[/]")
        self.console.print(f"[bold yellow]▶ {title}[/]")
        self.console.print(f"[bold cyan]{divider}[/]\n")
    
    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"[bold green]✓[/] {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"[bold red]✗[/] {message}")
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"[bold blue]ℹ[/] {message}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        self.console.print(f"[bold yellow]⚠[/] {message}")
    
    def create_status_table(self, data: Dict[str, str]) -> Table:
        """Create a styled status table"""
        table = Table(
            title="[bold cyan]Status Report[/]",
            box=box.DOUBLE_EDGE,
            border_style="bright_blue",
            padding=(0, 1),
            expand=False
        )
        
        table.add_column("Property", style="cyan", width=25)
        table.add_column("Value", style="yellow", width=50)
        
        for key, value in data.items():
            table.add_row(key, value)
        
        return table
    
    def create_feature_table(self, features: List[Dict[str, str]]) -> Table:
        """Create a features table"""
        table = Table(
            title="[bold cyan]Features[/]",
            box=box.HEAVY_HEAD,
            border_style="bright_green",
            padding=(0, 1)
        )
        
        table.add_column("Feature", style="green", width=30)
        table.add_column("Description", style="white", width=60)
        
        for feature in features:
            table.add_row(feature.get("name", ""), feature.get("desc", ""))
        
        return table
    
    def show_progress(self, title: str, total: int):
        """Display progress bar"""
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]{title}", total=total)
            for i in range(total):
                time.sleep(0.1)
                progress.update(task, advance=1)
    
    def create_menu(self, title: str, options: List[str]) -> int:
        """Display interactive menu"""
        self.print_section(title)
        
        for idx, option in enumerate(options, 1):
            self.console.print(f"  [bold cyan][{idx}][/] {option}")
        
        self.console.print()
        while True:
            try:
                choice = input("[bold yellow]Enter choice (1-{}): [/]".format(len(options)))
                choice = int(choice)
                if 1 <= choice <= len(options):
                    return choice
                else:
                    self.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                self.print_error("Invalid input. Please enter a number.")
    
    def show_project_dashboard(self):
        """Display a comprehensive project dashboard"""
        self.print_header("LENLU AI+ Dashboard", "Interactive Terminal Interface")
        
        # Project Stats
        stats = {
            "Project": "LENLU AI+ with Ollama Integration",
            "Version": "1.0.0",
            "Status": "[green]Active[/]",
            "Last Update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Python Version": "3.11+",
            "Framework": "PyTorch + Transformers"
        }
        
        self.console.print(self.create_status_table(stats))
        
        # Features
        features = [
            {
                "name": "AI Plus Training",
                "desc": "Advanced machine learning model training"
            },
            {
                "name": "Ollama Integration",
                "desc": "Seamless Ollama model management"
            },
            {
                "name": "Knowledge Base",
                "desc": "Comprehensive knowledge management system"
            },
            {
                "name": "User Training",
                "desc": "Personalized model training from user data"
            },
            {
                "name": "Conversation Logging",
                "desc": "Track and analyze all conversations"
            }
        ]
        
        self.console.print("\n")
        self.console.print(self.create_feature_table(features))
    
    def show_module_info(self):
        """Display module information"""
        self.print_section("Project Modules")
        
        modules = {
            "lenlu_ai_plus.py": "Core AI+ implementation with advanced training",
            "lenlu_ollama.py": "Ollama integration and model management",
            "ollama_integration.py": "Ollama API wrapper and utilities",
            "user_training_system.py": "User-based model training system",
            "verify_ollama_setup.py": "Ollama setup verification tool",
            "setup_ollama.py": "Automated Ollama setup script"
        }
        
        for module, description in modules.items():
            self.console.print(f"  [bold cyan]►[/] [yellow]{module}[/]")
            self.console.print(f"      {description}\n")
    
    def show_quick_commands(self):
        """Display quick command reference"""
        self.print_section("Quick Commands")
        
        commands = {
            "python lenlu_ai_plus.py": "Start AI+ training",
            "python lenlu_ollama.py": "Run Ollama integration",
            "python verify_ollama_setup.py": "Verify Ollama setup",
            "python setup_ollama.py": "Setup Ollama automatically",
            "python user_training_system.py": "Train with user data"
        }
        
        for cmd, desc in commands.items():
            self.console.print(f"  [bold green]$[/] [cyan]{cmd}[/]")
            self.console.print(f"    └─ {desc}\n")
    
    def show_main_menu(self):
        """Display main interactive menu"""
        while True:
            self.console.clear()
            self.show_project_dashboard()
            
            options = [
                "View Module Information",
                "Quick Commands Reference",
                "System Status",
                "Run Training",
                "Ollama Management",
                "Exit"
            ]
            
            choice = self.create_menu("Main Menu", options)
            
            if choice == 1:
                self.show_module_info()
            elif choice == 2:
                self.show_quick_commands()
            elif choice == 3:
                self.show_system_status()
            elif choice == 4:
                self.print_info("Starting AI+ training...")
                self.show_progress("Training Progress", 50)
                self.print_success("Training completed!")
            elif choice == 5:
                self.print_info("Ollama management options")
                time.sleep(1)
            elif choice == 6:
                self.print_success("Thank you for using LENLU AI+!")
                break
            
            input("[bold yellow]Press Enter to continue...[/]")
    
    def show_system_status(self):
        """Display system status"""
        self.print_section("System Status")
        
        status_data = {
            "Python Path": os.sys.executable,
            "Current Directory": os.getcwd(),
            "Project Root": os.path.dirname(os.path.abspath(__file__)),
            "Virtual Environment": "Active" if hasattr(os.sys, "real_prefix") else "Not Active",
            "Timestamp": datetime.now().isoformat()
        }
        
        self.console.print(self.create_status_table(status_data))


class PowerShellStyled:
    """PowerShell-themed terminal interface"""
    
    def __init__(self):
        self.console = Console()
    
    def print_powershell_header(self):
        """Print PowerShell-style header"""
        ps_banner = """
        ╔═══════════════════════════════════════╗
        ║    LENLU AI+ PowerShell Interface     ║
        ║   Enhanced Terminal Management Tool   ║
        ╚═══════════════════════════════════════╝
        """
        self.console.print(ps_banner, style="bold cyan")
    
    def execute_command_style(self, command: str, output: str):
        """Display command execution in PowerShell style"""
        self.console.print(f"[cyan]PS>[/] [yellow]{command}[/]")
        self.console.print(f"[green]{output}[/]\n")
    
    def show_commands_menu(self):
        """Show available PowerShell commands"""
        self.print_powershell_header()
        
        commands = [
            ("training-start", "Start AI+ training process"),
            ("ollama-check", "Check Ollama status"),
            ("knowledge-load", "Load knowledge base"),
            ("conversation-log", "View conversation logs"),
            ("system-info", "Display system information"),
            ("help", "Show help information"),
            ("exit", "Exit the program")
        ]
        
        self.console.print("[bold cyan]Available Commands:[/]\n")
        
        for cmd, desc in commands:
            self.console.print(f"  [bold green]{cmd:<20}[/] {desc}")
        
        self.console.print()


def main():
    """Main entry point"""
    import sys
    
    terminal = StyledTerminal()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--powershell":
        ps = PowerShellStyled()
        ps.show_commands_menu()
    else:
        terminal.show_main_menu()


if __name__ == "__main__":
    main()
