"""Flask HTML report service for the Dify data-visualization workflow."""
import os
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)
SAVE_DIR = Path(os.getenv("REPORT_SAVE_DIR", "/app/static_files"))
SAVE_DIR.mkdir(parents=True, exist_ok=True)
PORT = int(os.getenv("PORT", "5000"))
PUBLIC_BASE_URL = os.getenv("REPORT_PUBLIC_BASE_URL", "http://localhost:5000").rstrip("/")
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_HTML_BYTES", str(5 * 1024 * 1024)))

@app.get("/")
def home():
    return "HTML report service is running"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/upload_html")
def upload_html():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "JSON body required"}), 400
    html = data.get("html_content")
    if not isinstance(html, str) or not html.strip():
        return jsonify({"status": "error", "message": "html_content cannot be empty"}), 400
    filename = f"report_{uuid.uuid4().hex}.html"
    (SAVE_DIR / filename).write_text(html, encoding="utf-8")
    return jsonify({"status": "success", "download_url": f"{PUBLIC_BASE_URL}/download/{filename}"})

@app.get("/download/<filename>")
def download(filename):
    return send_from_directory(str(SAVE_DIR), filename, mimetype="text/html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
