import pandas as pd
import pytest
from src.finetl.validator import process_etl, check_financial_integrity
from src.finetl.models import ETLConfig, DataIntegrityError


def test_process_etl_success():
    df = pd.DataFrame({
        "Open": [100.0], "High": [105.0], "Low": [99.0],
        "Close": [104.0], "Volume": [1000]
    })
    config = ETLConfig(method="drop", min_rows=1)
    result = process_etl(df, config)
    assert len(result) == 1

def test_process_etl_integrity_fail():
    # High < Low 的情况
    df = pd.DataFrame({
        "Open": [100.0], "High": [99.0], "Low": [105.0],
        "Close": [104.0], "Volume": [1000]
    })
    config = ETLConfig(method="drop", min_rows=1)
    with pytest.raises(DataIntegrityError):
        process_etl(df, config)

def test_process_etl_config_validation():
    # 传入错误的 method
    with pytest.raises(Exception):  # Pydantic 会抛出 ValidationError
        ETLConfig(method="invalid_method") # type: ignore[arg-type]