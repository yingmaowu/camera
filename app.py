from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 首頁 - index.html
@app.route("/")
def home():
    return render_template("index.html")

# 查看歷史照片 - history.html
@app.route("/history")
def history():
    return render_template("history.html")

# 上傳照片
@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"tongue_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)
    return f"Uploaded {filename}", 200

# 列出歷史照片
@app.route("/photos", methods=["GET"])
def list_photos():
    files = os.listdir(UPLOAD_FOLDER)
    files = sorted(files, reverse=True)
    urls = [f"/uploads/{fname}" for fname in files]
    return jsonify(urls)

# 顯示上傳的圖片
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
