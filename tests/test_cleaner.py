import pandas as pd
import pytest
from src.finetl.cleaner import clean_missing_data, validate_columns


def test_clean_missing_data_drop():
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, 5, 6]})
    print(df)
    cleaned = clean_missing_data(df, method="drop")
    assert len(cleaned) == 2
    assert cleaned.iloc[1]["A"] == 2
    print("====assert===========: ", cleaned.iloc[1]["A"])

def test_clean_missing_data_ffill():
    df = pd.DataFrame({"A": [1, None, 3], "B": [4, 5, 6]})
    cleaned = clean_missing_data(df, method="ffill")
    assert cleaned.iloc[1]["A"] == 1.0  # 向前填充
    print("====assert===========: ", cleaned.iloc[1]["A"])

def test_validate_columns_true():
    df = pd.DataFrame({"Close": [1], "Open": [1]})
    assert validate_columns(df, ["Close", "Open"]) is True

def test_validate_columns_false():
    df = pd.DataFrame({"Close": [1]})
    assert validate_columns(df, ["Close", "Open"]) is False