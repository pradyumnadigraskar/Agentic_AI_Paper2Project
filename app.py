import os, shutil
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from services.llm_factory import LLMProvider
from services.reader_agent import extract_core_idea
from services.slides_agent import create_slides, generate_ppt
from utils.project_writer import save_project_structure

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/process")
async def process(request: Request, project_name: str = Form(...), llm_choice: str = Form("ollama"), pdf: UploadFile = File(...)):
    print(f"\n--- NEW REQUEST: {project_name} using {llm_choice} ---")
    try:
        # Save PDF
        pdf_path = os.path.join("uploads", pdf.filename)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        
        llm = LLMProvider(provider=llm_choice)
        
        # Run Agents
        idea = extract_core_idea(pdf_path, llm)
        dataset_info = llm.generate(f"Suggest one public dataset for: {idea}")
        code = llm.generate(f"Write complete Python code for: {idea}")
        slides_text = create_slides(idea, llm)
        
        # Save Files
        clean_name = project_name.replace(" ", "_")
        proj_file, struct = save_project_structure(clean_name, idea, code)
        ppt_file = generate_ppt(clean_name, slides_text)

        print("LOG: All agents finished. Sending results to UI.\n")
        return templates.TemplateResponse("result.html", {
            "request": request, "idea": idea, "dataset": dataset_info,
            "folder_structure": struct, "slides": slides_text,
            "project_file": proj_file, "ppt_file": ppt_file
        })
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(path=os.path.join("output", filename), filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)