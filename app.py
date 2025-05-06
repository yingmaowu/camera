from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400

    # 🔺從這裡開始：新增讀取病人 ID
    patient_id = request.form.get('patient_id', '').strip()
    if not patient_id:
        return "Missing patient ID", 400

    # 建立病人專屬資料夾
    patient_folder = os.path.join(UPLOAD_FOLDER, patient_id)
    os.makedirs(patient_folder, exist_ok=True)

    # 儲存檔案
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{patient_id}_{timestamp}.jpg"
    filepath = os.path.join(patient_folder, filename)
    image.save(filepath)

    return f"Uploaded {filename}", 200


# 列出歷史照片
@app.route("/photos", methods=["GET"])
def list_photos():
    patient_id = request.args.get("patient", "").strip()
    if not patient_id:
        return jsonify([])

    folder = os.path.join(UPLOAD_FOLDER, patient_id)
    if not os.path.exists(folder):
        return jsonify([])

    files = sorted(os.listdir(folder), reverse=True)
    urls = [f"/uploads/{patient_id}/{fname}" for fname in files]
    return jsonify(urls)


# 顯示上傳的圖片
@app.route("/uploads/<patient>/<filename>")
def uploaded_file(patient, filename):
    folder = os.path.join(UPLOAD_FOLDER, patient)
    return send_from_directory(folder, filename)

