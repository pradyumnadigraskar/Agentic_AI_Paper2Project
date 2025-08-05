### app.py
from flask import Flask, render_template, request, send_file
import os
from agents.reader_agent import extract_core_idea
from agents.dataset_agent import find_dataset
from agents.codegen_agent import generate_code
from agents.slides_agent import create_slides, generate_ppt
from utils.project_witer import save_project_structure

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['pdf']
    project_name = request.form.get('project_name', 'my_project').replace(" ", "_")

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    idea = extract_core_idea(filepath)
    dataset = find_dataset(idea)
    code = generate_code(idea, dataset)
    slides_text = create_slides(idea)

    project_path, folder_structure = save_project_structure(project_name, idea, code, dataset)


    ppt_path = generate_ppt(project_name, slides_text)

    return render_template(
        'result.html',
        idea=idea,
        dataset=dataset,
        code=code,
        slides=slides_text,
        project_file=os.path.basename(project_path),
        ppt_file=os.path.basename(ppt_path),
        folder_structure=folder_structure

    )

@app.route('/download/<filename>')
def download_file(filename):
    output_dir = os.path.abspath(os.path.join(app.root_path, 'output'))
    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        return f"File not found: {path}", 404
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)