from flask import request,app, jsonify
from .AI_logic import *
from . import *

@app.route('/pdf_text', methods=['POST'])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded PDF temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Summarize extracted text
    summarized_text = summarize(extracted_text)

    # Delete file after processing
    os.remove(file_path)

    return jsonify({
        "summary": summarized_text
    })