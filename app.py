import streamlit as st
import requests

API_URL = "https://house-price-prediction-9aoe.onrender.com"

st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")
st.title("🏠 House Price Prediction")
st.write("Enter property details below to get an AI-powered price estimate.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        housing_median_age = st.number_input("Housing Median Age", min_value=1.0, max_value=100.0, value=25.0)
        total_rooms        = st.number_input("Total Rooms",         min_value=1.0, max_value=50000.0, value=2000.0)
        total_bedrooms     = st.number_input("Total Bedrooms",      min_value=1.0, max_value=10000.0, value=400.0)
        population         = st.number_input("Population",          min_value=1.0, max_value=50000.0, value=1200.0)
    with col2:
        households      = st.number_input("Households",              min_value=1.0, max_value=10000.0, value=380.0)
        median_income   = st.number_input("Median Income (in $10k)", min_value=0.5, max_value=15.0, value=4.5, step=0.1)
        ocean_proximity = st.selectbox("Ocean Proximity",
                            options=["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"])
    submitted = st.form_submit_button("Predict Price", use_container_width=True)

if submitted:
    payload = {
        "housing_median_age": housing_median_age,
        "total_rooms":        total_rooms,
        "total_bedrooms":     total_bedrooms,
        "population":         population,
        "households":         households,
        "median_income":      median_income,
        "ocean_proximity":    ocean_proximity,
    }
    with st.spinner("Getting prediction from API..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=60)
            if response.status_code == 200:
                predicted = response.json()["predicted_price"]
                st.success(f"### Predicted House Price: **${predicted:,.2f}**")
                st.info("Prediction stored in Neon PostgreSQL database.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            st.warning("API is waking up (cold start). Wait 30 seconds and try again.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API.")

st.divider()
st.subheader("Last 5 Predictions")
if st.button("Refresh History"):
    with st.spinner("Fetching..."):
        try:
            res = requests.get(f"{API_URL}/history", timeout=60)
            if res.status_code == 200:
                records = res.json()[:5]
                if records:
                    for r in records:
                        st.write(f"ID {r['id']} | Age: {r['housing_median_age']} | "
                                 f"Income: {r['median_income']} | Location: {r['ocean_proximity']} | "
                                 f"Price: ${r['predicted_price']:,.2f} | {r['timestamp'][:19]}")
                else:
                    st.info("No predictions yet.")
        except Exception as e:
            st.error(f"Error: {e}")