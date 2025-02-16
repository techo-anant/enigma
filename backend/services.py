import requests
import os
import fitz  # PyMuPDF

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"

# Get API key securely
API_KEY = os.environ.get("Hugging_Face_Api_key")
if not API_KEY:
    raise ValueError("Hugging Face API key is missing! Set it as an environment variable.")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Summarization function
def summarize(message):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": message})
        data = response.json()

        # Handle errors properly
        if response.status_code == 200 and isinstance(data, list) and "generated_text" in data[0]:
            return {"generated_text": data[0]["generated_text"]}
        else:
            return {"error": f"Summarization failed: {data}"}
    except Exception as e:
        return {"error": str(e)}

# Extract text from PDF with better formatting
def extract_text_from_pdf(file_path):
    text = ""
    try:
        pdf_document = fitz.open(file_path)
        for page in pdf_document:
            text += page.get_text("text", sort=True, block_separator="\n\n")  # Fix spacing issue
        return text.strip()
    except Exception as e:
        return str(e)