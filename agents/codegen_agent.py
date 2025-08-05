from utils.llm_utils import run_llm_prompt

def generate_code(idea, dataset):
    prompt = f"""Generate Python demo code for the project: {idea}
    Use the dataset: {dataset}
    """
    return run_llm_prompt(prompt)
