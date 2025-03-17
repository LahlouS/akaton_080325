import pytest
import pandas as pd
from src.main import merge_answers, features_coverage_pipeline
from unittest.mock import patch, MagicMock


@pytest.mark.parametrize(
        "list_1, list_2, expected",
        [
            (["Biden", "Trump", "Neutral"], ["Biden", "Biden", "Biden"], ["biden", "neutral", "biden"]),
            (["Trump", "Neutral", "Neutral"], ["Biden", "Neutral", "Trump"], ["neutral", "neutral", "trump"]),
            (["Trump", "Biden", "Neutral"], ["Trump", "Biden", "Trump"], ["trump", "biden", "trump"])
        ]
)
def test_merge_answer(list_1: list, list_2: list, expected: list):
    assert merge_answers(list_1, list_2) == expected


def test_merge_answer_len():
    list_1 = ["mock", "mock"]
    list_2 = ["mock"]

    with pytest.raises(ValueError):
        merge_answers(list_1, list_2)


@patch("src.main.infer_with_features", return_value=["mock"])
@patch("src.main.merge_answers", return_value=["mock", "mock"])
@patch("src.main.plot_llm_comparison")
@patch("src.main.write_confusion_matrix")
def test_features_coverage_pipeline(
    mock_confusion_matrix,
    mock_plot_comparison,
    mock_merge,
    mock_infer
):
    mock_dataframe = MagicMock(spec=pd.DataFrame)
    with pytest.raises(ValueError):
        features_coverage_pipeline(
            mock_dataframe,
            ["mock"],
            ["mock"],
            ["mock"]
        )
    mock_plot_comparison.assert_not_called()
    mock_confusion_matrix.assert_not_called()
