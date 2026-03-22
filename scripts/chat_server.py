#!/usr/bin/env python3
"""GitChat - GitHub Actions pe chalane wala Real-time Chat App!"""

import json, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

users = {}
messages = []
msg_ctr = [0]
lock = threading.Lock()

HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GitChat 💬</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0e1a;color:#e0e0e0;height:100vh;display:flex;flex-direction:column;overflow:hidden}
.header{background:linear-gradient(135deg,#1a472a,#2d6a4f);padding:14px 20px;display:flex;align-items:center;gap:12px;box-shadow:0 2px 20px rgba(0,0,0,.5)}
.header-logo{font-size:28px}.header-title{font-size:20px;font-weight:700;color:#a8edbd}
.header-sub{font-size:12px;color:#6fcf97;margin-top:2px}
.header-badge{margin-left:auto;background:#27ae60;color:#fff;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:600}
#signup-screen{flex:1;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at center,#0d2137,#0a0e1a 70%)}
.signup-card{background:#131c2e;border:1px solid #1e3a5f;border-radius:24px;padding:40px;width:380px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.6)}
.signup-emoji{font-size:64px;margin-bottom:16px;animation:bounce 2s infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.signup-card h2{font-size:26px;color:#a8edbd;margin-bottom:8px}
.signup-card p{color:#7f9ab0;font-size:14px;margin-bottom:30px}
.signup-card input{width:100%;padding:14px 18px;background:#0d1b2a;border:2px solid #1e3a5f;border-radius:12px;color:#e0e0e0;font-size:16px;outline:none;transition:border-color .3s;margin-bottom:16px}
.signup-card input:focus{border-color:#27ae60}.signup-card input::placeholder{color:#3d5a73}
.btn-join{width:100%;padding:14px;background:linear-gradient(135deg,#1a472a,#27ae60);border:none;border-radius:12px;color:#fff;font-size:16px;font-weight:700;cursor:pointer;transition:transform .2s,opacity .2s}
.btn-join:hover{transform:translateY(-2px);opacity:.9}
#app-screen{flex:1;display:none;flex-direction:row;overflow:hidden}
.sidebar{width:280px;background:#111827;border-right:1px solid #1e2d40;display:flex;flex-direction:column;overflow:hidden}
.sidebar-header{padding:16px;background:#0d1b2a;border-bottom:1px solid #1e2d40;display:flex;align-items:center;gap:10px}
.my-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#1a472a,#27ae60);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#fff;flex-shrink:0}
.my-name{font-weight:600;font-size:15px;color:#a8edbd}.my-label{font-size:11px;color:#4a7c59}
.sidebar-title{padding:10px 16px;font-size:11px;color:#4a7c59;font-weight:700;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid #1e2d40;display:flex;align-items:center;justify-content:space-between}
.online-count{background:#1a472a;color:#6fcf97;padding:2px 8px;border-radius:10px;font-size:11px}
.user-list{flex:1;overflow-y:auto}.user-list::-webkit-scrollbar{width:4px}.user-list::-webkit-scrollbar-thumb{background:#1e2d40;border-radius:2px}
.user-item{display:flex;align-items:center;gap:12px;padding:12px 16px;cursor:pointer;transition:background .2s;border-bottom:1px solid #0d1218}
.user-item:hover{background:#1a2535}.user-item.active{background:#1a3a2a;border-left:3px solid #27ae60}
.user-avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:17px;color:#fff;flex-shrink:0}
.user-info{flex:1;min-width:0}.user-name{font-size:14px;font-weight:600;color:#d0e8d0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.user-status{font-size:11px;color:#4a7c59}
.online-dot{width:10px;height:10px;border-radius:50%;background:#27ae60;flex-shrink:0;box-shadow:0 0 6px #27ae60;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
.no-users{padding:30px 20px;text-align:center;color:#3d5a73;font-size:14px}
.chat-area{flex:1;display:flex;flex-direction:column;background:#0a0e1a;overflow:hidden}
.chat-empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#2a3f55}
.chat-empty-icon{font-size:72px;margin-bottom:20px;opacity:.4}.chat-empty h3{font-size:20px;color:#3d5a73;margin-bottom:8px}
.chat-empty p{font-size:14px;color:#2a3f55}
.chat-header{padding:14px 20px;background:#111827;border-bottom:1px solid #1e2d40;display:flex;align-items:center;gap:14px;box-shadow:0 2px 10px rgba(0,0,0,.3)}
.chat-partner-avatar{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:17px;color:#fff}
.chat-partner-name{font-size:16px;font-weight:600;color:#a8edbd}.chat-partner-status{font-size:12px;color:#27ae60}
.messages-container{flex:1;overflow-y:auto;padding:20px 16px;display:flex;flex-direction:column;gap:4px}
.messages-container::-webkit-scrollbar{width:4px}.messages-container::-webkit-scrollbar-thumb{background:#1e2d40;border-radius:2px}
.msg-wrapper{display:flex;margin-bottom:2px}.msg-wrapper.mine{justify-content:flex-end}.msg-wrapper.theirs{justify-content:flex-start}
.msg-bubble{max-width:65%;padding:10px 14px;border-radius:18px;font-size:14px;line-height:1.5;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.msg-wrapper.mine .msg-bubble{background:linear-gradient(135deg,#1a472a,#27ae60);color:#e8f5e9;border-bottom-right-radius:4px}
.msg-wrapper.theirs .msg-bubble{background:#1e2d40;color:#c8d8e8;border-bottom-left-radius:4px}
.msg-time{font-size:10px;margin-top:4px;opacity:.6;text-align:right}
.msg-input-area{padding:12px 16px;background:#111827;border-top:1px solid #1e2d40;display:flex;gap:10px;align-items:flex-end}
.msg-input{flex:1;background:#0d1b2a;border:1px solid #1e3a5f;border-radius:24px;padding:12px 18px;color:#e0e0e0;font-size:14px;outline:none;resize:none;max-height:120px;min-height:44px;font-family:inherit;transition:border-color .3s}
.msg-input:focus{border-color:#27ae60}.msg-input::placeholder{color:#3d5a73}
.send-btn{width:44px;height:44px;background:linear-gradient(135deg,#1a472a,#27ae60);border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;transition:transform .2s}
.send-btn:hover{transform:scale(1.1)}.send-btn:active{transform:scale(.95)}
.toast{position:fixed;bottom:20px;right:20px;background:#1a3a2a;border:1px solid #27ae60;color:#a8edbd;padding:12px 20px;border-radius:12px;font-size:14px;z-index:1000;opacity:0;transform:translateY(20px);transition:all .3s;box-shadow:0 4px 20px rgba(0,0,0,.5)}
.toast.show{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<div class="header">
  <span class="header-logo">💬</span>
  <div><div class="header-title">GitChat</div><div class="header-sub">Powered by GitHub Actions ⚡</div></div>
  <div class="header-badge">🟢 Live</div>
</div>
<div id="signup-screen">
  <div class="signup-card">
    <div class="signup-emoji">🚀</div>
    <h2>GitChat mein Swagat!</h2>
    <p>Sirf apna naam likho aur join ho jao 👇<br>No password, no email — seedha chat!</p>
    <input type="text" id="name-input" placeholder="Apna naam likho..." maxlength="20" autocomplete="off">
    <button class="btn-join" onclick="signup()">⚡ Join Now!</button>
  </div>
</div>
<div id="app-screen">
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="my-avatar" id="my-avatar">?</div>
      <div><div class="my-name" id="my-name-display">...</div><div class="my-label">Tum 😎</div></div>
    </div>
    <div class="sidebar-title">Online Users <span class="online-count" id="online-count">0</span></div>
    <div class="user-list" id="user-list"><div class="no-users">Koi online nahi... 😴<br>Share karo link dosto ko!</div></div>
  </div>
  <div class="chat-area">
    <div class="chat-empty" id="chat-empty">
      <div class="chat-empty-icon">👈</div>
      <h3>Kisi ko select karo!</h3>
      <p>Left se kisi user par click karo aur chatting shuru karo 🎉</p>
    </div>
    <div id="active-chat" style="display:none;flex-direction:column;height:100%">
      <div class="chat-header">
        <div class="chat-partner-avatar" id="partner-avatar">?</div>
        <div><div class="chat-partner-name" id="partner-name">...</div><div class="chat-partner-status">🟢 Online</div></div>
      </div>
      <div class="messages-container" id="messages-container"></div>
      <div class="msg-input-area">
        <textarea class="msg-input" id="msg-input" placeholder="Message likho..." rows="1" onkeydown="handleKey(event)"></textarea>
        <button class="send-btn" onclick="sendMessage()">&#10148;</button>
      </div>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
const COLORS=['linear-gradient(135deg,#1a4a8a,#2196f3)','linear-gradient(135deg,#6a1a8a,#9c27b0)','linear-gradient(135deg,#8a4a1a,#ff9800)','linear-gradient(135deg,#8a1a1a,#f44336)','linear-gradient(135deg,#1a6a4a,#4caf50)','linear-gradient(135deg,#1a6a6a,#00bcd4)'];
function colorFor(n){let h=0;for(let c of n)h=(h*31+c.charCodeAt(0))%COLORS.length;return COLORS[h]}
function ini(n){return n.trim().charAt(0).toUpperCase()}
function showToast(m,d=3000){const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),d)}
function fmtTime(ts){return new Date(ts*1000).toLocaleTimeString('hi-IN',{hour:'2-digit',minute:'2-digit'})}
function escHtml(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>')}

let myName=localStorage.getItem('gitchat_name')||'';
let chatWith=null,lastMsgId=0;

document.getElementById('msg-input')?.addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,120)+'px'});
document.getElementById('name-input')?.addEventListener('keydown',e=>{if(e.key==='Enter')signup()});

async function signup(){
  const input=document.getElementById('name-input');
  const name=input.value.trim();
  if(!name){showToast('❌ Naam toh dalo bhai!');return}
  try{
    const r=await fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});
    const d=await r.json();
    if(d.ok){myName=name;localStorage.setItem('gitchat_name',name);enterApp()}
  }catch(e){showToast('❌ Server se connect nahi hua!')}
}

function enterApp(){
  document.getElementById('signup-screen').style.display='none';
  document.getElementById('app-screen').style.display='flex';
  document.getElementById('my-name-display').textContent=myName;
  const av=document.getElementById('my-avatar');av.textContent=ini(myName);av.style.background=colorFor(myName);
  fetchUsers();ping();
  setInterval(()=>{fetchUsers();ping()},5000);
  setInterval(fetchMessages,2000);
}

async function fetchUsers(){
  try{
    const r=await fetch('/api/users');const users=await r.json();
    const others=users.filter(u=>u.name!==myName);
    const list=document.getElementById('user-list');
    const now=Math.floor(Date.now()/1000);
    const online=others.filter(u=>now-(u.last_seen||0)<30);
    document.getElementById('online-count').textContent=online.length;
    if(!others.length){list.innerHTML='<div class="no-users">Koi online nahi... 😴<br>Share karo link dosto ko!</div>';return}
    list.innerHTML=others.map(u=>{
      const isOnline=now-(u.last_seen||0)<30;
      const active=u.name===chatWith?'active':'';
      return `<div class="user-item ${active}" onclick="openChat('${u.name.replace(/'/g,"\\\\'")}')">
        <div class="user-avatar" style="background:${colorFor(u.name)}">${ini(u.name)}</div>
        <div class="user-info"><div class="user-name">${u.name}</div><div class="user-status">${isOnline?'🟢 Online':'⚫ Away'}</div></div>
        ${isOnline?'<div class="online-dot"></div>':''}
      </div>`;
    }).join('');
  }catch(e){}
}

function openChat(name){
  chatWith=name;lastMsgId=0;
  document.getElementById('chat-empty').style.display='none';
  const ac=document.getElementById('active-chat');ac.style.display='flex';
  document.getElementById('partner-name').textContent=name;
  const av=document.getElementById('partner-avatar');av.textContent=ini(name);av.style.background=colorFor(name);
  document.getElementById('messages-container').innerHTML='';
  document.getElementById('msg-input').focus();
  fetchUsers();fetchMessages();
}

async function fetchMessages(){
  if(!chatWith)return;
  try{
    const r=await fetch(`/api/messages?me=${encodeURIComponent(myName)}&other=${encodeURIComponent(chatWith)}&since=${lastMsgId}`);
    const msgs=await r.json();
    if(msgs.length>0){appendMessages(msgs);lastMsgId=msgs[msgs.length-1].id}
  }catch(e){}
}

function appendMessages(msgs){
  const c=document.getElementById('messages-container');
  const atBottom=c.scrollHeight-c.clientHeight<=c.scrollTop+50;
  msgs.forEach(m=>{
    const mine=m.from===myName;
    const div=document.createElement('div');div.className=`msg-wrapper ${mine?'mine':'theirs'}`;
    div.innerHTML=`<div class="msg-bubble">${escHtml(m.text)}<div class="msg-time">${fmtTime(m.ts)}</div></div>`;
    c.appendChild(div);
  });
  if(atBottom)c.scrollTop=c.scrollHeight;
}

async function sendMessage(){
  const input=document.getElementById('msg-input');
  const text=input.value.trim();if(!text||!chatWith)return;
  input.value='';input.style.height='auto';
  try{
    const r=await fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({from:myName,to:chatWith,text})});
    const d=await r.json();if(d.ok)fetchMessages();
  }catch(e){showToast('❌ Message send nahi hua!')}
}

function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage()}}
async function ping(){try{await fetch(`/api/ping?me=${encodeURIComponent(myName)}`)}catch(e){}}

window.addEventListener('load',()=>{
  if(myName){
    document.getElementById('name-input').value=myName;
    fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName})})
      .then(()=>enterApp()).catch(()=>{});
  }
});
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path)
        qs = parse_qs(p.query)
        if p.path in ('/', '/index.html'):
            self.send_html(HTML)
        elif p.path == '/api/users':
            with lock:
                self.send_json(list(users.values()))
        elif p.path == '/api/messages':
            me    = qs.get('me',    [''])[0]
            other = qs.get('other', [''])[0]
            since = int(qs.get('since', ['0'])[0])
            with lock:
                msgs = [m for m in messages
                        if m['id'] > since and (
                            (m['from'] == me    and m['to'] == other) or
                            (m['from'] == other and m['to'] == me)
                        )]
            self.send_json(msgs)
        elif p.path == '/api/ping':
            me = qs.get('me', [''])[0]
            if me:
                with lock:
                    if me in users:
                        users[me]['last_seen'] = int(time.time())
            self.send_json({'ok': True})
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        p    = urlparse(self.path)
        data = self.read_body()
        if p.path == '/api/signup':
            name = data.get('name', '').strip()[:20]
            if not name:
                self.send_json({'error': 'Name required'}, 400); return
            with lock:
                if name not in users:
                    users[name] = {'name': name, 'joined': int(time.time()), 'last_seen': int(time.time())}
                else:
                    users[name]['last_seen'] = int(time.time())
            print(f"User joined: {name}  (total: {len(users)})")
            self.send_json({'ok': True, 'name': name})
        elif p.path == '/api/send':
            frm  = data.get('from', '')
            to   = data.get('to',   '')
            text = data.get('text', '').strip()[:500]
            if not (frm and to and text):
                self.send_json({'error': 'Missing fields'}, 400); return
            with lock:
                msg_ctr[0] += 1
                msg = {'id': msg_ctr[0], 'from': frm, 'to': to, 'text': text, 'ts': int(time.time())}
                messages.append(msg)
                if len(messages) > 2000: messages.pop(0)
            print(f"{frm} -> {to}: {text[:40]}")
            self.send_json({'ok': True, 'id': msg_ctr[0]})
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, fmt, *args): pass

print("GitChat server starting on port 8080...")
HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
