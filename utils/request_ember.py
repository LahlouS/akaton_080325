import os
import goodfire
from prompt import build_prompt
from parse_csv import parse_csv


def request_ember(prompt_list: list[str], start: int, end: int) -> list[str]:
    """
    Requests goodfire with our prompt_list[start] to our prompt_list[end]
    """
    api_key = os.getenv("GOODFIRE_API_KEY")

    client = goodfire.Client(api_key=api_key)
    # Instantiate a model variant.
    variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")
    llm_answers: list[str] = []
    for index, prompt in enumerate(prompt_list[start:]):
        if index == end: break
        tokens = list(client.chat.completions.create(
        [{"role": "user", "content": prompt}],
        model=variant,
        stream=True,
        max_completion_tokens=100,
        ))
        word = ''
        for token in tokens:
            word += token.choices[0].delta.content
        llm_answers.append(word)
    return llm_answers
