import os
from dotenv import load_dotenv
import pandas as pd
from utils.prompt import build_basic_prompt
from utils.parse_csv import parse_csv
from utils.ember_answers import ember_answers
from utils.create_df_group import split_prompt_in_group_label
from utils.request_ember import infer_with_features, request_ember
from utils.write_list_to_file import write_list_to_file
from utils.get_sorted_features_by_inspect import get_top_features
from utils.write_graph import plot_llm_comparison, write_confusion_matrix
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class MessagePair(BaseModel):
    userMsg: Message
    assistantMsg: Message


def merge_answers(biden_llm_answers: list, trump_llm_answers: list) -> list:
    llm_merged_answers: list = []
    for biden_answer, trump_answer in zip(biden_llm_answers, trump_llm_answers):
        if biden_answer == trump_answer:
            llm_merged_answers.append(biden_answer)
        elif biden_answer != "neutral" and trump_answer == "neutral":
            llm_merged_answers.append(biden_answer)
        elif trump_answer != "neutral" and biden_answer == "neutral":
            llm_merged_answers.append(trump_answer)
        elif trump_answer != biden_answer:
            llm_merged_answers.append("neutral")
        else:
            llm_merged_answers.append(biden_answer)
    return llm_merged_answers


def features_coverage_pipeline(
    data_frame: pd.DataFrame,
    llm_answers: list[str],
    biden_features: list[str],
    trump_features: list[str]
):
    llm_features_answers_biden: list[str] = infer_with_features(
        data_frame=data_frame, features=biden_features)
    llm_features_answers_trump: list[str] = infer_with_features(
        data_frame=data_frame, features=trump_features)
    llm_features_answers: list[str] = merge_answers(
        llm_features_answers_biden, llm_features_answers_trump)

    # TODO: no assert in code -> raise error
    if len(llm_features_answers) != len(llm_features_answers_biden) or len(
        llm_features_answers) != len(llm_features_answers_biden):
        raise ValueError("In featufeatures_coverage_pipeline: List must be the same size")
    plot_llm_comparison(
        llm_answers=llm_answers, llm_features_answer=llm_features_answers, filename="exp-00-plot.png")
    write_confusion_matrix(
        llm_answers=llm_answers, llm_features_answers=llm_features_answers, filename="exp-00-confusion-matrix.png")


#TODO: Schema pydantic ?
def build_conversation_list(user_input_list: list, llm_output: str):
    """format a list of input into ember "conversation" format """
    return [
        [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": llm_output}
        ] for user_input in user_input_list
    ]


def read_file(filepath: str):
    with open(filepath, "r") as file:
        content = file.read()
        return content.splitlines()


def main():
    api_key = os.getenv("GOODFIRE_API_KEY")
    data_frame = parse_csv()
    prompt_list = build_basic_prompt(data_frame=data_frame)
    llm_answers = request_ember(prompt_list)
    
    write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')

    biden_prompt_list, trump_prompt_list = split_prompt_in_group_label(llm_answers, prompt_list)
    #write prompt
    print(len(trump_prompt_list))
    print(len(biden_prompt_list))
    biden_conversation = build_conversation_list(biden_prompt_list, "Biden")
    trump_conversation = build_conversation_list(trump_prompt_list, "Trump")

    #TODO: No assert in code -> raise Error
    assert(len(biden_conversation) == len(biden_prompt_list) == ember_answers.count("Biden"))
    assert(len(trump_conversation) == len(trump_prompt_list) == ember_answers.count("Trump"))
    
    #TODO: get a json (easier to process)
    biden_top_features_score, biden_top_features = get_top_features(biden_conversation)
    trump_top_features_score, trump_top_features = get_top_features(trump_conversation)
    #TODO: write in json file
    write_list_to_file(
        biden_top_features_score, "result/biden_top_features_by_inspect_score.txt")
    write_list_to_file(
        biden_top_features, "result/biden_top_features_by_inspect.txt")
    write_list_to_file(
        trump_top_features_score, "result/trump_top_features_by_inspect_score.txt")
    write_list_to_file(
        trump_top_features, "result/trump_top_features_by_inspect.txt")
    
    #TODO: read a json but no need to read in pipeline
    #biden_top_features = read_file("/Users/garancecolomer/akaton_080325/result/biden_top_features_by_inspect_0.txt")
    #trump_top_features = read_file("/Users/garancecolomer/akaton_080325/result/trump_top_features_by_inspect_0.txt")

    sample_to_process: int = 60
    features_to_infer: int = 10
    features_coverage_pipeline(
        data_frame=data_frame,
        llm_answers=llm_answers[:sample_to_process],
        biden_features=biden_top_features[:features_to_infer],
        trump_features=trump_top_features[:features_to_infer]
    )
    #TODO: in feature_coverage_pipeline

if __name__ == "__main__":
	# Load .env file
    load_dotenv()
    main()
