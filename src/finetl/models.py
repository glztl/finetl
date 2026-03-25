from pydantic import BaseModel, Field, field_validator, ValidationInfo
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
    def validate_min_rows(cls, v: int, info: ValidationInfo) -> int:
        """
        验证: min_rows 的合理性
        规则: 如果 check_integrity=False, min_rows 可以更小, 但必须有警告
        """
        # 获取其他字段的值 
        check_integrity = info.data.get('check_integrity', True)

        # 如果不检查完整性但要求最小行数 > 100, 给出警告
        if not check_integrity and v > 100:
            # Pydantic中抛出 ValueError 会阻止验证通过
            # 选择允许但记录日志
            import warnings
            warnings.warn(
                f"check_integrity=False 但 min_rows={v}, 建议降低 min_rows 或启用完整性检查",
                UserWarning
            )

        # 必须至少为 1
        if v < 1:
            raise ValueError("min_rows 必须至少为1")

        return v
    
    # 验证 method 和 check_integrity 的组合
    @field_validator('method')
    @classmethod
    def validate_method_with_integrity(cls, v, info):
        """
        验证清洗方法与完整性检查的组合是否合理
        """
        check_integrity = info.data.get('check_integrity', True)

        # 如果选择drop方法但数量要求很高
        if v == "drop" and info.data.get("min_rows", "10") > 50:
            import warnings
            warnings.warn(
                f"使用 method='drop' 可能会删除大量数据，导致行数低于 min_rows={info.data.get('min_rows, 10')}",
                UserWarning
            )
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

