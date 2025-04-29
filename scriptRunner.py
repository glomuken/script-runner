from flask import Flask, request, jsonify, abort
import os
import subprocess

app = Flask(__name__)

SCRIPTS_DIR = "./scripts"

@app.route("/scripts", methods=["GET"])
def list_scripts():
    try:
        files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py")]
        return jsonify({"scripts": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/run/<script>", methods=["POST"])
def run_script(script):
    script_path = os.path.join(SCRIPTS_DIR, script)
    if not os.path.exists(script_path):
        abort(404, description="Script not found")
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

@app.route("/upload", methods=["POST"])
def upload_script():
    if "file" not in request.files:
        abort(400, description="No file part")
    file = request.files["file"]
    if file.filename == "":
        abort(400, description="No selected file")
    path = os.path.join(SCRIPTS_DIR, file.filename)
    file.save(path)
    return jsonify({"message": "Script uploaded", "filename": file.filename})

if __name__ == "__main__":
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    app.run(debug=True)
