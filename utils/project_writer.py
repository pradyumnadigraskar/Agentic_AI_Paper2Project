import os

def save_project_structure(project_name, idea, code):
    print("LOG: Writing Project Setup Script...")
    folder_structure = f"{project_name}/\n├── src/\n│   └── main.py\n├── requirements.txt\n└── README.md"
    
    scaffold = f'''
import os
def build():
    root = "{project_name}"
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    files = {{
        "README.md": "# {project_name}\\n\\nIdea: {idea}",
        "requirements.txt": "pandas\\nnumpy\\nmatplotlib",
        "src/main.py": {repr(code)}
    }}
    for path, content in files.items():
        with open(os.path.join(root, path), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"✅ Project '{{root}}' built successfully!")
if __name__ == "__main__":
    build()
'''
    file_name = f"{project_name}_builder.py"
    with open(os.path.join("output", file_name), "w", encoding="utf-8") as f:
        f.write(scaffold.strip())
    return file_name, folder_structure