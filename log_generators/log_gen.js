/**
 * log_gen.js — Auto-push logger (Node.js)
 * Usage:
 *   const { start, log, stop } = require('./log_generators/log_gen')
 *   start()
 *   log("kuch bhi")
 *   await stop()
 */
const { execSync } = require('child_process')
const fs   = require('fs')
const path = require('path')
const crypto = require('crypto')

const WS       = process.env.GITHUB_WORKSPACE || '.'
const OUT      = path.join(WS, 'output')
const RUNTIME  = path.join(OUT, 'runtimelogs.txt')
const DETAILED = path.join(OUT, 'detailedlog.txt')

let _lastHash = null
let _timer    = null
let _pushing  = false

// ── helpers ────────────────────────────────────────────────────────────
const ts  = () => new Date().toISOString().replace('T',' ').slice(0,19) + ' UTC'
const git = (...a) => { try { execSync(`git ${a.join(' ')}`, { cwd: WS, stdio: 'pipe' }) } catch {} }

function _hash() {
  let c = ''
  for (const f of [RUNTIME, DETAILED])
    try { c += fs.readFileSync(f, 'utf8') } catch {}
  return crypto.createHash('md5').update(c).digest('hex')
}

function _push() {
  if (_pushing) return
  _pushing = true
  try {
    const h = _hash()
    if (h === _lastHash) return           // kuch badla nahi — skip!
    _lastHash = h
    git('add', 'output/')
    try { execSync('git diff --staged --quiet', { cwd: WS }); return } catch {}
    const t = new Date().toISOString().slice(11,19)
    git('commit', '-m', `"🔄 ${t}"`)
    git('pull', '--rebase', 'origin', 'main')
    git('push')
  } finally { _pushing = false }
}

// ── public API ─────────────────────────────────────────────────────────
function log(msg, level = 'INFO') {
  fs.mkdirSync(OUT, { recursive: true })
  const line = `[${ts()}] [${level}] ${msg}`
  console.log(line)
  fs.appendFileSync(RUNTIME, line + '\n')
}

function start() {
  fs.mkdirSync(OUT, { recursive: true })
  log('🚀 LogGen started!')
  _timer = setInterval(_push, 5000)
}

async function stop() {
  clearInterval(_timer)
  log('🏁 LogGen stopped — final push...')
  _push()
}

module.exports = { start, log, stop }
