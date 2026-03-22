from http.server import HTTPServer, BaseHTTPRequestHandler
import json, datetime, platform, os, socket, subprocess, urllib.parse

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🚀 Claude's Live Demo - GitHub Actions</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono&display=swap');
  
  * { margin:0; padding:0; box-sizing:border-box; }
  
  body {
    font-family: 'Inter', sans-serif;
    background: #0a0a0f;
    color: #fff;
    min-height: 100vh;
    overflow-x: hidden;
  }
  
  .bg-grid {
    position: fixed; top:0; left:0; width:100%; height:100%;
    background-image: 
      linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
  }
  
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
    animation: float 8s ease-in-out infinite;
  }
  .orb1 { width:400px; height:400px; background:#6366f1; top:-100px; left:-100px; }
  .orb2 { width:300px; height:300px; background:#ec4899; bottom:-50px; right:-50px; animation-delay: -4s; }
  .orb3 { width:250px; height:250px; background:#06b6d4; top:50%; left:50%; animation-delay: -2s; }
  
  @keyframes float {
    0%,100% { transform: translate(0,0) scale(1); }
    33% { transform: translate(30px,-30px) scale(1.05); }
    66% { transform: translate(-20px,20px) scale(0.95); }
  }
  
  .container { position:relative; z-index:1; max-width:900px; margin:0 auto; padding:40px 20px; }
  
  .header { text-align:center; margin-bottom:50px; }
  .badge {
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(99,102,241,0.2); border:1px solid rgba(99,102,241,0.4);
    padding:6px 16px; border-radius:20px; font-size:12px; color:#a5b4fc;
    margin-bottom:20px; letter-spacing:1px; text-transform:uppercase;
  }
  .dot { width:8px; height:8px; border-radius:50%; background:#22c55e; animation:pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
  
  h1 { font-size:clamp(2rem,5vw,3.5rem); font-weight:900; line-height:1.1; margin-bottom:15px; }
  .gradient-text {
    background: linear-gradient(135deg, #6366f1, #ec4899, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .subtitle { color:#94a3b8; font-size:1.1rem; }
  
  .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:20px; margin-bottom:30px; }
  
  .card {
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:24px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
  }
  .card:hover { border-color:rgba(99,102,241,0.4); transform:translateY(-2px); background:rgba(99,102,241,0.05); }
  
  .card-icon { font-size:2rem; margin-bottom:12px; }
  .card-label { font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }
  .card-value { font-size:1.4rem; font-weight:700; color:#e2e8f0; font-family:'JetBrains Mono', monospace; }
  .card-sub { font-size:12px; color:#475569; margin-top:4px; }
  
  .ping-section {
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:30px; margin-bottom:30px;
  }
  
  .ping-section h2 { font-size:1.3rem; margin-bottom:20px; color:#e2e8f0; }
  
  .ping-btn {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border: none; color: white; padding: 12px 30px;
    border-radius: 10px; font-size: 15px; font-weight: 600;
    cursor: pointer; transition: all 0.2s; margin-right: 10px; margin-bottom:10px;
  }
  .ping-btn:hover { transform:scale(1.05); box-shadow:0 0 30px rgba(99,102,241,0.5); }
  .ping-btn:active { transform:scale(0.98); }
  
  .ping-btn.cyan { background: linear-gradient(135deg, #06b6d4, #0891b2); }
  .ping-btn.pink { background: linear-gradient(135deg, #ec4899, #db2777); }
  
  #response-box {
    margin-top:20px;
    background:rgba(0,0,0,0.4);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:10px; padding:16px;
    font-family:'JetBrains Mono',monospace;
    font-size:13px; color:#a5b4fc;
    min-height:60px; line-height:1.6;
    white-space:pre-wrap;
  }
  
  .visitor-section {
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:30px;
    margin-bottom:30px;
  }
  
  .visitor-section h2 { font-size:1.3rem; margin-bottom:20px; color:#e2e8f0; }
  
  #visitor-list { list-style:none; }
  #visitor-list li {
    padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05);
    font-family:'JetBrains Mono',monospace; font-size:13px; color:#94a3b8;
    display:flex; justify-content:space-between;
  }
  #visitor-list li:last-child { border-bottom:none; }
  
  .clock-display {
    text-align:center; padding:20px;
    font-family:'JetBrains Mono',monospace;
    font-size:clamp(1.5rem,4vw,2.5rem);
    color:#6366f1; letter-spacing:4px;
    margin-bottom:30px;
  }
  
  .footer { text-align:center; color:#334155; font-size:12px; margin-top:40px; }
  .footer a { color:#6366f1; text-decoration:none; }
  
  #status-dot { display:inline-block; width:10px; height:10px; border-radius:50%; background:#22c55e; margin-right:8px; animation:pulse 2s infinite; }
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>

<div class="container">
  <div class="header">
    <div class="badge"><span class="dot"></span> LIVE on GitHub Actions</div>
    <h1>Claude's <span class="gradient-text">Live Demo</span> 🚀</h1>
    <p class="subtitle">Running inside a GitHub Actions runner — powered by bore.pub tunnel! 😎</p>
  </div>
  
  <div class="clock-display" id="clock">00:00:00</div>
  
  <div class="cards" id="stats-cards">
    <div class="card">
      <div class="card-icon">🖥️</div>
      <div class="card-label">Server</div>
      <div class="card-value" id="server-os">Loading...</div>
      <div class="card-sub" id="server-host">GitHub Actions Runner</div>
    </div>
    <div class="card">
      <div class="card-icon">⚡</div>
      <div class="card-label">Uptime</div>
      <div class="card-value" id="uptime">0s</div>
      <div class="card-sub">Server ke seconds</div>
    </div>
    <div class="card">
      <div class="card-icon">👥</div>
      <div class="card-label">Total Visitors</div>
      <div class="card-value" id="visitor-count">0</div>
      <div class="card-sub">Aaj ka score 😄</div>
    </div>
    <div class="card">
      <div class="card-icon">🌍</div>
      <div class="card-label">Location</div>
      <div class="card-value">Azure</div>
      <div class="card-sub">US East Data Center</div>
    </div>
  </div>
  
  <div class="ping-section">
    <h2>🎮 Interactive API Tester</h2>
    <button class="ping-btn" onclick="callApi('/api/ping')">🏓 Ping Server</button>
    <button class="ping-btn cyan" onclick="callApi('/api/info')">📊 Server Info</button>
    <button class="ping-btn pink" onclick="callApi('/api/joke')">😂 Random Joke</button>
    <button class="ping-btn" style="background:linear-gradient(135deg,#22c55e,#16a34a)" onclick="callApi('/api/time')">⏰ Server Time</button>
    <div id="response-box">👆 Koi bhi button press karo aur API ka response dekho!</div>
  </div>
  
  <div class="visitor-section">
    <h2>📋 Recent Visitors Log</h2>
    <ul id="visitor-list">
      <li><span>Waiting for visitors...</span><span>--</span></li>
    </ul>
  </div>
  
  <div class="footer">
    Made with ❤️ by <a href="#">Claude AI</a> • Running on GitHub Actions • Tunneled via bore.pub<br>
    <span id="server-url-display" style="color:#6366f1;font-family:monospace;font-size:13px;margin-top:5px;display:block;"></span>
  </div>
</div>

<script>
  // Live clock
  function updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent = 
      now.toTimeString().split(' ')[0];
  }
  setInterval(updateClock, 1000);
  updateClock();
  
  // API caller
  async function callApi(endpoint) {
    const box = document.getElementById('response-box');
    box.textContent = '⏳ Loading...';
    const start = Date.now();
    try {
      const res = await fetch(endpoint);
      const data = await res.json();
      const elapsed = Date.now() - start;
      box.textContent = `✅ ${endpoint} [${elapsed}ms]\n\n${JSON.stringify(data, null, 2)}`;
    } catch(e) {
      box.textContent = `❌ Error: ${e.message}`;
    }
  }
  
  // Stats refresh
  async function refreshStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      document.getElementById('visitor-count').textContent = data.visitors;
      document.getElementById('uptime').textContent = data.uptime + 's';
      document.getElementById('server-os').textContent = data.os;
      document.getElementById('server-host').textContent = data.hostname;
      
      // Update visitor list
      const list = document.getElementById('visitor-list');
      if (data.recent_visits && data.recent_visits.length > 0) {
        list.innerHTML = data.recent_visits.slice(-8).reverse().map(v => 
          `<li><span>${v.path}</span><span style="color:#475569">${v.time}</span></li>`
        ).join('');
      }
    } catch(e) {}
  }
  
  setInterval(refreshStats, 2000);
  refreshStats();
  
  // Show current URL
  document.getElementById('server-url-display').textContent = '🌐 ' + window.location.href;
</script>
</body>
</html>"""

import time
START_TIME = time.time()
VISITORS = []
VISIT_COUNT = 0

JOKES = [
    {"setup": "GitHub Actions runner ne kya kaha?", "punchline": "\"Main free hoon but kabhi nahi sonta!\" 😂"},
    {"setup": "Programmer ko kya hua jab bore.pub se tunnel khola?", "punchline": "Uski duniya hi khul gayi! 🌍😎"},
    {"setup": "Cloud server ka favorite song?", "punchline": "\"Tujhe dekha toh ye jaana sanam... main toh CPU hoon!\" 😂"},
    {"setup": "API ne GET request ko kya bola?", "punchline": "\"Aaja mere paas, data dunga!\" 💘"},
    {"setup": "Ek developer roz 8 ghante kaam karta tha...", "punchline": "Phir usne GitHub Actions discover kiya. Ab woh 23 ghante kaam karta hai! 😭"},
]

import random

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Quiet logs
    
    def do_GET(self):
        global VISIT_COUNT
        VISIT_COUNT += 1
        visit_time = datetime.datetime.now().strftime('%H:%M:%S')
        VISITORS.append({"path": self.path, "time": visit_time, "ip": self.client_address[0]})
        
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/api/ping':
            self.send_json({"pong": True, "time": visit_time, "message": "🏓 Pong! Server alive hai bhai!", "latency_tip": "Ye response GitHub Actions runner se aa raha hai!"})
        
        elif path == '/api/info':
            self.send_json({
                "server": "GitHub Actions Runner",
                "os": platform.system() + " " + platform.release(),
                "python": platform.python_version(),
                "hostname": socket.gethostname(),
                "cpu_count": os.cpu_count(),
                "tunnel": "bore.pub",
                "message": "Ye sab GitHub ka free runner hai! 🤯"
            })
        
        elif path == '/api/joke':
            joke = random.choice(JOKES)
            self.send_json(joke)
        
        elif path == '/api/time':
            now = datetime.datetime.utcnow()
            self.send_json({
                "utc": now.isoformat(),
                "ist": (now + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S IST'),
                "message": "GitHub runner UTC time! 🕐"
            })
        
        elif path == '/api/stats':
            uptime = int(time.time() - START_TIME)
            self.send_json({
                "visitors": VISIT_COUNT,
                "uptime": uptime,
                "os": platform.system(),
                "hostname": socket.gethostname()[:15],
                "recent_visits": VISITORS[-20:]
            })
        
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode())
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

if __name__ == '__main__':
    port = 3000
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"🚀 Server running on port {port}")
    server.serve_forever()
