from dotenv import load_dotenv
import pandas as pd
from utils.prompt import build_basic_prompt
from utils.parse_csv import parse_csv
from ember_answers import ember_answers
from utils.create_df_group import create_df_group
# from utils.request_ember import request_ember
# from utils.write_list_to_csv import write_list_to_file
# from utils.request_ember import request_ember


def build_conversation(user_input_list: pd.DataFrame, llm_output: str) -> list[list[dict[str, str]]]:
    # Construct the list of conversation pairs
    return [[{"role": "user", "content": str(user_input.to_dict())},
         {"role": "assistant", "content": llm_output}]
        for _, user_input in user_input_list.iterrows()]

def main():
    data_frame = parse_csv()
    prompt_list = build_basic_prompt(data_frame=data_frame)
    # llm_answers = request_ember(prompt_list)
    # write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')\
    df_trump_list, df_biden_list = create_df_group(ember_answers, data_frame)

    biden_conversation = build_conversation(df_biden_list, "Biden")
    trump_conversation = build_conversation(df_trump_list, "Trump")
    assert(len(biden_conversation) == len(df_biden_list) == ember_answers.count("Biden"))
    assert(len(trump_conversation) == len(df_trump_list) == ember_answers.count("Trump"))

if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    main()
