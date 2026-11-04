import os
import platform
import time
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
START_TIME = time.time()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Next-Gen Flask Microservice</title>
    <style>
        :root {
            --bg: #030712;
            --card-bg: rgba(17, 24, 39, 0.7);
            --border: rgba(255, 255, 255, 0.08);
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.15);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --success: #34d399;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text-main); display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; position: relative; }
        
        /* Background Glow Orbs */
        .orb { position: absolute; width: 400px; height: 400px; border-radius: 50%; filter: blur(120px); z-index: -1; opacity: 0.4; }
        .orb-1 { background: #4f46e5; top: -100px; left: -100px; }
        .orb-2 { background: #06b6d4; bottom: -100px; right: -100px; }

        .dashboard { background: var(--card-bg); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: 24px; padding: 40px; width: 100%; max-width: 520px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); }
        
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .status-badge { display: flex; align-items: center; gap: 8px; background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.2); color: var(--success); padding: 6px 14px; border-radius: 99px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .status-dot { width: 8px; height: 8px; background: var(--success); border-radius: 50%; box-shadow: 0 0 10px var(--success); animation: pulse 2s infinite; }
        
        h1 { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.025em; margin-bottom: 8px; background: linear-gradient(to right, #fff, var(--text-muted)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.subtitle { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 30px; }

        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
        .metric-card { background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border); border-radius: 16px; padding: 18px; transition: all 0.3s ease; }
        .metric-card:hover { border-color: rgba(56, 189, 248, 0.3); background: var(--accent-glow); transform: translateY(-2px); }
        .metric-label { color: var(--text-muted); font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
        .metric-value { color: var(--text-main); font-size: 1.1rem; font-weight: 600; font-family: ui-monospace, monospace; }

        .actions { display: flex; gap: 12px; }
        .btn { flex: 1; background: var(--text-main); color: var(--bg); border: none; padding: 12px 20px; border-radius: 12px; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s ease; text-decoration: none; text-align: center; }
        .btn:hover { background: var(--accent); box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
        .btn-outline { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
        .btn-outline:hover { background: rgba(255, 255, 255, 0.05); border-color: var(--text-muted); box-shadow: none; }

        .footer { margin-top: 30px; text-align: center; font-size: 0.75rem; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 20px; }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 15px var(--success); }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>

    <div class="dashboard">
        <div class="header">
            <div>
                <h1>AetherCore</h1>
                <p class="subtitle">Cloud Native Python Runtime</p>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                Active
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Runtime</div>
                <div class="metric-value">Python {{ python_version }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Environment</div>
                <div class="metric-value">{{ env }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Host Platform</div>
                <div class="metric-value">{{ os_info }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Container Uptime</div>
                <div class="metric-value" id="uptime">{{ uptime }}s</div>
            </div>
        </div>

        <div class="actions">
            <a href="/health" class="btn">Inspect Health API</a>
            <button class="btn btn-outline" onclick="location.reload()">Refresh State</button>
        </div>

        <div class="footer">
            <span>Dockerized Deployment</span>
            <span>{{ current_time }}</span>
        </div>
    </div>

    <script>
        // Live client-side uptime incrementer sync
        let uptimeSec = parseInt("{{ uptime }}");
        setInterval(() => {
            uptimeSec++;
            document.getElementById('uptime').innerText = uptimeSec + 's';
        }, 1000);
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    uptime = int(time.time() - START_TIME)
    return render_template_string(
        HTML_TEMPLATE,
        os_info=platform.system(),
        python_version=platform.python_version(),
        uptime=uptime,
        env=os.getenv("APP_ENV", "Production"),
        current_time=datetime.utcnow().strftime("%H:%M:%S UTC")
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": int(time.time() - START_TIME)
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
