import os
import pytesseract
from pdf2image import convert_from_path

def extract_core_idea(pdf_path, llm_provider):
    tesseract_path = os.getenv("TESSERACT_PATH")
    poppler_path = os.getenv("POPPLER_PATH")
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    print("LOG: Converting PDF to images...")
    pages = convert_from_path(pdf_path, first_page=1, last_page=3, poppler_path=poppler_path)
    
    print("LOG: Extracting text via OCR...")
    full_text = ""
    for page in pages:
        full_text += pytesseract.image_to_string(page)
    
    print(f"LOG: OCR Complete. Extracted {len(full_text)} characters.")
    
    prompt = f"Extract a concise Python project idea from this research paper text: {full_text[:3000]}"
    return llm_provider.generate(prompt)