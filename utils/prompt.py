import pandas as pd

PROMPT_BASIC_INSTRUCTION = """To do this, you must rely on the user's name, their description, their tweet, and their state."""

PROMPT_FEATURES_INSTRUCTION = """To do this, you must rely on these sentences:
{features}
"""

PROMPT_TEMPLATE="""You are a political analyst. Your goal is to determine who the user voted for between Trump and Biden.
{instructions}
Respond only with string "Trump" or "Biden" or "Neutral".
Input example:
{{
    "user_name": "Love the beach love my family",
    "user_description" : "I love America !",
    "tweet": "Sleepy Joe wearing $1,450 blazer...the Scranton kid...lol so it's ok for #Biden but not for #POTUS45",
    "state": "Florida"
}}

Output example:

Trump

Input:
{{
    "user_name": "{user_name}",
    "user_description" : "{user_description}",
    "tweet": "{tweet}",
    "state": "{state}"
}}

Output:

"""

def build_prompt(data_frame: pd.DataFrame, instruction: str):
    """Build prompt"""
    prompt_array: list[str] = []
    for _index, row in data_frame.iterrows():
        prompt_array.append(
            PROMPT_TEMPLATE.format(
                instructions=instruction,
                user_name=row["user_name"],
                user_description=row["user_description"],
                tweet=row["tweet"],
                state=row["state"]
            )
        )
    return prompt_array


def build_basic_prompt(data_frame: pd.DataFrame) -> list[str]:
    """Prompt with basic instruction"""
    return build_prompt(data_frame=data_frame, instruction=PROMPT_BASIC_INSTRUCTION)


def build_features_prompt(data_frame: pd.DataFrame, features: list[str]) -> list[str]:
    """Prompt with top features instructions"""
    instructions: str = ""
    for feature in features:
        instructions += "- " + feature + "\n"
    return build_prompt(
        data_frame=data_frame,
        instruction=PROMPT_FEATURES_INSTRUCTION.format(features=instructions)
    )
