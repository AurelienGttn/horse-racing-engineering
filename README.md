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
```

### 3. Data Ingestion
Generate current race data from the PMU API:

```bash
python scripts/generate_mock_data.py
```

### 4. Transformation & Testing
```bash
cd horse_racing_dbt

# Build models and run data quality tests
dbt run
dbt test
```

## 🛡 Quality & Automation
* **Data Testing:** Includes Generic (Unique, Not Null) and Singular (Business Logic) tests.

* **CI/CD:** GitHub Actions automatically runs the ingestion, build, and test suite on every Push/PR.

* **Documentation:** View the lineage and data dictionary by running dbt docs serve.
