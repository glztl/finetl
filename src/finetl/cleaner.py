import pandas as pd
from typing import Optional

def clean_missing_data(df: pd.DataFrame, method: str = "drop") -> pd.DataFrame:
    """
    清晰数据中的缺失值

    Args:
        df: 输入的 DataFrame
        method: 'drop' (删除), 'ffill' (前向填充), 'bfill' (后向填充)

    Returns:
        清洗后的 DataFrame
    """
    if df.empty:
        return df
    
    if method == "drop":
        return df.dropna()
    elif method == "ffill":
        return df.ffill()
    elif method == "bfill":
        return df.bfill()
    else:
        raise ValueError(f"Unsupported method: {method}")
    
def validate_columns(df: pd.DataFrame, required_cols: list[str]) -> bool:
    """
    验证 DataFrame 是否包含必需的列
    """
    return all(col in df.columns for col in required_cols)