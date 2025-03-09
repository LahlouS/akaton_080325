import os
import goodfire
from utils.prompt import build_features_prompt
import pandas as pd

def slice_list(list_to_slice: list, start: int = -1, end: int = -1):
    if start > -1:
        list_to_slice = list_to_slice[start:]
    if end > -1:
        list_to_slice = list_to_slice[:end]
    return list_to_slice

def request_ember(prompt_list: list[str], start: int = -1, end: int = -1) -> list[str]:
    """
    Requests goodfire with our prompt_list[start] to our prompt_list[end]
    """
    client = goodfire.Client(os.getenv("GOODFIRE_API_KEY"))

    # Instantiate a model variant.
    variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")
    slice_list(prompt_list, start=start, end=end)
    llm_answers: list[str] = []
    for _index, prompt in enumerate(prompt_list):
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


def infer_with_features(data_frame: pd.DataFrame, features: list[str], start: int = -1, end: int = -1) -> list[str]:
    return request_ember(
        prompt_list=build_features_prompt(
            data_frame=data_frame,
            features=features
        ), start=start, end=end)
