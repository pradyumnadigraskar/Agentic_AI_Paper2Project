import os
from utils.llm_utils import generate_folder_structure_from_idea

OUTPUT_FOLDER = 'output'

def save_project_structure(project_name, idea, code, dataset):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    project_file = f"{project_name}_project.py"
    project_path = os.path.join(OUTPUT_FOLDER, project_file)

    # Ask LLM to suggest folder structure
    folder_structure = generate_folder_structure_from_idea(idea)

    # Extract folders & files from folder_structure (roughly)
    lines = folder_structure.strip().splitlines()
    parsed_lines = [line.strip('│├└─ ') for line in lines if line.strip() and not line.startswith('```')]
    relative_paths = [line for line in parsed_lines if '/' in line or line.endswith('.py') or line.endswith('.md')]

    scaffold_lines = [
        '    base = os.path.abspath(os.path.dirname(__file__))',
        f'    project_root = os.path.join(base, "{project_name}")',
        f'    os.makedirs(project_root, exist_ok=True)',
        f'    print("📁 Creating project at", project_root)',
        '',
        '    # Create folders and files',
    ]

    for path in relative_paths:
        if path.endswith('/'):
            scaffold_lines.append(f'    os.makedirs(os.path.join(project_root, "{path.strip("/")}"), exist_ok=True)')
        else:
            scaffold_lines.append(
                f'    with open(os.path.join(project_root, "{path}"), "w", encoding="utf-8") as f:\n'
                f'        f.write("# File: {path}\\n")'
            )

    scaffold_script = f'''# Auto-generated scaffold script for: {project_name}

import os

def scaffold():
{chr(10).join(scaffold_lines)}

if __name__ == "__main__":
    scaffold()
'''

    with open(project_path, 'w', encoding='utf-8') as f:
        f.write(scaffold_script)

    return project_path, folder_structure.strip()
