import pandas as pd

def parse_csv() -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame filtré.
    :return: DataFrame filtré
    """
    return pd.read_csv(
        "", encoding='utf-8', sep=','
    )["user_name", "user_description", "tweet", "state", "vote_prediction"]
