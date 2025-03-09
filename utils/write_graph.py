import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_llm_comparison(llm_answers, llm_features_answer, filename):
    # Création du dossier de sauvegarde s'il n'existe pas
    save_path = "save/graphic"
    os.makedirs(save_path, exist_ok=True)

    # Définition des catégories et de leur position sur l'axe y
    categories = {"Trump": 0, "Neutral": 1, "Biden": 2}

    # Conversion des réponses en coordonnées numériques
    x_values = np.arange(len(llm_answers))
    y_values_answers = np.array([categories[answer] for answer in llm_answers])
    y_values_features = np.array([categories[answer] for answer in llm_features_answer])

    # Détection des superpositions
    overlap = y_values_answers == y_values_features

    # Création du graphique
    plt.figure(figsize=(8, 5))

    # Affichage des points
    plt.scatter(x_values[~overlap], y_values_answers[~overlap], color='blue', label='LLM Answers')
    plt.scatter(x_values[~overlap], y_values_features[~overlap], color='yellow', label='LLM Features Answer')
    plt.scatter(x_values[overlap], y_values_answers[overlap], color='green', label='Overlap', marker='o')

    # Configuration de l'axe y
    plt.yticks(list(categories.values()), list(categories.keys()))
    plt.xlabel("Index")
    plt.ylabel("Categories")
    plt.title("Comparison of neuronal pathway")
    plt.legend()

    # Sauvegarde et affichage
    filepath = os.path.join(save_path, filename)
    plt.savefig(filepath)
    plt.close()
    print(f"Graphique sauvegardé dans {filepath}")

def write_confusion_matrix(llm_answers: list[str], llm_features_answers: list[str], filename: str):
    save_path = os.path.join(
        os.getenv("HOME"), os.getenv("SAVE_PATH"), "confusion_matrix", filename)

    labels = ["Trump", "Neutral", "Biden"]
    cm = confusion_matrix(llm_answers, llm_features_answers, labels=labels)
    cm_percentage = cm.astype('float') / cm.sum() * 100

    # Affichage avec seaborn
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm_percentage, annot=True, fmt=".2f", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("LLM features-based prediction")
    plt.ylabel("LLM tweet-based prediction")
    plt.title("Neural Pathway Coverage")
    plt.show()
    plt.savefig(save_path)
    plt.close()

