# Chat UI Server - connects to Ollama API
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib.request, urllib.error, datetime, time

START_TIME = time.time()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦙 Llama Chat - GitHub Actions LLM</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',sans-serif; background:#0d1117; color:#e6edf3; height:100vh; display:flex; flex-direction:column; }
  
  .header {
    background:linear-gradient(135deg,#161b22,#1c2128);
    border-bottom:1px solid #30363d;
    padding:16px 24px;
    display:flex; align-items:center; gap:12px;
  }
  .header-icon { font-size:2rem; }
  .header-info h1 { font-size:1.1rem; font-weight:700; }
  .header-info p { font-size:12px; color:#8b949e; }
  .status-badge {
    margin-left:auto; display:flex; align-items:center; gap:6px;
    background:rgba(35,134,54,0.2); border:1px solid rgba(35,134,54,0.4);
    padding:4px 12px; border-radius:20px; font-size:12px; color:#3fb950;
  }
  .dot { width:8px; height:8px; border-radius:50%; background:#3fb950; animation:pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
  
  .model-info {
    background:#161b22; border-bottom:1px solid #30363d;
    padding:8px 24px; font-size:12px; color:#8b949e;
    display:flex; gap:20px; align-items:center;
  }
  .model-info span { color:#e6edf3; font-weight:600; }
  
  #chat-box {
    flex:1; overflow-y:auto; padding:20px 24px;
    display:flex; flex-direction:column; gap:16px;
  }
  
  .msg { display:flex; gap:12px; max-width:800px; }
  .msg.user { flex-direction:row-reverse; align-self:flex-end; }
  
  .avatar {
    width:36px; height:36px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
  }
  .avatar.ai { background:linear-gradient(135deg,#8957e5,#6e40c9); }
  .avatar.user { background:linear-gradient(135deg,#238636,#1a6e2c); }
  
  .bubble {
    background:#161b22; border:1px solid #30363d;
    border-radius:12px; padding:12px 16px;
    font-size:14px; line-height:1.6; max-width:600px;
  }
  .msg.user .bubble { background:#1f3a5f; border-color:#1b4b7a; }
  
  .bubble .name { font-size:11px; font-weight:600; color:#8b949e; margin-bottom:6px; }
  .msg.user .bubble .name { color:#79c0ff; }
  
  .typing { display:flex; gap:4px; align-items:center; padding:4px 0; }
  .typing span {
    width:8px; height:8px; border-radius:50%; background:#8b949e;
    animation:typing 1.2s infinite;
  }
  .typing span:nth-child(2) { animation-delay:0.2s; }
  .typing span:nth-child(3) { animation-delay:0.4s; }
  @keyframes typing { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }
  
  .input-area {
    border-top:1px solid #30363d; padding:16px 24px;
    background:#161b22;
    display:flex; gap:12px; align-items:flex-end;
  }
  
  #user-input {
    flex:1; background:#0d1117; border:1px solid #30363d;
    color:#e6edf3; padding:12px 16px; border-radius:10px;
    font-family:'Inter',sans-serif; font-size:14px;
    resize:none; outline:none; min-height:46px; max-height:120px;
    transition: border-color 0.2s;
  }
  #user-input:focus { border-color:#8957e5; }
  #user-input::placeholder { color:#484f58; }
  
  #send-btn {
    background:linear-gradient(135deg,#8957e5,#6e40c9);
    border:none; color:white; padding:12px 20px;
    border-radius:10px; cursor:pointer; font-size:18px;
    transition:all 0.2s; height:46px;
  }
  #send-btn:hover { transform:scale(1.05); box-shadow:0 0 20px rgba(137,87,229,0.5); }
  #send-btn:disabled { opacity:0.5; cursor:not-allowed; transform:none; }
  
  .welcome {
    text-align:center; margin:auto; padding:40px;
    color:#8b949e;
  }
  .welcome h2 { font-size:2rem; margin-bottom:10px; color:#e6edf3; }
  .welcome p { font-size:14px; margin-bottom:24px; }
  .suggestions { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; }
  .sug-btn {
    background:#161b22; border:1px solid #30363d;
    color:#e6edf3; padding:8px 16px; border-radius:20px;
    cursor:pointer; font-size:13px; transition:all 0.2s;
    font-family:'Inter',sans-serif;
  }
  .sug-btn:hover { border-color:#8957e5; color:#d2a8ff; }
  
  #chat-box::-webkit-scrollbar { width:6px; }
  #chat-box::-webkit-scrollbar-track { background:#0d1117; }
  #chat-box::-webkit-scrollbar-thumb { background:#30363d; border-radius:3px; }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">🦙</div>
  <div class="header-info">
    <h1>Llama Chat</h1>
    <p>Powered by GitHub Actions Runner</p>
  </div>
  <div class="status-badge">
    <span class="dot"></span> Live on bore.pub
  </div>
</div>

<div class="model-info">
  Model: <span>qwen2:0.5b</span> &nbsp;|&nbsp;
  Running on: <span>GitHub Actions (Azure)</span> &nbsp;|&nbsp;
  Tunnel: <span>bore.pub</span> &nbsp;|&nbsp;
  Context: <span>2048 tokens</span>
</div>

<div id="chat-box">
  <div class="welcome" id="welcome">
    <h2>🦙 Llama is Ready!</h2>
    <p>GitHub Actions pe chal raha hai ye LLM — bilkul free! 🤯<br>Kuch bhi pooch sakte ho!</p>
    <div class="suggestions">
      <button class="sug-btn" onclick="sendSuggestion(this)">🇮🇳 Bharat ke baare mein batao</button>
      <button class="sug-btn" onclick="sendSuggestion(this)">Write a haiku about coding</button>
      <button class="sug-btn" onclick="sendSuggestion(this)">Python vs JavaScript - kaunsa better?</button>
      <button class="sug-btn" onclick="sendSuggestion(this)">Ek funny joke sunao</button>
      <button class="sug-btn" onclick="sendSuggestion(this)">What is GitHub Actions?</button>
    </div>
  </div>
</div>

<div class="input-area">
  <textarea id="user-input" placeholder="Kuch bhi pooch... (Enter = send, Shift+Enter = newline)" rows="1"></textarea>
  <button id="send-btn" onclick="sendMessage()">➤</button>
</div>

<script>
  const chatBox = document.getElementById('chat-box');
  const input = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  let isLoading = false;

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });

  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  });

  function sendSuggestion(btn) {
    input.value = btn.textContent.replace(/^[^ ]+ /, '').trim();
    sendMessage();
  }

  function addMsg(role, text) {
    const welcome = document.getElementById('welcome');
    if (welcome) welcome.remove();
    
    const div = document.createElement('div');
    div.className = 'msg ' + (role === 'user' ? 'user' : 'ai');
    const isAI = role !== 'user';
    div.innerHTML = `
      <div class="avatar ${isAI ? 'ai' : 'user'}">${isAI ? '🦙' : '👤'}</div>
      <div class="bubble">
        <div class="name">${isAI ? 'Llama (qwen2:0.5b)' : 'You'}</div>
        <div class="text">${text}</div>
      </div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
  }

  function addTyping() {
    const welcome = document.getElementById('welcome');
    if (welcome) welcome.remove();
    const div = document.createElement('div');
    div.className = 'msg ai'; div.id = 'typing-indicator';
    div.innerHTML = `<div class="avatar ai">🦙</div><div class="bubble"><div class="name">Llama (qwen2:0.5b)</div><div class="typing"><span></span><span></span><span></span></div></div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById('typing-indicator');
    if (t) t.remove();
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isLoading) return;
    
    isLoading = true;
    sendBtn.disabled = true;
    input.value = ''; input.style.height = 'auto';
    
    addMsg('user', text.replace(/\n/g, '<br>'));
    addTyping();
    
    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      removeTyping();
      addMsg('ai', (data.reply || data.error || 'No response').replace(/\n/g, '<br>'));
    } catch(e) {
      removeTyping();
      addMsg('ai', '❌ Error: ' + e.message);
    }
    
    isLoading = false;
    sendBtn.disabled = false;
    input.focus();
  }
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode())
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        msg = body.get('message', '')
        
        try:
            payload = json.dumps({
                "model": "qwen2:0.5b",
                "prompt": msg,
                "stream": False
            }).encode()
            
            req = urllib.request.Request(
                'http://localhost:11434/api/generate',
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                reply = result.get('response', 'No response')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode())
        
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    print("🚀 Chat UI server running on port 3000")
    server.serve_forever()
