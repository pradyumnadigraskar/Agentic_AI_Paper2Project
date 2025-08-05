from utils.ocr_utils import extract_text_from_pdf
from utils.llm_utils import run_llm_prompt

def extract_core_idea(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    prompt = f"""You are an AI assistant. Extract the core idea of the following research paper:
    {extracted_text[:2000]}..."""
    return run_llm_prompt(prompt)
