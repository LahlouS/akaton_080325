import os
import sys
import goodfire
import pandas as pd

GOODFIRE_API_KEY = os.getenv("GOODFIRE_API_KEY", default = None)
if GOODFIRE_API_KEY is None:
    sys.exit("Please provide the GOODFIRE_API_KEY")


client = goodfire.Client(api_key=GOODFIRE_API_KEY)
variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")

dataset = "manchunhui/us-election-2020-tweets"
dataset_directory = "dataset"
files_name = {
    "trump": "hashtag_donaldtrump.csv",
    "biden": "hashtag_joebiden.csv"
}

files = [f"{dataset_directory}/{name}" for name in files_name.values()]
is_files = [os.path.isfile(file) for file in files]

if not all(is_files):
    import kaggle as kg
    kg.api.authenticate()
    kg.api.dataset_download_files(dataset= dataset, path='dataset', unzip=True)

data_frames = {
    k: pd.read_csv(f"{dataset_directory}/{v}", lineterminator='\n')
    for k, v in files_name.items()
}

# print("First 5 records:", data_frames["trump"].head())
print("First 5 records:", data_frames["trump"].columns)

sys.exit()