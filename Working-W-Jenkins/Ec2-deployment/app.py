import os
import socket
from datetime import datetime

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "1.0")
HOSTNAME = socket.gethostname()

tasks = []
next_id = 1

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TaskBoard</title>
<style>
  :root { --bg:#0f172a; --card:#1e293b; --text:#e2e8f0; --muted:#94a3b8; --accent:#38bdf8; --ok:#4ade80; --bad:#f87171; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: system-ui, sans-serif; background:var(--bg); color:var(--text); }
  .wrap { max-width: 640px; margin: 40px auto; padding: 0 16px; }
  h1 { margin:0 0 4px; }
  .sub { color:var(--muted); margin-bottom:24px; }
  .stats { display:flex; gap:12px; margin-bottom:20px; }
  .stat { flex:1; background:var(--card); border-radius:12px; padding:14px; text-align:center; }
  .stat b { display:block; font-size:24px; color:var(--accent); }
  form { display:flex; gap:8px; margin-bottom:20px; }
  input { flex:1; padding:12px; border-radius:10px; border:1px solid #334155; background:var(--card); color:var(--text); font-size:16px; }
  button { padding:12px 18px; border:0; border-radius:10px; background:var(--accent); color:#0f172a; font-weight:600; cursor:pointer; }
  ul { list-style:none; padding:0; margin:0; }
  li { display:flex; align-items:center; gap:10px; background:var(--card); padding:12px 14px; border-radius:10px; margin-bottom:8px; }
  li span { flex:1; }
  li.done span { text-decoration: line-through; color:var(--muted); }
  .icon { background:transparent; color:var(--muted); padding:4px 8px; font-size:18px; }
  .icon:hover { color:var(--text); }
  footer { margin-top:30px; padding:14px; background:var(--card); border-radius:12px; color:var(--muted); font-size:14px; }
  footer code { color:var(--ok); }
  .empty { text-align:center; color:var(--muted); padding:24px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>TaskBoard</h1>
  <div class="sub">A tiny task manager deployed by a Jenkins CI/CD pipeline</div>

  <div class="stats">
    <div class="stat"><b id="s-total">0</b>Total</div>
    <div class="stat"><b id="s-open">0</b>Open</div>
    <div class="stat"><b id="s-done">0</b>Done</div>
  </div>

  <form id="add-form">
    <input id="title" placeholder="What needs to be done?" autocomplete="off" required>
    <button type="submit">Add</button>
  </form>

  <ul id="list"></ul>

  <footer>
    Version <code>{{ version }}</code> &middot; served by <code>{{ hostname }}</code>
  </footer>
</div>

<script>
async function api(path, options) {
  const res = await fetch(path, options);
  return res.json();
}

async function load() {
  const data = await api('/api/tasks');
  const list = document.getElementById('list');
  list.innerHTML = '';
  if (data.tasks.length === 0) {
    list.innerHTML = '<div class="empty">No tasks yet. Add one above.</div>';
  }
  data.tasks.forEach(t => {
    const li = document.createElement('li');
    if (t.done) li.className = 'done';
    li.innerHTML = '<button class="icon" title="Toggle">' + (t.done ? '&#9745;' : '&#9744;') + '</button>'
                 + '<span></span><button class="icon" title="Delete">&#10005;</button>';
    li.querySelector('span').textContent = t.title;
    const [toggle, del] = li.querySelectorAll('button');
    toggle.onclick = async () => { await api('/api/tasks/' + t.id, {method:'PUT'}); load(); };
    del.onclick = async () => { await api('/api/tasks/' + t.id, {method:'DELETE'}); load(); };
    list.appendChild(li);
  });
  document.getElementById('s-total').textContent = data.stats.total;
  document.getElementById('s-open').textContent = data.stats.open;
  document.getElementById('s-done').textContent = data.stats.done;
}

document.getElementById('add-form').onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById('title');
  await api('/api/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title: input.value})
  });
  input.value = '';
  load();
};

load();
</script>
</body>
</html>
"""


def stats():
    done = sum(1 for t in tasks if t["done"])
    return {"total": len(tasks), "open": len(tasks) - done, "done": done}


@app.route("/")
def home():
    return render_template_string(PAGE, version=VERSION, hostname=HOSTNAME)


@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION, host=HOSTNAME)


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks=tasks, stats=stats())


@app.route("/api/tasks", methods=["POST"])
def add_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = {
        "id": next_id,
        "title": title[:200],
        "done": False,
        "created": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify(error="not found"), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return jsonify(deleted=task_id)
    return jsonify(error="not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
