# 📦 log_generators — Universal Auto-Push Logger

Ek baar import karo — **har 5 sec mein apne aap push hota rahega!**
Sirf tabhi push hoga jab file mein **kuch badlav hua ho** (1 bit bhi)!

---

## 🚀 Kaise Kaam Karta Hai:

```
start()  →  background mein 5 sec loop shuru
log()    →  runtimelogs.txt mein likhta hai
stop()   →  loop band + final push
```

**runtimelogs.txt** — tumhara manual log  
**detailedlog.txt** — poora terminal capture (BASH_ENV se)

---

## 📋 Language-wise Import:

### 🐍 Python
```python
from log_generators.log_gen import start, log, stop

start()
log("Processing shuru!")
log("Error aaya!", "ERROR")
stop()
```

### 🟨 JavaScript (Node.js)
```javascript
const { start, log, stop } = require('./log_generators/log_gen')

start()
log("Processing shuru!")
await stop()
```

### 🔷 TypeScript
```typescript
import { start, log, stop } from './log_generators/log_gen'

start()
log("Processing shuru!")
await stop()
```

### 🐚 Bash
```bash
source ./log_generators/log_gen.sh

log_start
log "Processing shuru!"
log_stop
```

### 💎 Ruby
```ruby
require_relative '../log_generators/log_gen'

LogGen.start
LogGen.log("Processing shuru!")
LogGen.stop
```

### 🐘 PHP
```php
require_once __DIR__ . '/../log_generators/log_gen.php';

LogGen::start();
LogGen::log("Processing shuru!");
LogGen::stop();
```

### ☕ Java
```java
import log_generators.LogGen;

LogGen.start();
LogGen.log("Processing shuru!");
LogGen.stop();
```

### 🐹 Go
```go
import "your-repo/log_generators/loggen"

loggen.Start()
loggen.Log("Processing shuru!", "INFO")
loggen.Stop()
```

---

## 📄 YML — Ekdum Normal:

```yaml
- name: 📥 Checkout
  uses: actions/checkout@v4

- name: 🪵 Setup BASH_ENV (detailedlog ke liye)
  run: |
    mkdir -p output
    echo 'exec > >(tee -a "$GITHUB_WORKSPACE/output/detailedlog.txt") 2>&1' \
      > /tmp/autolog.sh
    echo "BASH_ENV=/tmp/autolog.sh" >> "$GITHUB_ENV"
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] 🚀 Started!" \
      > output/detailedlog.txt

- name: ▶️ Run Script
  run: python scripts/process_data.py   # ← bas itna!
  # log_gen andar se sab handle karta hai!
```

---

## 🎯 Output Files:

| File | Kya hai |
|------|---------|
| `output/runtimelogs.txt` | `log()` calls — clean milestones |
| `output/detailedlog.txt` | Poora terminal — install logs bhi! |
