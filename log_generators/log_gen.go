// log_gen.go — Auto-push logger (Go)
// Usage:
//   go run scripts/main.go
//   In main.go: loggen.Start(); loggen.Log("kuch bhi"); loggen.Stop()

package loggen

import (
	"crypto/md5"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"time"
)

var (
	ws       = getEnv("GITHUB_WORKSPACE", ".")
	out      = filepath.Join(ws, "output")
	runtime  = filepath.Join(out, "runtimelogs.txt")
	detailed = filepath.Join(out, "detailedlog.txt")
	lastHash string
	mu       sync.Mutex
	quit     = make(chan struct{})
)

func getEnv(k, d string) string {
	if v := os.Getenv(k); v != "" { return v }
	return d
}

func ts() string { return time.Now().UTC().Format("2006-01-02 15:04:05 UTC") }

func hash() string {
	c := ""
	for _, f := range []string{runtime, detailed} {
		if b, err := os.ReadFile(f); err == nil { c += string(b) }
	}
	return fmt.Sprintf("%x", md5.Sum([]byte(c)))
}

func git(args ...string) { exec.Command("git", append([]string{"-C", ws}, args...)...).Run() }

func push() {
	mu.Lock(); defer mu.Unlock()
	h := hash()
	if h == lastHash { return }          // kuch badla nahi — skip!
	lastHash = h
	git("add", "output/")
	if exec.Command("git", "-C", ws, "diff", "--staged", "--quiet").Run() == nil { return }
	git("commit", "-m", "🔄 "+time.Now().UTC().Format("15:04:05"))
	git("pull", "--rebase", "origin", "main")
	git("push")
}

// Log writes msg to runtimelogs.txt
func Log(msg, level string) {
	os.MkdirAll(out, 0755)
	line := fmt.Sprintf("[%s] [%s] %s\n", ts(), level, msg)
	fmt.Print(line)
	f, _ := os.OpenFile(runtime, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer f.Close()
	f.WriteString(line)
}

// Start begins background auto-push loop
func Start() {
	os.MkdirAll(out, 0755)
	Log("🚀 LogGen started!", "INFO")
	go func() {
		for {
			select {
			case <-quit: return
			case <-time.After(5 * time.Second): push()
			}
		}
	}()
}

// Stop kills loop and does final push
func Stop() {
	close(quit)
	Log("🏁 LogGen stopped — final push...", "INFO")
	push()
}
