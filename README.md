# finetl

> 可靠的金融数据 ETL 与清洗工具库

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/finetl.svg)](https://badge.fury.io/py/finetl)
[![CI](https://github.com/glztl/finetl/actions/workflows/ci.yml/badge.svg)](https://github.com/glztl/finetl/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/glztl/finetl/branch/main/graph/badge.svg)](https://codecov.io/gh/glztl/finetl)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 项目简介

**finetl** 是一个专为量化交易和数据分析师设计的金融数据 ETL（Extract-Transform-Load）工具库。

在量化交易中，**脏数据是策略失效的主要原因之一**。`finetl` 通过严格的类型验证、数据完整性检查和自动化清洗流程，确保你的数据在进入策略模型前是**干净、一致、可靠**的。

### 为什么选择 finetl？

| 问题 | 传统方式 | finetl 方案 |
|------|----------|-------------|
| 数据格式不统一 | 手动检查每列 | ✅ 自动 Schema 验证 |
| 脏数据导致策略失效 | 运行时才发现错误 | ✅ 加载时主动报错 |
| 缺失值处理不一致 | 每个项目重复写代码 | ✅ 统一配置化处理 |
| 缺乏类型安全 | 运行时错误 | ✅ Pydantic 静态验证 |

---

## ✨ 核心功能

- 🛡️ **数据完整性验证**：自动检查 `High >= Low`、`Close >= 0` 等金融逻辑
- 🔧 **灵活的清洗策略**：支持 `drop`、`ffill`、`bfill` 等多种缺失值处理方法
- 📐 **类型安全配置**：基于 Pydantic 的配置验证，IDE 自动补全
- 🧪 **高测试覆盖率**：核心逻辑 90%+ 测试覆盖，生产环境可用
- 🚀 **零依赖负担**：仅需 `pandas` 和 `pydantic`，轻量级设计

---

## 🚀 快速开始

### 安装

```bash
# 使用 pip
pip install finetl

# 或使用 uv（推荐）
uv add finetl
```

### 基础使用
```bash
import pandas as pd
from finetl import process_etl, ETLConfig, DataIntegrityError

# 1. 准备数据
df = pd.DataFrame({
    "Open": [100.0, 101.0, 102.0],
    "High": [105.0, 106.0, 107.0],
    "Low": [99.0, 100.0, 101.0],
    "Close": [104.0, 105.0, 106.0],
    "Volume": [1000, 1100, 1200]
})

# 2. 配置 ETL 管道
config = ETLConfig(
    method="ffill",          # 缺失值前向填充
    check_integrity=True,    # 启用金融逻辑检查
    min_rows=10              # 最小数据行数要求
)

# 3. 执行清洗
try:
    clean_df = process_etl(df, config)
    print("✅ 数据清洗成功！")
except DataIntegrityError as e:
    print(f"❌ 数据验证失败：{e}")
```

### 高级用法
```bash
from finetl import StockSchema, check_financial_integrity

# 自定义必需列 Schema
schema = StockSchema(
    required_columns=["Open", "High", "Low", "Close"],
    numeric_columns=["Open", "High", "Low", "Close"]
)

# 单独使用验证功能
check_financial_integrity(df)
```

### 🧪 测试与质量
```bash
# 克隆仓库
git clone https://github.com/glztl/finetl.git
cd finetl

# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 运行测试并查看覆盖率
uv run pytest --cov=src/finetl --cov-report=html
```

### 📁 项目结构
```bash
finetl/
├── src/finetl/
│   ├── __init__.py      # 公共接口导出
│   ├── models.py        # Pydantic 数据模型
│   ├── cleaner.py       # 数据清洗逻辑
│   └── validator.py     # 数据验证逻辑
├── tests/               # 单元测试
├── pyproject.toml       # 项目配置
└── README.md
```


### 开发环境设置
```bash
# 使用 uv 设置开发环境
uv sync --dev

# 运行代码检查
uv run ruff check src/

# 运行测试
uv run pytest
```
### ⚠️ 免责声明
#### 本项目仅用于学习和技术交流，不构成任何投资建议。
金融数据存在延迟和误差，使用本工具处理的数据进行任何交易决策，风险由用户自行承担。