import pandas as pd

def create_df_group(ember_answers: list[str], data_frame: pd.DataFrame):
    """ create group Biden / Trump """
    if (len(ember_answers) != len(data_frame)):
        raise ValueError("ember_answers data_frame not same size")
    df_trump_list: pd.DataFrame = pd.DataFrame()
    df_biden_list: pd.DataFrame = pd.DataFrame()

    for index, row in data_frame.iterrows():
        if ember_answers[index] == 'Biden':
            df_biden_list = pd.concat([df_biden_list, pd.DataFrame([row])], ignore_index=True)
        elif ember_answers[index] == 'Trump':
            df_trump_list = pd.concat([df_trump_list, pd.DataFrame([row])], ignore_index=True)
    return df_trump_list, df_biden_list

def create_list_group_based_on_prompt(ember_answers: list[str], prompt_list: list[str]):
    """ create group Biden / Trump """

    if (len(ember_answers) != len(prompt_list)):
        raise ValueError("HERE ember_answers data_frame not same size")
    biden_list: list = []
    trump_list: list = []
    for index, prompt  in enumerate(prompt_list):
        if ember_answers[index] == 'Biden':
            biden_list.append(prompt)
        elif ember_answers[index] == 'Trump':
            trump_list.append(prompt)
    return biden_list, trump_list
