import subprocess

def run_llm_prompt(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral:latest"],
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"  # 💥 Fixes UnicodeEncodeError
    )

    if result.returncode != 0:
        print("⚠️ Ollama Error:", result.stderr)
        return "(Error calling Ollama)"
    
    return result.stdout.strip()


def generate_folder_structure_from_idea(idea):
    prompt = f"""
    You're an expert software architect.

    Based on the following project idea, design a suitable Python project folder structure.
    
    Project Idea: "{idea}"

    Return only a folder tree structure using this format (no explanation):
    ```
    project_name/
    ├── folder/
    │   └── file.py
    └── README.md
    ```
    """
    return run_llm_prompt(prompt)
