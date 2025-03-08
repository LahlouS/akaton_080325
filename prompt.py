import pandas as pd
from dotenv import load_dotenv


PROMPT_TEMPLATE="""You are a political analyst. Your goal is to determine who the user voted for between Trump and Biden.
To do this, you must rely on the user's name, their description, their tweet, and their state.
Respond only with string "Trump" or "Biden".
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

def build_prompt(data_frame: pd.DataFrame) -> list[str]:
    prompt_array: list[str] = []
    for _index, row in data_frame.iterrows():
        prompt_array.append(
            PROMPT_TEMPLATE.format(
                user_name=row["user_name"],
                user_description=row["user_description"],
                tweet=row["tweet"],
                state=row["state"]
            )
        )
    return prompt_array
