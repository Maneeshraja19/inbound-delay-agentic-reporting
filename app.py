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
st.divider()
st.header("🔮 Predict Delay Risk for a New Shipment")
st.markdown("Enter shipment details below to get a live prediction from the trained model.")

import joblib

@st.cache_resource
def load_model():
    model = joblib.load("src/delay_model.pkl")
    features = joblib.load("src/model_features.pkl")
    return model, features

model, feature_cols = load_model()

col1, col2 = st.columns(2)

with col1:
    shipping_mode = st.selectbox("Shipping Mode", sorted(df['Shipping Mode'].unique()))
    order_region = st.selectbox("Order Region", sorted(df['Order Region'].unique()))
    order_country = st.selectbox("Order Country", sorted(df['Order Country'].unique()))

with col2:
    category_name = st.selectbox("Category Name", sorted(df['Category Name'].unique()))
    scheduled_days = st.number_input("Days for Shipment (Scheduled)", min_value=0, max_value=10, value=4)
    order_month = st.selectbox("Order Month", list(range(1, 13)))

if st.button("Predict"):
    # Build a single-row input matching the model's expected feature format
    input_dict = {col: 0 for col in feature_cols}
    input_dict['Days for shipment (scheduled)'] = scheduled_days
    input_dict['order_month'] = order_month

    mode_col = f"Shipping Mode_{shipping_mode}"
    region_col = f"Order Region_{order_region}"
    country_col = f"Order Country_{order_country}"
    category_col = f"Category Name_{category_name}"

    for col in [mode_col, region_col, country_col, category_col]:
        if col in input_dict:
            input_dict[col] = 1

    input_df = pd.DataFrame([input_dict])[feature_cols]
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Predicted: LATE (confidence: {probability:.1%})")
    else:
        st.success(f"✅ Predicted: ON TIME (confidence: {1-probability:.1%})")