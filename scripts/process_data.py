from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib.request, time, subprocess

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦙 Llama Chat</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Inter',sans-serif;background:#0d1117;color:#e6edf3;height:100vh;display:flex;flex-direction:column}
  .header{background:#161b22;border-bottom:1px solid #30363d;padding:14px 20px;display:flex;align-items:center;gap:10px}
  .header h1{font-size:1rem;font-weight:700}
  .header p{font-size:11px;color:#8b949e}
  .badge{margin-left:auto;background:rgba(35,134,54,0.2);border:1px solid #238636;padding:3px 10px;border-radius:20px;font-size:11px;color:#3fb950;display:flex;align-items:center;gap:5px}
  .dot{width:7px;height:7px;border-radius:50%;background:#3fb950;animation:pulse 2s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:0.3}}
  #chat{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
  .msg{display:flex;gap:10px;max-width:750px}
  .msg.user{align-self:flex-end;flex-direction:row-reverse}
  .av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0}
  .av.ai{background:linear-gradient(135deg,#8957e5,#6e40c9)}
  .av.user{background:linear-gradient(135deg,#238636,#1a6e2c)}
  .bub{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:10px 14px;font-size:13px;line-height:1.6;max-width:560px}
  .msg.user .bub{background:#1f3a5f;border-color:#1b4b7a}
  .name{font-size:10px;color:#8b949e;margin-bottom:4px;font-weight:600}
  .msg.user .name{color:#79c0ff}
  .typing{display:flex;gap:4px;padding:4px 0}
  .typing span{width:7px;height:7px;border-radius:50%;background:#8b949e;animation:t 1.2s infinite}
  .typing span:nth-child(2){animation-delay:.2s}
  .typing span:nth-child(3){animation-delay:.4s}
  @keyframes t{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
  .input-area{border-top:1px solid #30363d;padding:12px 16px;background:#161b22;display:flex;gap:10px;align-items:flex-end}
  #inp{flex:1;background:#0d1117;border:1px solid #30363d;color:#e6edf3;padding:10px 14px;border-radius:8px;font-family:'Inter',sans-serif;font-size:13px;resize:none;outline:none;min-height:42px;max-height:100px;transition:border-color .2s}
  #inp:focus{border-color:#8957e5}
  #inp::placeholder{color:#484f58}
  #btn{background:linear-gradient(135deg,#8957e5,#6e40c9);border:none;color:white;padding:10px 18px;border-radius:8px;cursor:pointer;font-size:16px;height:42px;transition:all .2s}
  #btn:hover{transform:scale(1.05);box-shadow:0 0 15px rgba(137,87,229,.5)}
  #btn:disabled{opacity:.5;cursor:not-allowed;transform:none}
  .welcome{text-align:center;margin:auto;padding:30px;color:#8b949e}
  .welcome h2{font-size:1.8rem;margin-bottom:8px;color:#e6edf3}
  .welcome p{font-size:13px;margin-bottom:20px}
  .sugs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
  .s{background:#161b22;border:1px solid #30363d;color:#e6edf3;padding:7px 14px;border-radius:16px;cursor:pointer;font-size:12px;transition:all .2s;font-family:'Inter',sans-serif}
  .s:hover{border-color:#8957e5;color:#d2a8ff}
  #chat::-webkit-scrollbar{width:5px}
  #chat::-webkit-scrollbar-track{background:#0d1117}
  #chat::-webkit-scrollbar-thumb{background:#30363d;border-radius:3px}
  #status{font-size:11px;color:#8b949e;padding:4px 16px;background:#0d1117;text-align:center}
</style>
</head>
<body>
<div class="header">
  <div style="font-size:1.8rem">🦙</div>
  <div><h1>Llama Chat</h1><p>qwen2:0.5b — GitHub Actions Runner</p></div>
  <div class="badge"><span class="dot"></span>Live</div>
</div>
<div id="status">✅ Server ready — type karke Enter dabao!</div>
<div id="chat">
  <div class="welcome" id="welcome">
    <h2>🦙 Chat karo!</h2>
    <p>GitHub Actions pe FREE LLM chal raha hai! 🤯<br>Kuch bhi pooch — Hindi ya English mein!</p>
    <div class="sugs">
      <button class="s" onclick="qs(this)">Bharat ke baare mein batao</button>
      <button class="s" onclick="qs(this)">Write a haiku about coding</button>
      <button class="s" onclick="qs(this)">Python kya hai simple mein?</button>
      <button class="s" onclick="qs(this)">Tell me a joke</button>
    </div>
  </div>
</div>
<div class="input-area">
  <textarea id="inp" placeholder="Kuch bhi pooch... (Enter = bhejo)"></textarea>
  <button id="btn" onclick="send()">➤</button>
</div>
<script>
const chat=document.getElementById('chat');
const inp=document.getElementById('inp');
const btn=document.getElementById('btn');
const status=document.getElementById('status');
let busy=false;

inp.addEventListener('keydown',e=>{
  if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}
});

function qs(b){inp.value=b.textContent;send();}

function addMsg(role,html){
  const w=document.getElementById('welcome');
  if(w)w.remove();
  const d=document.createElement('div');
  d.className='msg '+(role==='user'?'user':'ai');
  const isAI=role!=='user';
  d.innerHTML=`<div class="av ${isAI?'ai':'user'}">${isAI?'🦙':'👤'}</div>
    <div class="bub"><div class="name">${isAI?'Llama':'You'}</div><div class="txt">${html}</div></div>`;
  chat.appendChild(d);
  chat.scrollTop=chat.scrollHeight;
  return d;
}

async function send(){
  const txt=inp.value.trim();
  if(!txt||busy)return;
  busy=true; btn.disabled=true;
  inp.value=''; inp.style.height='auto';
  addMsg('user',txt.replace(/\n/g,'<br>'));
  
  // typing indicator
  const w=document.getElementById('welcome');
  if(w)w.remove();
  const td=document.createElement('div');
  td.className='msg ai'; td.id='typing';
  td.innerHTML='<div class="av ai">🦙</div><div class="bub"><div class="name">Llama</div><div class="typing"><span></span><span></span><span></span></div></div>';
  chat.appendChild(td); chat.scrollTop=chat.scrollHeight;
  
  status.textContent='⏳ Llama soch raha hai...';
  
  try{
    const res=await fetch('/chat',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({msg:txt})
    });
    const d=await res.json();
    const typing=document.getElementById('typing');
    if(typing)typing.remove();
    if(d.ok){
      addMsg('ai',d.reply.replace(/\n/g,'<br>').replace(/```([\s\S]*?)```/g,'<code style="background:#0d1117;padding:2px 6px;border-radius:4px;font-family:monospace">$1</code>'));
      status.textContent='✅ Ready!';
    } else {
      addMsg('ai','❌ Error: '+d.error);
      status.textContent='❌ Error hua!';
    }
  }catch(e){
    const typing=document.getElementById('typing');
    if(typing)typing.remove();
    addMsg('ai','❌ Network error: '+e.message);
    status.textContent='❌ Connection error!';
  }
  busy=false; btn.disabled=false; inp.focus();
}
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path != '/chat':
            self.send_response(404); self.end_headers(); return

        length = int(self.headers.get('Content-Length',0))
        body = json.loads(self.rfile.read(length))
        msg = body.get('msg','')

        print(f"[Chat] User: {msg[:60]}")

        try:
            payload = json.dumps({
                "model": "qwen2:0.5b",
                "prompt": msg,
                "stream": False,
                "options": {"num_predict": 300, "temperature": 0.7}
            }).encode()

            req = urllib.request.Request(
                'http://localhost:11434/api/generate',
                data=payload,
                headers={'Content-Type':'application/json'}
            )
            with urllib.request.urlopen(req, timeout=90) as r:
                result = json.loads(r.read())
                reply = result.get('response','').strip()
                print(f"[Chat] Reply: {reply[:60]}")

            resp = json.dumps({"ok": True, "reply": reply})
        except Exception as e:
            print(f"[Chat] ERROR: {e}")
            resp = json.dumps({"ok": False, "error": str(e)})

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(resp.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    print("🚀 Chat server port 3000 pe ready!")
    server.serve_forever()
