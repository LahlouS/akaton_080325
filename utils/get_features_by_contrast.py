import os
import goodfire
from utils.write_list_to_file import write_list_to_file

# cant load api_key from .env. Idk why.


def equalize_slice_size(list1: list, list2: list):
    """retuns list of the same size"""
    min_lenght = min(len(list1), len(list2))
    return list1[:min_lenght], list2[:min_lenght]


def slice_list_to_matrix(lst: list, size: int):
	return [lst[i:i + size] for i in range(0, len(lst), size)]

def from_features_to_list(features_list: goodfire.FeatureGroup) -> list:
	"""converts FeatureGroup and contact them"""
	return [feat.label for feat in features_list]

# not used anymore (due to ember credit amount)
def batchRequest(lst1: list, lst2: list, chunck_size: int):
	# according to goodfire doc, datasets have to :
	# 	- be lower than 60
	# 	- have same size
	api_key = os.getenv("GOODFIRE_API_KEY")
	client = goodfire.Client(api_key=api_key)
	variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")

	# equalize_slice_size
	if len(lst1) != len(lst2):
		lst1, lst2 = equalize_slice_size(lst1, lst2)
	# create chuncks
	chunk_size = len(lst1)/chunck_size
	full_list1_features: set = []
	full_list2_features: set = []
	lst1 = slice_list_to_matrix(lst1, int(chunk_size))
	lst2 = slice_list_to_matrix(lst2, int(chunk_size))

	# for i in range(len(lst1)):
	# 	print(len(lst1[i]))
	# for i in range(len(lst2)):
	# 	print(len(lst2[i]))
	# batch call ember
	for i in range(len(lst1)):
		for j in range(len(lst2)):
			# ignore slice of different size
			if (len(lst1) != len(lst2)): continue
			# call ember
			feat1, feat2 = client.features.contrast(
				dataset_1=lst1[i],
				dataset_2=lst2[j],
				model=variant,
				top_k=50
			)
			# concat result in list format
			full_list1_features += set(from_features_to_list(feat1))
			full_list2_features += set(from_features_to_list(feat2))
	return full_list1_features, full_list2_features

def get_features_by_contrast_60(lst1: list, lst2: list):
	api_key = os.getenv("GOODFIRE_API_KEY")
	client = goodfire.Client(api_key=api_key)
	variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")
	feat1, feat2 = client.features.contrast(
					dataset_1=lst1[:60],
					dataset_2=lst2[:60],
					model=variant,
					top_k=120
				)
	return set(from_features_to_list(feat1)), set(from_features_to_list(feat2))


def get_features_by_contrast(biden_conversation: list[list[dict[str, str]]], trump_conversation: list[list[dict[str, str]]]):
	# biden_feature_set, trump_feature_set = batchRequest(biden_conversation, trump_conversation, 4)
	biden_feature_set, trump_feature_set = get_features_by_contrast_60(biden_conversation, trump_conversation)
	write_list_to_file(biden_feature_set, './result/biden_feature_contrast_list.txt')
	write_list_to_file(trump_feature_set, './result/trump_feature_contrast_list.txt')
	return biden_feature_set, trump_feature_set

