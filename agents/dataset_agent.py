from utils.llm_utils import run_llm_prompt

def find_dataset(idea):
    prompt = f"Suggest a public dataset for the following project idea: {idea}"
    return run_llm_prompt(prompt)
