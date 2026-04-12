"""
LENLU AI+ Ollama Web GUI
Beautiful Flask-based web interface for Ollama chat with localStorage persistence
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime
import requests
from typing import Dict, List, Optional
import uuid

app = Flask(__name__)
app.secret_key = 'lenlu_ollama_secret_key_2024'
CORS(app)

# Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
CONVERSATION_LOG = 'conversation_log.json'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global state
chat_sessions = {}
conversation_history = []

def load_conversations():
    """Load conversation history from file"""
    global conversation_history
    if os.path.exists(CONVERSATION_LOG):
        try:
            with open(CONVERSATION_LOG, 'r') as f:
                conversation_history = json.load(f)
        except (json.JSONDecodeError, IOError):
            conversation_history = []
    else:
        conversation_history = []

def save_conversations():
    """Save conversation history to file"""
    try:
        with open(CONVERSATION_LOG, 'w') as f:
            json.dump(conversation_history, f, indent=2)
    except IOError:
        pass

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [m.get('name', 'unknown') for m in models]
    except:
        pass
    return []

def query_ollama(prompt: str, model: str) -> Optional[str]:
    """Query Ollama API"""
    try:
        payload = {
            'model': model,
            'prompt': prompt,
            'stream': False
        }
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=300
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return None
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check service status"""
    return jsonify({
        'ollama_running': check_ollama_running(),
        'models': get_available_models()
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat endpoint"""
    data = request.json
    message = data.get('message', '').strip()
    model = data.get('model', 'lenlu')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    if not message:
        return jsonify({'error': 'Empty message'}), 400
    
    response = query_ollama(message, model)
    
    if response:
        # Add to history
        entry = {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'session_id': session_id,
            'user': message,
            'assistant': response
        }
        conversation_history.append(entry)
        save_conversations()
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': entry['timestamp']
        })
    
    return jsonify({'error': 'No response from model'}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """Get conversation history"""
    return jsonify(conversation_history)

@app.route('/api/history/<session_id>', methods=['GET'])
def api_session_history(session_id):
    """Get specific session history"""
    session_chats = [c for c in conversation_history if c.get('session_id') == session_id]
    return jsonify(session_chats)

@app.route('/api/summary', methods=['GET'])
def api_summary():
    """Get chat summary statistics"""
    models_used = set(c.get('model') for c in conversation_history)
    return jsonify({
        'total_chats': len(conversation_history),
        'models_used': list(models_used),
        'unique_sessions': len(set(c.get('session_id') for c in conversation_history))
    })

@app.route('/api/export', methods=['GET'])
def api_export():
    """Export all conversations"""
    filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, 'w') as f:
        json.dump(conversation_history, f, indent=2)
    
    return jsonify({
        'filename': filename,
        'path': f'/uploads/{filename}'
    })

@app.route('/api/clear-history', methods=['POST'])
def api_clear_history():
    """Clear conversation history"""
    global conversation_history
    confirm = request.json.get('confirm', False)
    
    if confirm:
        conversation_history = []
        save_conversations()
        return jsonify({'status': 'cleared'})
    
    return jsonify({'error': 'Confirmation required'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    load_conversations()
    print("=" * 60)
    print("LENLU AI+ Ollama Web GUI")
    print("=" * 60)
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"Server: http://localhost:5000")
    print("=" * 60)
    app.run(debug=False, host='localhost', port=5000)
