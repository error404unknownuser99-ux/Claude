const express = require('express');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const app = express();
app.use(express.json());

const ROOT    = path.join(__dirname, '..');
const DATA    = path.join(ROOT, 'data');
const OUTPUT  = path.join(ROOT, 'output');
const USERS   = path.join(DATA, 'users.json');
const MSGS    = path.join(DATA, 'messages.json');
const LOGFILE = path.join(OUTPUT, 'runtimelogs.txt');

fs.mkdirSync(DATA,   { recursive: true });
fs.mkdirSync(OUTPUT, { recursive: true });
if (!fs.existsSync(USERS)) fs.writeFileSync(USERS, '[]');
if (!fs.existsSync(MSGS))  fs.writeFileSync(MSGS,  '{}');

let users    = JSON.parse(fs.readFileSync(USERS, 'utf8'));
let messages = JSON.parse(fs.readFileSync(MSGS,  'utf8'));
let dirty    = false;

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try { fs.appendFileSync(LOGFILE, line + '\n'); } catch(e) {}
}

function gitSync() {
  if (!dirty) return;
  try {
    fs.writeFileSync(USERS, JSON.stringify(users, null, 2));
    fs.writeFileSync(MSGS,  JSON.stringify(messages, null, 2));
    execSync('git add data/', { cwd: ROOT, stdio: 'pipe' });
    const diff = execSync('git diff --staged --name-only', { cwd: ROOT, stdio: 'pipe' }).toString().trim();
    if (diff) {
      const ts = new Date().toISOString().slice(0,19).replace('T',' ');
      execSync(`git commit -m "🤖 Chat sync [${ts}]"`, { cwd: ROOT, stdio: 'pipe' });
      execSync('git pull --rebase origin main', { cwd: ROOT, stdio: 'pipe' });
      execSync('git push', { cwd: ROOT, stdio: 'pipe' });
      dirty = false;
      log('✅ GitHub sync done — users:' + users.length);
    }
  } catch(e) {
    log('⚠️ Sync error: ' + e.message.slice(0, 120));
  }
}

setInterval(gitSync, 30000);

// ── API Routes ──────────────────────────────────────────────────

app.get('/api/ping', (_, res) => {
  res.json({ ok: true, users: users.length, ts: Date.now() });
});

app.get('/api/users', (_, res) => {
  res.json(users);
});

app.post('/api/signup', (req, res) => {
  const name = String(req.body.name || '').trim().slice(0, 20);
  if (name.length < 2) return res.status(400).json({ error: 'Name min 2 chars' });

  const existing = users.find(u => u.name.toLowerCase() === name.toLowerCase());
  if (existing) return res.json({ user: existing });

  const user = {
    id:   Date.now().toString(36) + Math.random().toString(36).slice(2, 5),
    name: name,
    at:   Date.now()
  };
  users.push(user);
  dirty = true;
  log('👤 Joined: ' + name);
  res.json({ user });
});

app.get('/api/chat/:chatId', (req, res) => {
  const since = parseInt(req.query.since) || 0;
  const all = messages[req.params.chatId] || [];
  res.json(all.filter(m => m.ts > since));
});

app.post('/api/chat', (req, res) => {
  const { from, to, text } = req.body;
  if (!text || !text.trim()) return res.status(400).json({ error: 'Empty message' });
  if (!from || !to)          return res.status(400).json({ error: 'Missing from/to' });

  const chatId = [from, to].sort().join(':');
  if (!messages[chatId]) messages[chatId] = [];

  const msg = {
    id:   Date.now().toString(36) + Math.random().toString(36).slice(2,4),
    from: from,
    to:   to,
    text: text.trim().slice(0, 500),
    ts:   Date.now()
  };
  messages[chatId].push(msg);
  if (messages[chatId].length > 300) {
    messages[chatId] = messages[chatId].slice(-300);
  }
  dirty = true;

  res.json({ ok: true, msg });
});

// ── Serve Frontend ──────────────────────────────────────────────
app.get('/', (_, res) => {
  res.sendFile(path.join(__dirname, 'chat_app.html'));
});

app.listen(3000, '0.0.0.0', () => {
  log('🚀 GitChat server live on port 3000');
});
