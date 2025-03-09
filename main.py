from dotenv import load_dotenv
import pandas as pd
from utils.prompt import build_basic_prompt
from utils.parse_csv import parse_csv
from ember_answers import ember_answers
from utils.create_df_group import create_df_group
from utils.get_features_by_contrast import get_features_by_contrast
import os
from utils.request_ember import infer_with_features, request_ember
from utils.write_list_to_csv import write_list_to_file
from utils.request_ember import request_ember

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


def main():
    data_frame = parse_csv()
    prompt_list = build_basic_prompt(data_frame=data_frame)
    llm_answers = request_ember(prompt_list)
    write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')
    # TODO: test avec les prompts plutot que la dataframe et regarder les features les plus pertinentes
    df_trump_list, df_biden_list = create_df_group(ember_answers, data_frame)

	biden_conversation = build_conversation_list(df_biden_list, "Biden")
	trump_conversation = build_conversation_list(df_trump_list, "Trump")

    assert(len(biden_conversation) == len(df_biden_list) == ember_answers.count("Biden"))
    assert(len(trump_conversation) == len(df_trump_list) == ember_answers.count("Trump"))
    biden_features, trump_features = get_features_by_contrast(
        biden_conversation[:60], trump_conversation[:60])
    features_coverage_pipeline(
        data_frame=data_frame,
        llm_answers=llm_answers,
        biden_features=biden_features,
        trump_features=trump_features
    )

if __name__ == "__main__":
	# Load .env file
	load_dotenv()
	main()
