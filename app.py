# app.py

from flask import Flask, render_template, request, redirect, send_file, url_for
import os
from compress import compress_file
from decompress import decompress_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['file']
    if file:
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Compress file
        output_path = os.path.join(PROCESSED_FOLDER, f"{file.filename}.compressed")
        compress_file(input_path, output_path)

        return render_template('result.html', operation="Compression", file_url=url_for('download_file', filename=f"{file.filename}.compressed"))

@app.route('/decompress', methods=['POST'])
def decompress():
    file = request.files['file']
    if file:
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Decompress file
        output_name = file.filename.rsplit('.', 1)[0] + ".txt"  # Ensure output is .txt
        output_path = os.path.join(PROCESSED_FOLDER, output_name)
        decompress_file(input_path, output_path)

        return render_template('result.html', operation="Decompression", file_url=url_for('download_file', filename=output_name))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

