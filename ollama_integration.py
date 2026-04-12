"""
LENLU AI+ - Ollama Integration Module
Enables LENLU to use local Ollama models
"""

import requests
import json
import os
from typing import Optional, Dict, List
import subprocess
import platform
import time

class OllamaIntegration:
    """Integration for Ollama models with LENLU"""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        """Initialize Ollama integration"""
        self.base_url = base_url
        self.timeout = timeout
        self.is_running = False
        
    def check_ollama_running(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            self.is_running = response.status_code == 200
            return self.is_running
        except (requests.ConnectionError, requests.Timeout):
            self.is_running = False
            return False
    
    def start_ollama_server(self) -> bool:
        """Start Ollama server on current platform"""
        try:
            if platform.system() == "Windows":
                paths = [
                    "C:\\Program Files\\Ollama\\ollama.exe",
                    os.path.expanduser("~\\AppData\\Local\\Programs\\Ollama\\ollama.exe"),
                    "ollama"
                ]
                for path in paths:
                    try:
                        subprocess.Popen(path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(3)
                        return self.check_ollama_running()
                    except (FileNotFoundError, OSError):
                        continue
                        
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)
                return self.check_ollama_running()
                
            else:  # Linux
                subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)
                return self.check_ollama_running()
                
        except Exception as e:
            print(f"Error starting Ollama: {e}")
        return False
    
    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            if response.status_code == 200:
                return [m["name"] for m in response.json().get("models", [])]
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull (download) a model from Ollama registry"""
        try:
            print(f"Pulling model: {model_name}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=300,  # Long timeout for downloads
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "status" in data:
                            print(f"  {data['status']}")
                print(f"✓ Model {model_name} pulled successfully")
                return True
            return False
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False
    
    def generate_completion(self, model: str, prompt: str, **kwargs) -> str:
        """Generate completion using Ollama model"""
        try:
            payload = {"model": model, "prompt": prompt, "stream": False, **kwargs}
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            print(f"Error: {response.status_code}")
            return ""
        except Exception as e:
            print(f"Error generating completion: {e}")
            return ""
    
    def generate_streaming(self, model: str, prompt: str, **kwargs):
        """Generate completion with streaming"""
        try:
            payload = {"model": model, "prompt": prompt, "stream": True, **kwargs}
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
            else:
                yield f"Error: {response.status_code}"
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def embed_text(self, model: str, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json={"model": model, "input": text},
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json().get("embedding", [])
            return []
        except Exception as e:
            print(f"Error embedding text: {e}")
            return []
    
    def get_model_info(self, model: str) -> Dict:
        """Get information about a model"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model},
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error getting model info: {e}")
            return {}


class LenluOllamaAdapter:
    """Adapter to use Ollama models within LENLU"""
    
    def __init__(self, ollama: OllamaIntegration, model_name: str = "llama3.1"):
        """Initialize LENLU Ollama adapter"""
        self.ollama = ollama
        self.model_name = model_name
        self.default_params = {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 256
        }
    
    def _build_prompt(self, question: str, context: str = "") -> str:
        """Build question/answer prompt"""
        return f"Context: {context}\n\nQuestion: {question}\n\nAnswer (concise):"
    
    def answer_question(self, question: str, context: str = "", **kwargs) -> str:
        """Answer a question using Ollama"""
        params = {**self.default_params, **kwargs}
        return self.ollama.generate_completion(
            self.model_name,
            self._build_prompt(question, context),
            **params
        )
    
    def stream_answer(self, question: str, context: str = "", **kwargs):
        """Stream answer from Ollama"""
        params = {**self.default_params, **kwargs}
        yield from self.ollama.generate_streaming(
            self.model_name,
            self._build_prompt(question, context),
            **params
        )


# Environment setup helper
def setup_ollama_environment():
    """Set up Ollama environment variables and paths"""
    
    # Set models directory
    if platform.system() == "Windows":
        models_dir = os.path.expanduser("~\\.ollama\\models")
    else:
        models_dir = os.path.expanduser("~/.ollama/models")
    
    os.environ["OLLAMA_MODELS"] = models_dir
    os.makedirs(models_dir, exist_ok=True)
    
    # Create local models symlink if needed
    local_models = os.path.join(os.path.dirname(__file__), "models", "ollama_models")
    os.makedirs(local_models, exist_ok=True)
    
    return {
        "models_dir": models_dir,
        "local_models": local_models,
        "status": "initialized"
    }
