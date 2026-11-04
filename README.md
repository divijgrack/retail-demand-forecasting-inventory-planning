# Retail Demand Forecasting and Inventory Planning

A forecasting and inventory-planning demo built with the M5 Forecasting Accuracy dataset. It compares simple demand baselines with machine-learning experiments, then uses a 28-day forecast to illustrate reorder planning.

> **Data note:** The M5 dataset provides historical sales, calendar, and price information. It does not provide the current stock, supplier lead times, or inbound orders needed for live replenishment. The inventory values in this project are simulated.

## Project contents

Run the notebooks in this order:

1. code/notebooks/01_data_check.ipynb — inspect M5 data and compare simple forecasting baselines.
2. code/notebooks/02_ml_forecasting.ipynb — test machine-learning models and additional features.
3. code/notebooks/03_final_evaluation.ipynb — compare forecasting methods across all 30,490 product-store series.
4. code/notebooks/04_inventory_planning.ipynb — create a 28-day forecast and demonstrate an inventory scenario.

The notebooks locate the project root automatically, so the project can be moved to another folder.

## Forecast evaluation

The 7-day average was selected for the inventory-planning demonstration because it is simple and inexpensive to compute. Its mean absolute error (MAE) across all 30,490 series was:

| Test window | 7-day average MAE |
|---|---:|
| Window 1 | 1.048760 |
| Window 2 | 1.046485 |
| Latest window | 1.062837 |

CatBoost was also evaluated. Results varied by test window: CatBoost did better in the latest window, while the 7-day average did better in the first two. These experiments do not establish that one method wins in every period.

## Inventory-planning demonstration

The M5 data has no actual stock or supplier records, so the notebook creates a simulated scenario using:

- Generated starting stock, set to 0–14 days of forecast demand per series with a fixed random seed
- No incoming orders
- A 7-day assumed supplier lead time
- A 95% assumed service level

In this scenario, 27,578 of 30,490 series (90.4%) were flagged for reorder. CA_3 had the largest simulated total order quantity (143,073 units), and CA_4 had the smallest (75,143 units). These are illustrative outputs under the stated assumptions; they are not Walmart stock levels or real purchase recommendations.

## Dashboard

The Streamlit dashboard includes store, category, and item filters, forecast charts, a simulated reorder view, and CSV download.

- On the development machine, if both required files exist in data/processed/, the app uses those local M5-derived forecast and simulated-inventory results.
- On a fresh clone, the app falls back to the small fictional synthetic CSV fixtures in data/demo/. Those fixtures contain no M5/Walmart rows and make the dashboard viewable without the competition data.

Start the dashboard after installing dependencies:

    .venv/bin/streamlit run src/app.py

The project-specific run_dashboard.sh launcher can also be used after setting up .venv.

## Setup

Use Python 3.10 or newer.

Create an environment and install the notebook dependencies:

    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt

Open the project folder in VS Code, select the .venv Python kernel, then run notebooks in the order above.

### M5 data

The public repository intentionally excludes raw M5 files and the full M5-derived CSV outputs. To reproduce the notebook analysis:

1. Download the required files directly from the M5 dataset page on Kaggle:
   https://www.kaggle.com/competitions/m5-forecasting-accuracy/data
2. Place sales_train_validation.csv, calendar.csv, and sell_prices.csv in data/raw/m5-forecasting-accuracy/.
3. Run notebooks 01–04 in order.

Review Kaggle's current data terms before redistributing any dataset files or derived exports. The Git ignore rules exclude data/raw/ and data/processed/; the synthetic data/demo/ fixtures remain available.

## Dashboard-only setup

Install just the dashboard dependencies if you do not need the notebooks:

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements-dashboard.txt
    .venv/bin/python -m streamlit run src/app.py

The personal desktop shortcut is not included in the public repository.
