import streamlit as st
import pandas as pd
import plotly.express as px

st.title("FEMA Disaster Relief Dashboard")
st.write("Eileena Doek")

# -------- Load data (cached & trimmed so the app doesn't crash) --------
@st.cache_data
def load_data():
    url = "https://storage.googleapis.com/info_450/IndividualAssistanceHousingRegistrantsLargeDisasters%20(1).csv"
    use_cols = ["repairAmount", "tsaEligible"]
    df = pd.read_csv(url, usecols=use_cols)

    # Drop rows where repairAmount or tsaEligible is missing
    df = df.dropna(subset=["repairAmount", "tsaEligible"])

    # Convert repairAmount to numeric just in case
    df["repairAmount"] = pd.to_numeric(df["repairAmount"], errors="coerce")
    df = df.dropna(subset=["repairAmount"])

    # Optional: sample to keep the charts fast & safe
    if len(df) > 200_000:
        df = df.sample(200_000, random_state=42)

    return df

df = load_data()

# -------- Data preview --------
st.subheader("Data Preview")
st.write(df.head())

# -------- Histogram of repairAmount --------
st.subheader("Histogram of Repair Amount")
fig_hist = px.histogram(
    df,
    x="repairAmount",
    nbins=30,
    title="Distribution of Repair Amounts"
)
st.plotly_chart(fig_hist, use_container_width=True)

# -------- Boxplot of repairAmount by tsaEligible --------
st.subheader("Boxplot: Repair Amount by TSA Eligibility")
fig_box = px.box(
    df,
    x="tsaEligible",
    y="repairAmount",
    title="Repair Amount by TSA Eligibility",
    labels={
        "tsaEligible": "TSA Eligible (1 = Yes, 0 = No)",
        "repairAmount": "Repair Amount"
    }
)
st.plotly_chart(fig_box, use_container_width=True)

# -------- Optional short text insight --------
st.markdown(
    """
    **Insight:** Based off of the data, TSA-Eligible households tend to have higher repair amounts than Non-Eligible households. This fits TSA's goals of helping those in greater need.
    """
)
