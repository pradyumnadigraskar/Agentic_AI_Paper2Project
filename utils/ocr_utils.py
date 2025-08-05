import pytesseract
from pdf2image import convert_from_path
import os

# Set the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"D:\exam study\Tesseract\tesrt\tesseract.exe"

# Set your Poppler path here
POPPLER_PATH = r"D:\download\Release-24.08.0-0\poppler-24.08.0\Library\bin" # <-- UPDATE this if different

def extract_text_from_pdf(pdf_path):
    # Pass poppler_path to avoid PDFInfoNotInstalledError
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text
