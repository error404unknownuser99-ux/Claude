#!/bin/bash
# log_gen.sh — Auto-push logger (Bash)
# Usage:
#   source ./log_generators/log_gen.sh
#   log_start
#   log "kuch bhi"
#   log_stop

WS="${GITHUB_WORKSPACE:-.}"
OUT="$WS/output"
RUNTIME="$OUT/runtimelogs.txt"
PID_FILE="/tmp/log_gen_pid"
HASH_FILE="/tmp/log_gen_hash"

_ts()   { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
_hash() { cat "$RUNTIME" "$OUT/detailedlog.txt" 2>/dev/null | md5sum | cut -d' ' -f1; }

_push_loop() {
  while true; do
    sleep 5
    NEW_H=$(_hash)
    OLD_H=$(cat "$HASH_FILE" 2>/dev/null)
    [ "$NEW_H" = "$OLD_H" ] && continue          # kuch badla nahi — skip!
    echo "$NEW_H" > "$HASH_FILE"
    git -C "$WS" add output/ 2>/dev/null
    git -C "$WS" diff --staged --quiet && continue
    git -C "$WS" commit -m "🔄 $(date -u +%H:%M:%S)" 2>/dev/null
    git -C "$WS" pull --rebase origin main        2>/dev/null
    git -C "$WS" push                             2>/dev/null
  done
}

log() {
  local MSG="$1" LEVEL="${2:-INFO}"
  mkdir -p "$OUT"
  local LINE="[$(_ts)] [$LEVEL] $MSG"
  echo "$LINE"
  echo "$LINE" >> "$RUNTIME"
}

log_start() {
  mkdir -p "$OUT"
  log "🚀 LogGen started!"
  _push_loop &
  echo $! > "$PID_FILE"
}

log_stop() {
  log "🏁 LogGen stopped — final push..."
  [ -f "$PID_FILE" ] && kill "$(cat $PID_FILE)" 2>/dev/null
  # Final push
  git -C "$WS" add output/ 2>/dev/null
  git -C "$WS" diff --staged --quiet || {
    git -C "$WS" commit -m "✅ Final $(date -u +%H:%M:%S)"
    git -C "$WS" pull --rebase origin main
    git -C "$WS" push
  }
}
