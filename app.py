import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inbound Delay Dashboard", layout="wide")

st.title("📦 Inbound Logistics Delay Dashboard")
st.markdown("Analyzing shipment delays to identify root causes and predict risk.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/dashboard_data.csv")
    return df

df = load_data()

# --- Overview metrics ---
col1, col2, col3 = st.columns(3)
overall_late_rate = df['is_late'].mean()
col1.metric("Overall Late Rate", f"{overall_late_rate:.1%}")
col2.metric("Total Shipments", f"{len(df):,}")
col3.metric("Model PR-AUC", "0.843")

st.divider()

# --- Shipping Mode chart ---
st.subheader("Late Rate by Shipping Mode")
mode_data = df.groupby('Shipping Mode')['is_late'].mean().sort_values(ascending=False).reset_index()
fig1 = px.bar(mode_data, x='Shipping Mode', y='is_late', 
              labels={'is_late': 'Late Rate'})
st.plotly_chart(fig1, width='stretch')
st.caption("First Class shows 100% late rate — not due to poor execution, but because the promised delivery window (1 day) is unrealistic compared to actual delivery time (~2 days).")

col_a, col_b = st.columns(2)

# --- Region chart ---
with col_a:
    st.subheader("Late Rate by Region")
    region_data = df.groupby('Order Region')['is_late'].mean().sort_values(ascending=False).reset_index()
    fig2 = px.bar(region_data, x='is_late', y='Order Region', orientation='h',
                  labels={'is_late': 'Late Rate'})
    st.plotly_chart(fig2, width='stretch')

# --- Month chart ---
with col_b:
    st.subheader("Late Rate by Month")
    month_data = df.groupby('order_month')['is_late'].mean().sort_index().reset_index()
    fig3 = px.line(month_data, x='order_month', y='is_late', markers=True,
                    labels={'is_late': 'Late Rate', 'order_month': 'Month'})
    st.plotly_chart(fig3, width='stretch')

st.divider()
st.markdown("**Key takeaway:** The delivery *promise* itself — not geography or season — is the primary driver of late deliveries in this dataset.")
st.markdown("[View full analysis on GitHub](https://github.com/Maneeshraja19/inbound-delay-agentic-reporting)")