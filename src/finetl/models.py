from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


class DataIntegrityError(Exception):
    """
    自定义异常: 当数据完整性检查失败时抛出
    """
    pass

class ETLConfig(BaseModel):
    """
    ETL 管道配置模型
    使用 Pydantic 自动验证用户输入的配置是否合法
    """
    # 必填字段: 清洗方法
    method: Literal["drop", "ffill", "bfill"] = Field(
        default="drop",
        description="缺失值处理方法"
    )

    # 必填字段: 是否检查数据完整性
    check_integrity: bool = Field(
        default=True,
        description="是否检查 High >= Low 等金融逻辑"
    )

    # 可选字段: 最小数据行数量
    min_rows: int = Field(
        default=10,
        ge=1,   # 验证: 必须大于等于 1
        description="允许的最小数据行数"
    )

    # 自定义验证器: 如果 check_integrity 为 False, 则 min_rows 必须为 1
    @field_validator('min_rows')
    @classmethod
    def validate_min_rows(cls, v, info):
        if info.data.get("check_integrity") is False and v > 1:
            # 示例逻辑，根据实际需求调整
            pass
        return v

class StockSchema(BaseModel):
    """
    定义标准的股票数据列 schema
    用于验证输入 DataFrame 是否包含必须列
    """
    required_columns: list[str] = Field(
        default=["Open", "High", "Low", "Close", "Volume"],
        description="必需的列名"
    )

    numeric_columns: list[str] = Field(
        default=["Open", "High", "Low", "Close", "Volume"],
        description="必须为数值型的列"
    )