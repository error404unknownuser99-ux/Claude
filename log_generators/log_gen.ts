/**
 * log_gen.ts — Auto-push logger (TypeScript)
 * Usage:
 *   import { start, log, stop } from './log_generators/log_gen'
 *   start()
 *   log("kuch bhi")
 *   await stop()
 */
import { execSync } from 'child_process'
import * as fs     from 'fs'
import * as path   from 'path'
import * as crypto from 'crypto'

const WS       = process.env.GITHUB_WORKSPACE ?? '.'
const OUT      = path.join(WS, 'output')
const RUNTIME  = path.join(OUT, 'runtimelogs.txt')
const DETAILED = path.join(OUT, 'detailedlog.txt')

let _lastHash: string | null = null
let _timer:    ReturnType<typeof setInterval> | null = null
let _pushing   = false

const ts  = (): string => new Date().toISOString().replace('T',' ').slice(0,19) + ' UTC'
const git = (...a: string[]) => { try { execSync(`git ${a.join(' ')}`, { cwd: WS, stdio: 'pipe' }) } catch {} }

function _hash(): string {
  let c = ''
  for (const f of [RUNTIME, DETAILED])
    try { c += fs.readFileSync(f, 'utf8') } catch {}
  return crypto.createHash('md5').update(c).digest('hex')
}

function _push(): void {
  if (_pushing) return
  _pushing = true
  try {
    const h = _hash()
    if (h === _lastHash) return
    _lastHash = h
    git('add', 'output/')
    try { execSync('git diff --staged --quiet', { cwd: WS }); return } catch {}
    const t = new Date().toISOString().slice(11,19)
    git('commit', '-m', `"🔄 ${t}"`)
    git('pull', '--rebase', 'origin', 'main')
    git('push')
  } finally { _pushing = false }
}

export function log(msg: string, level = 'INFO'): void {
  fs.mkdirSync(OUT, { recursive: true })
  const line = `[${ts()}] [${level}] ${msg}`
  console.log(line)
  fs.appendFileSync(RUNTIME, line + '\n')
}

export function start(): void {
  fs.mkdirSync(OUT, { recursive: true })
  log('🚀 LogGen started!')
  _timer = setInterval(_push, 5000)
}

export async function stop(): Promise<void> {
  if (_timer) clearInterval(_timer)
  log('🏁 LogGen stopped — final push...')
  _push()
}
