from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import goodfire

load_dotenv('.env')
save_path = os.getenv("")
api_key = os.getenv("GOODFIRE_API_KEY")

def rerank(feat1, feat2, query="emotional"):
	client = goodfire.Client(api_key)
	variant = goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct")
	
	refeat1 = client.features.rerank(
		features=feat1,
		query=query,
		model=variant,
		top_k=50
	)

	refeat2 = client.features.rerank(
		features=feat2,
		query=query,
		model=variant,
		top_k=50
	)
	return refeat1, refeat2


def remove_common_words(str1, str2):
	# Convert strings to sets of words
	words1 = set(str1.split())
	words2 = set(str2.split())

	# Remove common words
	unique1 = words1 - words2
	unique2 = words2 - words1

	# Return as strings
	return " ".join(unique1), " ".join(unique2)

def generate_wordcloud(text, color="black"):
	wordcloud = WordCloud(
		width=800, 
		height=400, 
		background_color="white",  # White background
		color_func=lambda *args, **kwargs: color,  # All words in red
	).generate(text)

	plt.figure(figsize=(10, 5))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.savefig(save_path + "cloud_word.plt")
