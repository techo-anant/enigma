import requests
import os
import fitz  # PyMuPDF


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
