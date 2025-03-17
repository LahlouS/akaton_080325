import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_llm_comparison(llm_answers, llm_features_answer, filename):
    # Création du dossier de sauvegarde s'il n'existe pas
    save_path = os.path.join(
        os.getenv("HOME"), os.getenv("SAVE_PATH"), "graphic", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # Définition des catégories et de leur position sur l'axe y
    categories = {"trump": 0, "neutral": 1, "biden": 2}

    llm_answers = [answer.lower().strip() for answer in llm_answers]
    llm_features_answer = [answer.lower().strip() for answer in llm_features_answer]

    if len(llm_answers) != len(llm_features_answer):
        raise ValueError("Les deux listes doivent avoir la même longueur")

    if not all(answer in categories for answer in llm_answers + llm_features_answer):
        raise ValueError("Toutes les réponses doivent être 'Trump', 'Neutral' ou 'Biden'")


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
    plt.savefig(save_path)
    plt.close()
    print(f"Graphique sauvegardé dans {save_path}")


def write_confusion_matrix(llm_answers: list[str], llm_features_answers: list[str], filename: str):
    save_path = os.path.join(
        os.getenv("HOME"), os.getenv("SAVE_PATH"), "confusion_matrix", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

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
    plt.savefig(save_path)
    plt.show()
    plt.close()

