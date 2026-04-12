"""
LENLU LLM (emu) Ollama Web GUI
Beautiful Flask-based web interface for Ollama chat with localStorage persistence
Includes real-time terminal output streaming
"""

from flask import Flask, render_template, request, jsonify, session, Response
from flask_cors import CORS
import json
import os
from datetime import datetime
import requests
from typing import Dict, List, Optional
import uuid
import subprocess
import threading
from queue import Queue
import sys

app = Flask(__name__, template_folder='templates')
app.secret_key = 'lenlu_ollama_secret_key_2024'
CORS(app)

# Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
# Path to store conversation logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONVERSATION_LOG = os.path.join(BASE_DIR, 'config', 'conversation_log.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(CONVERSATION_LOG), exist_ok=True)

# Global state
chat_sessions = {}
conversation_history = []
output_queues = {}  # For streaming terminal output

def load_conversations():
    """Load conversation history from file"""
    global conversation_history
    if os.path.exists(CONVERSATION_LOG):
        try:
            with open(CONVERSATION_LOG, 'r') as f:
                data = json.load(f)
                # Handle both old dict format and new list format
                if isinstance(data, dict):
                    # Old format with "conversations" key
                    conversation_history = data.get('conversations', [])
                elif isinstance(data, list):
                    # New format - just a list
                    conversation_history = data
                else:
                    conversation_history = []
        except (json.JSONDecodeError, IOError):
            conversation_history = []
    else:
        conversation_history = []

def save_conversations():
    """Save conversation history to file"""
    try:
        # Save as simple list format
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
    # Filter out any non-dict entries
    valid_history = [c for c in conversation_history if isinstance(c, dict)]
    return jsonify(valid_history)

@app.route('/api/history/<session_id>', methods=['GET'])
def api_session_history(session_id):
    """Get specific session history"""
    session_chats = [c for c in conversation_history if isinstance(c, dict) and c.get('session_id') == session_id]
    return jsonify(session_chats)

@app.route('/api/summary', methods=['GET'])
def api_summary():
    """Get chat summary statistics"""
    # Filter out any non-dict entries first
    valid_history = [c for c in conversation_history if isinstance(c, dict)]
    models_used = set(c.get('model') for c in valid_history)
    return jsonify({
        'total_chats': len(valid_history),
        'models_used': list(models_used),
        'unique_sessions': len(set(c.get('session_id') for c in valid_history))
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

@app.route('/api/export-pdf', methods=['GET'])
def api_export_pdf():
    """Export conversations as a stylish PDF"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        
        filename = f"LENLU_LLM_Chat_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4B0082'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8
        )
        
        # Title
        title = Paragraph("LENLU LLM (emu) Chat Export", title_style)
        story.append(title)
        
        # Export info
        export_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        info_text = f"<b>Exported:</b> {export_time} | <b>Total Conversations:</b> {len(conversation_history)}"
        story.append(Paragraph(info_text, normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Add conversations
        valid_history = [c for c in conversation_history if isinstance(c, dict)]
        
        for idx, chat in enumerate(valid_history, 1):
            # Timestamp and model
            timestamp = chat.get('timestamp', 'Unknown')
            model = chat.get('model', 'Unknown')
            conversation = f"<b>[{model}] {timestamp}</b>"
            story.append(Paragraph(conversation, heading_style))
            
            # User message
            user_msg = chat.get('user', '')
            user_text = f"<b style='color:#667eea'>Q:</b> {user_msg[:500]}"
            story.append(Paragraph(user_text, normal_style))
            
            # Assistant response
            assistant_msg = chat.get('assistant', '')
            asst_text = f"<b style='color:#764ba2'>A:</b> {assistant_msg[:500]}"
            story.append(Paragraph(asst_text, normal_style))
            
            story.append(Spacer(1, 0.15*inch))
            
            # Page break every 5 conversations
            if idx % 5 == 0 and idx < len(valid_history):
                story.append(PageBreak())
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer_text = "<i>Generated by LENLU LLM (emu) - Your Advanced AI Assistant</i>"
        story.append(Paragraph(footer_text, normal_style))
        
        # Build PDF
        doc.build(story)
        
        return jsonify({
            'filename': filename,
            'path': f'/uploads/{filename}'
        })
    except ImportError:
        return jsonify({'error': 'PDF library not installed. Install with: pip install reportlab'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/run-chat', methods=['POST'])
def api_run_chat():
    """Run chat interface and stream terminal output"""
    session_id = str(uuid.uuid4())
    output_queues[session_id] = Queue()
    
    data = request.json
    command = data.get('command', 'python ollama_chat_interface.py')
    
    def run_command():
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                output_queues[session_id].put(line.rstrip('\n'))
            
            process.wait()
            output_queues[session_id].put('[PROCESS_COMPLETE]')
        except Exception as e:
            output_queues[session_id].put(f'Error: {str(e)}')
            output_queues[session_id].put('[PROCESS_COMPLETE]')
    
    thread = threading.Thread(target=run_command, daemon=True)
    thread.start()
    
    return jsonify({'session_id': session_id})

@app.route('/api/stream/<session_id>')
def api_stream(session_id):
    """Stream terminal output"""
    def generate():
        while True:
            if session_id in output_queues:
                try:
                    line = output_queues[session_id].get(timeout=1)
                    if line == '[PROCESS_COMPLETE]':
                        yield f'data: [COMPLETE]\n\n'
                        del output_queues[session_id]
                        break
                    yield f'data: {json.dumps({"line": line})}\n\n'
                except:
                    pass
            else:
                break
    
    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    })

@app.route('/api/terminal', methods=['POST'])
def api_terminal():
    """Execute terminal command and return output"""
    data = request.json
    command = data.get('command', '')
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timeout'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    load_conversations()
    print("=" * 60)
    print("LENLU LLM (emu) Ollama Web GUI")
    print("=" * 60)
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"Server: http://localhost:5000")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
