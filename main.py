from dotenv import load_dotenv
import pandas as pd
from utils.prompt import build_basic_prompt
from utils.parse_csv import parse_csv
from ember_answers import ember_answers
from utils.create_df_group import create_list_group_based_on_prompt
from utils.get_features_by_contrast import get_features_by_contrast
import os
from utils.request_ember import infer_with_features, request_ember
from utils.write_list_to_file import write_list_to_file
from utils.request_ember import request_ember
from utils.get_sorted_features_by_inspect import get_sorted_features_by_inspect

api_key = os.getenv("GOODFIRE_API_KEY")

def build_conversation_list(user_input_list: pd.DataFrame, llm_output: str) -> list[list[dict[str, str]]]:
	"""creates a list of conversation between user and ember -> llama"""
	# Construct the list of conversation pairs
	return [[{"role": "user", "content": str(user_input.to_dict())},
		 {"role": "assistant", "content": llm_output}]
		for _, user_input in user_input_list.iterrows()]


def features_coverage_pipeline(
    data_frame: pd.DataFrame,
    llm_answers: list[str],
    biden_features: list[str],
    trump_features: list[str]
):
    llm_features_answers_biden: list[str] = infer_with_features(
        data_frame=data_frame, features=list(biden_features)[:20])
    llm_features_answers_trump: list[str] = infer_with_features(
        data_frame=data_frame, features=list(trump_features)[:20])
    llm_features_answers_biden = llm_features_answers_biden[:60]
    llm_features_answers_trump = llm_features_answers_trump[:60]
    llm_answers = llm_answers[:60]

    llm_features_answers: list[str] = []
    for biden_answer, trump_answer in zip(llm_features_answers_biden, llm_features_answers_trump):
        if biden_answer == trump_answer:
            llm_features_answers.append(biden_answer)
        elif biden_answer != "neutral" and trump_answer == "neutral":
            llm_features_answers.append(biden_answer)
        elif trump_answer != "neutral" and biden_answer == "neutral":
            llm_features_answers.append(trump_answer)
        elif trump_answer != biden_answer:
            llm_answers.append("neutral")
        else:
            llm_answers.append(biden_answer)
    assert len(llm_features_answers) == len(llm_features_answers_biden)
    assert len(llm_features_answers) == len(llm_features_answers_trump)


def from_df_to_conversation_list(user_input_list: pd.DataFrame, llm_output: str) -> list[list[dict[str, str]]]:
    """format a DataFrame into ember "conversation" format """
    # Construct the list of conversation pairs

    return [[{"role": "user", "content": str(user_input.to_dict())},
         {"role": "assistant", "content": llm_output}]
        for _, user_input in user_input_list.iterrows()]


def from_input_to_conversation_list(user_input_list: list, llm_output: str):
    """format a list of input into ember "conversation" format """
    return [
        [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": llm_output}
        ] for user_input in user_input_list
    ]

def main():
    data_frame = parse_csv()
    prompt_list = build_basic_prompt(data_frame=data_frame)
    llm_answers = request_ember(prompt_list)
    write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')

    biden_prompt_list, trump_prompt_list = create_list_group_based_on_prompt(ember_answers, prompt_list)
    print(len(trump_prompt_list))
    print(len(biden_prompt_list))
    biden_conversation = from_input_to_conversation_list(biden_prompt_list, "Biden")
    trump_conversation = from_input_to_conversation_list(trump_prompt_list, "Trump")

    assert(len(biden_conversation) == len(biden_prompt_list) == ember_answers.count("Biden"))
    assert(len(trump_conversation) == len(trump_prompt_list) == ember_answers.count("Trump"))
    biden_top_features_by_inspect_score, biden_top_features_by_inspect = get_sorted_features_by_inspect(biden_conversation)
    trump_top_features_by_inspect_score, trump_top_features_by_inspect = get_sorted_features_by_inspect(trump_conversation)
    write_list_to_file(biden_top_features_by_inspect_score, "result/biden_top_features_by_inspect_score.txt")
    write_list_to_file(biden_top_features_by_inspect, "result/biden_top_features_by_inspect.txt")
    write_list_to_file(trump_top_features_by_inspect_score, "result/trump_top_features_by_inspect_score.txt")
    write_list_to_file(trump_top_features_by_inspect, "result/trump_top_features_by_inspect.txt")
    features_coverage_pipeline(
        data_frame=data_frame,
        llm_answers=llm_answers,
        biden_features=biden_top_features_by_inspect[:10],
        trump_features=trump_top_features_by_inspect[:10]
    )

if __name__ == "__main__":
	# Load .env file
    load_dotenv()
    main()
