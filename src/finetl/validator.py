import pandas as pd
from .models import ETLConfig, StockSchema, DataIntegrityError


def validate_dataframe_schema(df: pd.DataFrame, schema: StockSchema) -> bool:
    """
    验证 DataFrame 是否包含必需的列
    """
    missing_cols = [col for col in schema.required_columns if col not in df.columns]
    if missing_cols:
        raise DataIntegrityError(f"数据缺少必需列: {missing_cols}")
    return True

def check_financial_integrity(df: pd.DataFrame) -> pd.DataFrame:
    """
    检查金融数据逻辑完整性
    1. High >= Low
    2. Close >= 0
    3. Volume >= 0
    """
    errors = []

    # 检查 High >= Low
    if 'High' in df.columns and 'Low' in df.columns:
        invalid_hl = df[df['High'] < df['Low']]
        if not invalid_hl.empty:
            errors.append(f"发现 {len(invalid_hl)} 行数据 High < Low")

    # 检查 Close >= 0
    if 'Close' in df.columns:
        invalid_close = df[df['Close'] < 0]
        if not invalid_close.empty:
            errors.append(f"发现 {len(invalid_close)} 行数据 Close < 0")

    # 检查 Volume > 0 (成交量)
    if 'Volume' in df.columns:
        invalid_vol = df[df['Volume'] < 0]
        if not invalid_vol.empty:
            errors.append(f"发现 {len(invalid_vol)} 行数据 Volume < 0")
            
    if errors:
        raise DataIntegrityError("数据完整性检查失败:\n" + "\n".join(errors))
    
    return df


def process_etl(df: pd.DataFrame, config: ETLConfig) -> pd.DataFrame:
    """
    ETL 主入口: 整合配置验证、schema验证、数据清洗、完整性检查
    """
    # 1. 验证配置 (Pydantic 自动完成)
    # 如果传入字典, 自动解析并验证
    if isinstance(config, dict):
        config = ETLConfig(**config)

    # 2. 验证 Schema
    schema = StockSchema()
    validate_dataframe_schema(df, schema)

    # 3. 检查最小行数
    if len(df) < config.min_rows:
        raise DataIntegrityError(f"数据行数 ({len(df)}) 小于最小要求 ({config.min_rows})")
    
    # 4. 数据清洗 (调用里程碑 1 的逻辑)
    from .cleaner import clean_missing_data
    df_clean = clean_missing_data(df, method=config.method)

    # 5. 金融完整性检查
    if config.check_integrity:
        check_financial_integrity(df_clean)

    return df_clean