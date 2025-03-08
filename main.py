import os
from dotenv import load_dotenv
import goodfire
from prompt import build_prompt
from parse_csv import parse_csv
import pandas as pd

def main():
    api_key = os.getenv("GOODFIRE_API_KEY")

    client = goodfire.Client(api_key=api_key)
    # Instantiate a model variant.
    variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")
    data_frame = parse_csv()
    prompt_list = build_prompt(data_frame=data_frame)
    llm_answers: list[str] = []

    for index, prompt in enumerate(prompt_list):
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

        if index == 2: break
    print(llm_answers)

        # for token in client.chat.completions.create(
        # [{"role": "user", "content": prompt}],
        # model=variant,
        # stream=True,
        # max_completion_tokens=100,
        # ):
        #     print(token.choices[0].delta.content, end="")


    # for prompt in prompt_list:
    #     message = [{"role": "user", "content": prompt}],
    #     response = client.chat.completions.create(
    #         message,
    #         model=variant,
    #         stream=True,
    #         max_completion_tokens=3,
    #     )
    #     for token in response:
    #         print(token.choices[0].delta.content, end="")

            #answer: str = token.choices[0].delta.content
            #llm_answers.append(answer)
    #data_frame["vote_prediction"] = llm_answers
    #print(llm_answers)

if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    main()
