# Import Libraries
import streamlit as st
import pandas as pd
import joblib

# Load Model
model = joblib.load("model.pkl")

# Load Label Encoder
le = joblib.load("label_encoder.pkl")

# Title
st.title("🏠 House Price Prediction")

st.write("Enter the house details below.")


# User Inputs

housing_median_age = st.number_input("Housing Median Age", value=25)

total_rooms = st.number_input("Total Rooms", value=5)

total_bedrooms = st.number_input("Total Bedrooms", value=5)

population = st.number_input("Population", value=1200)

households = st.number_input("Households", value=5)

median_income = st.number_input("Median Income", value=4.5)

ocean_proximity = st.selectbox(

    "Ocean Proximity",

    le.classes_

)


# Prediction

if st.button("Predict House Price"):

    # Encode Ocean Proximity
    ocean = le.transform([ocean_proximity])[0]

    # Create DataFrame
    input_data = pd.DataFrame({

        "housing_median_age":[housing_median_age],

        "total_rooms":[total_rooms],

        "total_bedrooms":[total_bedrooms],

        "population":[population],

        "households":[households],

        "median_income":[median_income],

        "ocean_proximity":[ocean]})

    # Prediction
    prediction = model.predict(input_data)

    st.success(f"Estimated House Price : ${prediction[0]:,.2f}")