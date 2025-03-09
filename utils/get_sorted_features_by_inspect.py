import os
import goodfire
from utils.write_list_to_file import write_list_to_file

def compute_feature_mean_scores(feature_map):
    feature_scores = {}
    mean_len = 0
    i = 0
    for feature, activations in feature_map.items():
        i += 1
        mean_len += len(feature)
    mean_len /= i
    for feature, activations in feature_map.items():
        if not activations:
            feature_scores[feature] = 0
            continue
        n = len(activations)
        _mean = sum(activations) / n
        score = _mean * (n / mean_len)
        feature_scores[feature] = score
    return feature_scores

# def compute_feature_scores(feature_map, lambda_variance=0.3):
#     """
#     Calcule un score pour chaque feature en fonction de l'activation.

#     feature_map: dict[str, list[int]] - Dictionnaire feature -> liste des activations.
#     lambda_variance: float - Poids donné à la variance dans le score.

#     Retourne: dict[str, float] - Dictionnaire feature -> score.
#     """
#     feature_scores = {}

#     for feature, activations in feature_map.items():
#         if not activations:
#             feature_scores[feature] = 0
#             continue

#         n = len(activations)
#         mean_activation = sum(activations) / n
#         variance_activation = sum((x - mean_activation) ** 2 for x in activations) / n

#         # Score combiné : Moyenne + lambda * Variance
#         score = mean_activation + lambda_variance * variance_activation
#         feature_scores[feature] = score

#     return feature_scores


def get_feature_activation(conversation: list, client, variant):
	context = client.features.inspect(
		messages=conversation,
		model=variant,
	)
	context.top(k=10)
	return context.top(k=10)


def get_features_by_inspect(conversations: list):
	api_key = os.getenv("GOODFIRE_API_KEY")
	client = goodfire.Client(api_key=api_key)
	variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")

	features_map: dict = {}

	#call ember
	for conversation in conversations:
		feat_activation = get_feature_activation(conversation, client, variant)
		for feat in feat_activation:
			if feat.feature.label in features_map:
				features_map[feat.feature.label].append(feat.activation)
			else:
				features_map[feat.feature.label] = [feat.activation]
	return features_map

def get_sorted_features_by_inspect(conversation: list[list[dict[str, str]]]):
	features_map = get_features_by_inspect(conversation)
	scored_features_map = compute_feature_scores(features_map)
	sorted_scored_features = sorted(scored_features_map.items(), key=lambda x: x[1], reverse=True)

	sorted_texts = [item[0] for item in sorted_scored_features]
	string_features_with_score = [str(feature) for feature in sorted_scored_features]

	return string_features_with_score , sorted_texts

