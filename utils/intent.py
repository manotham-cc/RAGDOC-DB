from core.llm import get_llm_response
from utils.load_prompt_txt import load_prompt_template
def classify_intent(question: str) -> str:
    """Classify user question into 'sql' or 'doc'."""
    prompt_template = load_prompt_template("prompt_templates/intent_classification_prompt.txt")

    final_prompt = prompt_template.format(
        user_question=question
        
    )

    return get_llm_response(final_prompt,question).strip().lower()
