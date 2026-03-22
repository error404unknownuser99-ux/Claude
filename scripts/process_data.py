import os, base64, json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import requests as req

LOG_FILE = "output/runtimelogs.txt"
os.makedirs("output", exist_ok=True)

def log(msg, level="INFO"):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] [{level}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>🎨 AI Image Generator</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    min-height: 100vh;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    font-family: 'Segoe UI', sans-serif;
    display: flex; flex-direction: column; align-items: center;
    padding: 40px 20px; color: white;
  }
  h1 {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px; text-align: center;
  }
  .subtitle { color: #94a3b8; margin-bottom: 40px; font-size: 1rem; }
  .card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 35px;
    width: 100%; max-width: 600px;
    backdrop-filter: blur(10px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
  }
  label { display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase; }
  textarea {
    width: 100%; padding: 14px 18px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px; color: white; font-size: 1rem;
    resize: vertical; min-height: 90px; outline: none;
    transition: border 0.3s;
  }
  textarea:focus { border-color: #a78bfa; }
  textarea::placeholder { color: #475569; }
  button {
    width: 100%; margin-top: 18px; padding: 15px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border: none; border-radius: 12px;
    color: white; font-size: 1.1rem; font-weight: 700;
    cursor: pointer; transition: all 0.3s;
  }
  button:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(124,58,237,0.5); }
  button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
  .result-box { margin-top: 30px; text-align: center; display: none; }
  .result-box img {
    width: 100%; border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
  }
  .loading { display: none; text-align: center; margin-top: 25px; color: #a78bfa; font-size: 1rem; }
  .spinner {
    display: inline-block; width: 28px; height: 28px;
    border: 3px solid rgba(167,139,250,0.3);
    border-top-color: #a78bfa; border-radius: 50%;
    animation: spin 0.8s linear infinite; margin-right: 10px; vertical-align: middle;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .error { color: #f87171; margin-top: 15px; font-size: 0.9rem; text-align: center; display: none; }
  .download-btn {
    display: none; margin-top: 15px; padding: 10px 25px;
    background: rgba(52,211,153,0.2); border: 1px solid #34d399;
    border-radius: 10px; color: #34d399; cursor: pointer;
    font-size: 0.95rem; width: auto;
  }
  .badge { display: inline-block; padding: 4px 12px; background: rgba(52,211,153,0.15); border: 1px solid #34d399; border-radius: 20px; color: #34d399; font-size: 0.75rem; margin-bottom: 25px; }
  .timer { color: #fbbf24; font-size: 0.85rem; margin-top: 10px; }
</style>
</head>
<body>
<h1>🎨 AI Image Generator</h1>
<p class="subtitle">Powered by Stable Diffusion • GitHub Actions</p>
<span class="badge">✅ LIVE</span>
<div class="card">
  <label>✏️ Describe your image</label>
  <textarea id="prompt" placeholder="e.g. a futuristic city at night, neon lights, cyberpunk style..."></textarea>
  <button id="genBtn" onclick="generate()">✨ Generate Image</button>
  <div class="loading" id="loading"><span class="spinner"></span> Generating... (20-40 sec)</div>
  <div class="error" id="errorMsg"></div>
  <div class="result-box" id="resultBox">
    <img id="resultImg" src="" alt="Generated Image"/>
    <br/>
    <button class="download-btn" id="dlBtn" onclick="downloadImg()">⬇️ Download Image</button>
  </div>
</div>
<script>
async function generate() {
  const prompt = document.getElementById('prompt').value.trim();
  if (!prompt) { alert('Prompt likhna bhool gaye! 😅'); return; }
  document.getElementById('genBtn').disabled = true;
  document.getElementById('loading').style.display = 'block';
  document.getElementById('resultBox').style.display = 'none';
  document.getElementById('errorMsg').style.display = 'none';
  try {
    const resp = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({prompt})
    });
    const data = await resp.json();
    if (data.image) {
      document.getElementById('resultImg').src = 'data:image/png;base64,' + data.image;
      document.getElementById('resultBox').style.display = 'block';
      document.getElementById('dlBtn').style.display = 'inline-block';
    } else { throw new Error(data.error || 'Unknown error'); }
  } catch(e) {
    document.getElementById('errorMsg').textContent = '❌ Error: ' + e.message;
    document.getElementById('errorMsg').style.display = 'block';
  } finally {
    document.getElementById('genBtn').disabled = false;
    document.getElementById('loading').style.display = 'none';
  }
}
function downloadImg() {
  const a = document.createElement('a');
  a.href = document.getElementById('resultImg').src;
  a.download = 'ai_generated.png'; a.click();
}
document.getElementById('prompt').addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'Enter') generate();
});
</script>
</body>
</html>"""

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    log(f"🎨 Generate request: '{prompt}'")
    try:
        # ✅ New HuggingFace router URL
        api_url = "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5"
        headers = {"Content-Type": "application/json"}
        payload = {"inputs": prompt}
        response = req.post(api_url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            img_b64 = base64.b64encode(response.content).decode('utf-8')
            log(f"✅ Image generated successfully!")
            return jsonify({"image": img_b64})
        else:
            err = response.text[:300]
            log(f"❌ HF API error {response.status_code}: {err}", "ERROR")
            return jsonify({"error": f"API Error {response.status_code}: {err}"}), 500
    except Exception as e:
        log(f"❌ Exception: {e}", "ERROR")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    log("🚀 Flask server starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
