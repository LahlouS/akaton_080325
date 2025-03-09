import os
from dotenv import load_dotenv
import goodfire
from utils.prompt import build_prompt
from utils.parse_csv import parse_csv
import pandas as pd
from ember_answers import ember_answers
# from utils.request_ember import request_ember
# from utils.write_list_to_csv import write_list_to_file
# from utils.request_ember import request_ember

def create_group(ember_answers: list[str], data_frame: pd.DataFrame):
    if (len(ember_answers) != len(data_frame)):
        raise ValueError("ember_answers data_frame not same size")
    trump_list: pd.DataFrame = pd.DataFrame()
    biden_list: pd.DataFrame = pd.DataFrame()

    for index, row in data_frame.iterrows():
        if ember_answers[index] == 'Biden':
            biden_list = pd.concat([biden_list, pd.DataFrame([row])], ignore_index=True)
        elif ember_answers[index] == 'Trump':
            trump_list = pd.concat([trump_list, pd.DataFrame([row])], ignore_index=True)
    return trump_list, biden_list



def main():
    data_frame = parse_csv()
    prompt_list = build_prompt(data_frame=data_frame)
    # llm_answers = request_ember(prompt_list, 0, len(prompt_list))
    # write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')\
    trump_list, biden_list = create_group(ember_answers, data_frame)

    print(trump_list, biden_list)
    # TODO : build format : [{ "role": "user", "content": "TWEET"},{"role": "assistant", "content": "Biden"}],



if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    main()
