from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SCENARIO_PATH = PROCESSED_DIR / "simulated_inventory_replenishment_scenario.csv"
FORECAST_PATH = PROCESSED_DIR / "forecast_7day_average_28day.csv"
DEMO_DIR = PROJECT_ROOT / "data" / "demo"
DEMO_SCENARIO_PATH = DEMO_DIR / "simulated_inventory_replenishment_scenario.csv"
DEMO_FORECAST_PATH = DEMO_DIR / "forecast_7day_average_28day.csv"
HAS_M5_OUTPUTS = SCENARIO_PATH.is_file() and FORECAST_PATH.is_file()

st.set_page_config(
    page_title="Demand & Inventory Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 14% 0%, rgba(33, 93, 115, .22), transparent 34%),
            radial-gradient(ellipse at 100% 20%, rgba(56, 71, 125, .17), transparent 30%),
            #090d13;
        color: #e8eef7;
    }
    [data-testid="stHeader"] { background: rgba(9, 13, 19, .72); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101722 0%, #0c1119 100%);
        border-right: 1px solid #202b39;
    }
    [data-testid="stSidebar"] * { color: #dce5f0; }
    .block-container { max-width: 1500px; padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #f1f5fb !important; letter-spacing: -0.025em; }
    p, label, [data-testid="stCaptionContainer"] { color: #aab8c9; }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.7rem 2rem 1.55rem;
        margin-bottom: 1.4rem;
        border: 1px solid #263446;
        border-radius: 20px;
        background: linear-gradient(115deg, rgba(20, 32, 45, .96), rgba(16, 22, 34, .92));
        box-shadow: 0 18px 55px rgba(0, 0, 0, .24);
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -55px;
        top: -155px;
        border-radius: 50%;
        background: rgba(63, 207, 173, .11);
        filter: blur(35px);
    }
    .hero-kicker, .section-kicker {
        color: #66d9bd;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }
    .hero h1 {
        position: relative;
        z-index: 1;
        margin: .55rem 0 .3rem;
        font-size: clamp(1.8rem, 3vw, 2.55rem);
        font-weight: 720;
    }
    .hero-copy { position: relative; z-index: 1; margin: 0; color: #aab8c9; }
    .status-row { position: relative; z-index: 1; display: flex; gap: .6rem; align-items: center; margin-top: 1.1rem; }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .36rem .68rem;
        border: 1px solid rgba(102, 217, 189, .28);
        border-radius: 999px;
        background: rgba(37, 133, 112, .13);
        color: #9ce8d5;
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .08em;
    }
    .status-dot { width: .42rem; height: .42rem; border-radius: 50%; background: #66d9bd; box-shadow: 0 0 12px rgba(102, 217, 189, .75); }
    [data-testid="stMetric"] {
        min-height: 118px;
        padding: 1.05rem 1.15rem;
        border: 1px solid #263446;
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(21, 31, 44, .97), rgba(15, 21, 31, .97));
        box-shadow: 0 8px 24px rgba(0, 0, 0, .16);
    }
    [data-testid="stMetricLabel"] { color: #9eafc2 !important; font-size: .78rem; }
    [data-testid="stMetricValue"] { color: #eef5fb !important; font-weight: 700; }
    [data-testid="stMetricDelta"] { color: #72dfc3 !important; }
    .section-kicker { margin: 1.6rem 0 .65rem; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #263446 !important;
        border-radius: 16px !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #263446;
        border-radius: 14px;
        overflow: hidden;
    }
    div[data-testid="stDownloadButton"] button {
        border: 1px solid #3e927f;
        border-radius: 10px;
        background: rgba(38, 119, 101, .18);
        color: #c9f4e9;
        font-weight: 650;
    }
    div[data-testid="stDownloadButton"] button:hover {
        border-color: #66d9bd;
        background: rgba(38, 119, 101, .32);
        color: #ffffff;
    }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stTextInput"] > div > div {
        border-color: #334356;
        border-radius: 10px;
        background: #121b27;
    }
    hr { border-color: #263446; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading forecast and scenario data…")
def load_data():
    if HAS_M5_OUTPUTS:
        scenario_path, forecast_path = SCENARIO_PATH, FORECAST_PATH
    elif DEMO_SCENARIO_PATH.is_file() and DEMO_FORECAST_PATH.is_file():
        scenario_path, forecast_path = DEMO_SCENARIO_PATH, DEMO_FORECAST_PATH
    else:
        raise FileNotFoundError(
            "No dashboard data found. Add the two generated CSV files under "
            "data/processed/, or restore the synthetic files under data/demo/."
        )
    scenario = pd.read_csv(scenario_path)
    forecast = pd.read_csv(forecast_path)
    return scenario, forecast


st.markdown(
    f"""
    <section class="hero">
      <div class="hero-kicker">Retail analytics · planning workspace</div>
      <h1>Demand &amp; Inventory Intelligence</h1>
      <p class="hero-copy">28-day demand outlook · product and store performance · replenishment planning</p>
      <div class="status-row">
        <span class="status-pill"><span class="status-dot"></span> {'HISTORICAL M5 FORECAST' if HAS_M5_OUTPUTS else 'SYNTHETIC DEMO FORECAST'}</span>
        <span class="status-pill">SIMULATED INVENTORY INPUTS</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

try:
    inventory, forecast = load_data()
except Exception as exc:
    st.error(f"Could not load dashboard data: {exc}")
    st.stop()

if not HAS_M5_OUTPUTS:
    st.info(
        "This copy is using fictional synthetic demo data. It does not contain "
        "M5/Walmart sales, actual stock records, or live store connections."
    )

required_inventory = {
    "id",
    "item_id",
    "cat_id",
    "store_id",
    "forecast_28day_total",
    "simulated_on_hand_units",
    "simulated_on_order_units",
    "reorder_point_units_rounded",
    "simulated_inventory_position_units",
    "simulated_reorder_now",
    "simulated_order_quantity_units",
}
required_forecast = {"id", "forecast_28day_total"}
missing_inventory_columns = sorted(required_inventory - set(inventory.columns))
missing_forecast_columns = sorted(required_forecast - set(forecast.columns))
if missing_inventory_columns or missing_forecast_columns:
    details = []
    if missing_inventory_columns:
        details.append("scenario CSV missing: " + ", ".join(missing_inventory_columns))
    if missing_forecast_columns:
        details.append("forecast CSV missing: " + ", ".join(missing_forecast_columns))
    st.error("The CSV files do not have the expected columns. " + "; ".join(details))
    st.stop()

st.sidebar.markdown("## Explore the data")
st.sidebar.caption("Filter the forecast and simulated replenishment scenario.")
store_options = ["All stores"] + sorted(inventory["store_id"].dropna().astype(str).unique())
category_options = ["All categories"] + sorted(inventory["cat_id"].dropna().astype(str).unique())
selected_store = st.sidebar.selectbox("Store", store_options)
selected_category = st.sidebar.selectbox("Category", category_options)
item_search = st.sidebar.text_input("Search item ID")
only_reorder = st.sidebar.checkbox("Show reorder-flagged items only", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Saved CSV inputs · no live store connection")

filtered = inventory.copy()
if selected_store != "All stores":
    filtered = filtered[filtered["store_id"].astype(str) == selected_store]
if selected_category != "All categories":
    filtered = filtered[filtered["cat_id"].astype(str) == selected_category]
if item_search.strip():
    filtered = filtered[
        filtered["item_id"].astype(str).str.contains(item_search.strip(), case=False, na=False)
    ]
if only_reorder:
    filtered = filtered[filtered["simulated_reorder_now"].astype(bool)]

if filtered.empty:
    st.info("No product–store series match the selected filters.")
    st.stop()

st.markdown('<div class="section-kicker">Scenario overview</div>', unsafe_allow_html=True)
metric_columns = st.columns(4)
flagged_count = int(filtered["simulated_reorder_now"].astype(bool).sum())
with metric_columns[0]:
    st.metric("Product–store series", f"{len(filtered):,}")
with metric_columns[1]:
    st.metric("28-day forecast units", f"{filtered['forecast_28day_total'].sum():,.0f}")
with metric_columns[2]:
    st.metric("Flagged in scenario", f"{flagged_count:,}")
with metric_columns[3]:
    st.metric("Simulated order units", f"{filtered['simulated_order_quantity_units'].sum():,.0f}")

st.markdown('<div class="section-kicker">Demand outlook &amp; replenishment signals</div>', unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.subheader("Daily forecast for selected series")
    selected_ids = set(filtered["id"].astype(str))
    forecast_subset = forecast[forecast["id"].astype(str).isin(selected_ids)]
    day_columns = [
        column
        for column in forecast.columns
        if column.startswith("d_") and column[2:].isdigit()
    ]
    if forecast_subset.empty or not day_columns:
        st.info("No daily forecast columns were found for this selection.")
    else:
        daily_totals = forecast_subset[day_columns].sum(axis=0)
        daily_chart = pd.DataFrame(
            {"Forecast units": daily_totals.to_numpy()},
            index=daily_totals.index,
        )
        daily_chart.index.name = "Forecast day"
        st.line_chart(daily_chart)

with right:
    st.subheader("Simulated order units by store")
    store_chart = (
        filtered.groupby("store_id")["simulated_order_quantity_units"]
        .sum()
        .sort_values()
        .to_frame(name="Simulated order units")
    )
    st.bar_chart(store_chart)

st.markdown('<div class="section-kicker">Product-level planning queue</div>', unsafe_allow_html=True)
st.caption(
    "A reorder flag means simulated inventory position is at or below the rounded "
    "reorder point. Order quantities follow the scenario assumptions in the notebook."
)
display_columns = [
    "id",
    "item_id",
    "cat_id",
    "store_id",
    "forecast_28day_total",
    "simulated_on_hand_units",
    "simulated_on_order_units",
    "reorder_point_units_rounded",
    "simulated_inventory_position_units",
    "simulated_reorder_now",
    "simulated_order_quantity_units",
]
visible_table = filtered.sort_values(
    "simulated_order_quantity_units", ascending=False
)[display_columns]
st.dataframe(visible_table, width="stretch", hide_index=True)

st.download_button(
    "Download filtered scenario as CSV",
    data=visible_table.to_csv(index=False).encode("utf-8"),
    file_name="filtered_inventory_demo.csv",
    mime="text/csv",
)

st.divider()
st.caption(
    "Planning demonstration · historical M5 demand · simulated stock and supply inputs · "
    "not connected to live inventory systems"
)
