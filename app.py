import os
import tempfile
from flask import Flask, flash, request, redirect, url_for, send_from_directory, after_this_request, render_template, url_for, jsonify
from werkzeug.utils import secure_filename
from modularise import converter_image_to_csv
import uuid

UPLOAD_FOLDER = "generated_csv"
ALLOWED_EXTENSIONS = ["txt", "pdf", "png", "jpg", "jpeg", "gif"]

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "I am the best"


def allow_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method  == "POST":
        # return "I enter here"
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        
        if file:
            if (allow_file(file.filename) == False):
                return jsonify({"error": "Invalid file format"}), 400
            filename = secure_filename(file.filename)
            with tempfile.TemporaryDirectory() as temp_dir:
                output_name = f"{uuid.uuid4()}.csv"
                temp_file_path = os.path.join(temp_dir, filename)
                file.save(temp_file_path)
                return_value = converter_image_to_csv(temp_file_path, output_name)
                if return_value is None:
                    return jsonify({"error": "Image doesn't contain table"}), 400

            output_path = f"{app.config["UPLOAD_FOLDER"]}/{output_name}"
                        
            file_url = url_for("download_file", filename=output_name)
            return jsonify({"file_url": file_url, "filename": output_name})
        else:
            return jsonify({"error": "No file uploaded"}), 400
        
    return render_template("homepage.html")

@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):

    @after_this_request
    def remove_file(response):
        os.remove(f"{app.config["UPLOAD_FOLDER"]}/{filename}")
        return response
    
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)