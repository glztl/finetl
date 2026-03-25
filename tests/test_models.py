import pytest
import warnings
from src.finetl.models import ETLConfig

def test_case_1_normal():
    """情况 1: check_integrity=True, v=10 → 正常"""
    config = ETLConfig(check_integrity=True, min_rows=10)
    assert config.min_rows == 10

def test_case_2_normal():
    """情况 2: check_integrity=False, v=10 → 正常"""
    config = ETLConfig(check_integrity=False, min_rows=10)
    assert config.min_rows == 10

def test_case_3_normal():
    """情况 3: check_integrity=True, v=150 → 正常"""
    config = ETLConfig(check_integrity=True, min_rows=150)
    assert config.min_rows == 150

def test_case_4_warning():
    """情况 4: check_integrity=False, v=150 → 警告"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ETLConfig(check_integrity=False, min_rows=150)
        assert len(w) >= 1
        assert "建议降低 min_rows" in str(w[0].message)

def test_case_5_error():
    """情况 5: v=0 → 异常 (Pydantic 内置验证)"""
    with pytest.raises(Exception):  # ValidationError
        ETLConfig(min_rows=0)

def test_case_6_error():
    """情况 6: v=-5 → 异常 (Pydantic 内置验证)"""
    with pytest.raises(Exception):  # ValidationError
        ETLConfig(min_rows=-5)

def test_etl_config_default():
    """测试默认配置"""
    config = ETLConfig()
    assert config.method == "drop"
    assert config.check_integrity is True
    assert config.min_rows == 10

def test_etl_config_custom():
    """测试自定义配置"""
    config = ETLConfig(method="ffill", check_integrity=False, min_rows=5)
    assert config.method == "ffill"
    assert config.check_integrity is False
    assert config.min_rows == 5


def test_etl_config_min_rows_too_low():
    """测试 min_rows 太小"""
    with pytest.raises(Exception):
        ETLConfig(min_rows=0)

def test_etl_config_warning_on_large_min_rows():
    """测试大 min_rows 时的警告"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ETLConfig(check_integrity=False, min_rows=150)
        # 检查是否有警告
        assert len(w) >= 1
        assert "建议降低 min_rows" in str(w[0].message)