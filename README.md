# 🐎 Horse Racing Engineering Project

A professional-grade data platform following the **Medallion Architecture**, built with **Python**, **dbt Core**, and **DuckDB**. This project serves as a technical showcase for Senior Analytics Engineering standards.

## 🏗 Architecture
The project follows the Medallion data design pattern:
- **Bronze (Raw):** Python ingestion scripts fetching data from APIs (initially PMU) stored as local CSVs.
- **Silver (Staging):** dbt models that clean, cast, and standardize raw data.
- **Gold (Marts):** Business-level aggregations and performance metrics.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- [pyenv](https://github.com/pyenv/pyenv) (recommended for version management)

### 2. Setup Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
