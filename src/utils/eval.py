def accuracy(features_answers: list[str], llm_answers: list[str]):
    if len(features_answers) != len(llm_answers):
        raise ValueError("list must be the same size")
    positif: int = 0
    negatif: int = 0
    neutral: int = 0
    features_answers = [answer.lower().strip() for answer in features_answers]
    llm_answers = [answer.lower().strip() for answer in llm_answers]

    for ft_answer, llm_answer in zip(features_answers, llm_answers):
        if ft_answer == llm_answer:
            positif += 1
        elif ft_answer == "neutral":
            neutral += 1
        else:
            negatif += 1
    return 100 * positif / len(features_answers)
