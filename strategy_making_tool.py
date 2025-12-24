import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Market Entry Strategy Dashboard", layout="wide")
st.title("🚕 Market Entry Strategy Using Game Theory")
st.caption("NYC Taxi Data • Product Management • Game Theory")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
def load_data():
    try:
        # Try local file first (works if you've run `git lfs pull` locally)
        df = pd.read_csv("output_file.csv", low_memory=False)
        return df
    except FileNotFoundError:
        # Fallback to external hosted dataset (Google Drive direct download link)
        url = "https://drive.google.com/uc?id=1Ni2A8i8VI9IsCzLGoXuI-YtAYJAe7qfS"
        df = pd.read_csv(url, low_memory=False)
        return df

df = load_data()



# --------------------------------------------------
# MARKET REALITY (STATIC)
# --------------------------------------------------
hourly_demand = df.groupby("hour").size()
hourly_fare = df.groupby("hour")["fare_amount"].mean()
avg_market_fare = df["fare_amount"].mean()
base_demand = hourly_demand.mean()

# --------------------------------------------------
# MODELS
# --------------------------------------------------
def demand_capture(discount, base_demand):
    elasticity = 0.04
    return base_demand * (1 + elasticity * discount)

def profit_model(price, demand, subsidy):
    return (price * demand) - (subsidy * demand)

# --------------------------------------------------
# SIDEBAR — DECISION LEVERS (PRODUCT CONTROLS)
# --------------------------------------------------
st.sidebar.header("🎛 Product Decisions (Platform B)")

discount = st.sidebar.slider("Introductory Discount (%)", 0, 30, 15)
subsidy = st.sidebar.slider("Subsidy per Ride ($)", 0.0, 5.0, 2.0)
entry_hour = st.sidebar.selectbox("Entry Hour", hourly_demand.index)

# --------------------------------------------------
# COMPUTATIONS
# --------------------------------------------------
entry_price = avg_market_fare * (1 - discount / 100)
captured_demand = demand_capture(discount, hourly_demand[entry_hour])
profit = profit_model(entry_price, captured_demand, subsidy)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Market Reality",
    "🚀 Entry Strategy",
    "🎮 Game Theory",
    "🧭 Product Roadmap"
])

# --------------------------------------------------
# TAB 1 — MARKET REALITY
# --------------------------------------------------
with tab1:
    st.subheader("Market Demand (Platform A)")

    fig, ax = plt.subplots()
    hourly_demand.plot(kind="bar", ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Trips")
    st.pyplot(fig)

    st.subheader("Pricing Benchmark (Platform A)")

    fig, ax = plt.subplots()
    hourly_fare.plot(ax=ax)
    ax.set_ylabel("Average Fare ($)")
    st.pyplot(fig)

    st.info(
        "This data represents the **existing platform (Platform A)**. "
        "It is historical and does NOT change with your decisions."
    )

# --------------------------------------------------
# TAB 2 — ENTRY STRATEGY
# --------------------------------------------------
with tab2:
    st.subheader("Platform B Entry Simulation")

    col1, col2, col3 = st.columns(3)

    col1.metric("Entry Price ($)", f"{entry_price:.2f}")
    col2.metric("Captured Demand (Trips)", int(captured_demand))
    col3.metric("Expected Profit ($)", f"{profit:,.0f}")

    st.markdown("### Profit vs Discount Curve")

    discounts = range(0, 31)
    profits = [
        profit_model(
            avg_market_fare * (1 - d/100),
            demand_capture(d, base_demand),
            subsidy
        )
        for d in discounts
    ]

    fig, ax = plt.subplots()
    ax.plot(discounts, profits)
    ax.axhline(0, color="red", linestyle="--")
    ax.set_xlabel("Discount (%)")
    ax.set_ylabel("Profit ($)")
    st.pyplot(fig)

# --------------------------------------------------
# TAB 3 — GAME THEORY
# --------------------------------------------------
with tab3:
    st.subheader("Strategic Interaction")

    if profit < 0:
        st.error("⚠ This strategy triggers a PRICE WAR (Dominated Strategy)")
    elif discount > 20:
        st.warning("⚠ High discount may provoke retaliation from Platform A")
    else:
        st.success("✅ Strategy lies in a Nash-stable region")

    st.markdown("""
    **Game Theory Interpretation**
    - Aggressive discounts benefit users short-term
    - But provoke retaliation
    - Nash equilibrium exists at **moderate discounts**
    """)

# --------------------------------------------------
# TAB 4 — PRODUCT ROADMAP
# --------------------------------------------------
with tab4:
    st.subheader("Product Lifecycle Strategy")

    st.markdown("""
    **Introduction**
    - Off-peak entry
    - Targeted discounts
    - Data-driven experimentation

    **Growth**
    - Reduce subsidies
    - Expand operating hours
    - Focus on retention

    **Maturity**
    - Feature differentiation
    - Loyalty programs

    **Innovation**
    - New services
    - Avoid commoditization
    """)

    st.success("🎯 Strategy aligned with Product Management lifecycle principles")
