from dotenv import load_dotenv
import pandas as pd
from src.utils.prompt import build_basic_prompt
from src.utils.parse_csv import parse_csv
from src.utils.create_df_group import split_prompt_in_group_label
from src.utils.request_ember import infer_with_features, request_ember
from src.utils.write_list_to_file import write_list_to_file
from src.utils.get_sorted_features_by_inspect import get_top_features
from src.utils.write_graph import plot_llm_comparison, write_confusion_matrix
import json


def merge_answers(
        biden_llm_answers: list[str],
        trump_llm_answers: list[str]
) -> list:
    if len(biden_llm_answers) != len(trump_llm_answers):
        raise ValueError("Merge answer: list must be the same size")
    llm_merged_answers: list = []
    for biden_answer, trump_answer in zip(biden_llm_answers, trump_llm_answers):
        biden_answer = biden_answer.lower()
        trump_answer = trump_answer.lower()
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

    if len(llm_features_answers) != len(llm_features_answers_biden) or len(
            llm_features_answers) != len(llm_features_answers_trump):
        raise ValueError("In features_coverage_pipeline: List must be the same size")
    plot_llm_comparison(
        llm_answers, llm_features_answers, filename="exp-00-plot.png")
    write_confusion_matrix(
        llm_answers, llm_features_answers, filename="exp-00-confusion-matrix.png")


def build_conversation_list(input_list: list, llm_output: str):
    """format a list of input into ember "conversation" format """
    return [
        [
            {"role": "user", "content": input},
            {"role": "assistant", "content": llm_output}
        ] for input in input_list
    ]


def read_file(filepath: str):
    with open(filepath, "r") as file:
        content = file.read()
        return content.splitlines()
    

def build_json(prompt_list: list, llm_answers: list):
    if len(prompt_list) != len(llm_answers):
        raise ValueError("Build json: List must be the same size")
    json_conversation_list: list = []
    for prompt, answer in zip(prompt_list, llm_answers):
        json_conversation_list.append(
            {
                "prompt": prompt,
                "answer": answer
            }
        )


def main():
    data_frame = parse_csv()
    prompt_list = build_basic_prompt(data_frame=data_frame)
    llm_answers = request_ember(prompt_list)

    json_conversations: list = build_json(prompt_list, llm_answers)
    with open("result_inference.json", "w+") as file:
        file.write(json.dumps(json_conversations, indent=4))

    #write_list_to_file(llm_answers, './result/vote_Prediction_llm_answer')

    biden_prompt_list, trump_prompt_list = split_prompt_in_group_label(
        llm_answers, prompt_list)

    biden_conversation = build_conversation_list(biden_prompt_list, "Biden")
    trump_conversation = build_conversation_list(trump_prompt_list, "Trump")

    if len(biden_conversation) != len(biden_prompt_list) or len(
            trump_conversation) != len(trump_prompt_list):
        raise ValueError("Conversation and prompt must be the same size")

    biden_top_features_score, biden_top_features = get_top_features(
        biden_conversation)
    trump_top_features_score, trump_top_features = get_top_features(
        trump_conversation)


    write_list_to_file(
        biden_top_features_score, "result/biden_top_features_by_inspect_score.txt")
    write_list_to_file(
        biden_top_features, "result/biden_top_features_by_inspect.txt")
    write_list_to_file(
        trump_top_features_score, "result/trump_top_features_by_inspect_score.txt")
    write_list_to_file(
        trump_top_features, "result/trump_top_features_by_inspect.txt")
    
    # TODO: read a json but no need to read in pipeline
    # biden_top_features = read_file("/Users/garancecolomer/akaton_080325/result/biden_top_features_by_inspect_0.txt")
    # trump_top_features = read_file("/Users/garancecolomer/akaton_080325/result/trump_top_features_by_inspect_0.txt")

    sample_to_process: int = 60
    features_to_infer: int = 10
    features_coverage_pipeline(
        data_frame=data_frame,
        llm_answers=llm_answers[:sample_to_process],
        biden_features=biden_top_features[:features_to_infer],
        trump_features=trump_top_features[:features_to_infer]
    )


if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    main()
