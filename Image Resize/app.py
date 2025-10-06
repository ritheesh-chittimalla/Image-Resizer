import os
from flask import Flask, request, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "resized"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        # Save original upload
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Resize & convert
        size = (800, 800)  # default
        output_format = request.form.get("format", "JPEG")

        try:
            with Image.open(filepath) as img:
                img = img.resize(size, Image.Resampling.LANCZOS)

                new_filename = os.path.splitext(file.filename)[0] + "." + output_format.lower()
                output_path = os.path.join(OUTPUT_FOLDER, new_filename)

                img.save(output_path, output_format)
        except Exception as e:
            return f"Error: {e}", 500

        return render_template("index.html", success=True, filename=new_filename)

    return render_template("index.html")

@app.route("/resized/<filename>")
def resized_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
