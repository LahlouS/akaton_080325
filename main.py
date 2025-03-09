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



def main():
	data_frame = parse_csv()
	prompt_list = build_basic_prompt(data_frame=data_frame)
	llm_answers = request_ember(prompt_list)
	features: list[str] = []
	llm_features_answers = infer_with_features(data_frame=data_frame, features=features)
	df_feature_trump_list, df_feature_biden_list = create_df_group(llm_features_answers, data_frame)
	# fonction qui prends llm_answer et llm_features answers
	write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')
	df_trump_list, df_biden_list = create_df_group(ember_answers, data_frame)

	biden_conversation = build_conversation_list(df_biden_list, "Biden")
	trump_conversation = build_conversation_list(df_trump_list, "Trump")

	assert(len(biden_conversation) == len(df_biden_list) == ember_answers.count("Biden"))
	assert(len(trump_conversation) == len(df_trump_list) == ember_answers.count("Trump"))
	print(len(biden_conversation))
	print(len(trump_conversation))
	biden_features, trump_features = get_features_by_contrast(biden_conversation, trump_conversation)
	print(biden_features)
	print(trump_features)

if __name__ == "__main__":
	# Load .env file
	load_dotenv()
	main()
