import pandas as pd
import os

def parse_csv() -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame filtré.
    :return: DataFrame filtré
    """
    file_path = os.getenv("CSV_FILE_PATH")
    return pd.read_csv(
        file_path, encoding='utf-8', sep=','
    )[["user_name", "user_description", "tweet", "state", "vote_prediction"]]
