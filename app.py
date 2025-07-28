import googlemaps
import streamlit as st
import numpy as np
import pandas as pd
from joblib import load

# Initialize Google Maps Client
gmaps = googlemaps.Client(key='AIzaSyA2wJTtkF8ySBHArbo6XB4QmiKLXx-Cxf0')

# Load the trained model
model = load('shelf_life_model.joblib')

# Title
st.title("🧪 Post-Harvest Shelf Life Predictor")

# User input fields
st.write("### 🌿 Enter Environmental and Transport Conditions")

temperature = st.slider("🌡️ Temperature (°C)", 10, 40, 25)
humidity = st.slider("💧 Humidity (%)", 30, 100, 70)
transport_time = st.number_input("🚚 Transport Time (hours)", min_value=0.0, step=0.5)

# Location input for Google Maps Distance Matrix
st.write("### 📍 Enter Locations for Distance Calculation")
origin = st.text_input("Enter Origin Location (e.g., Nuwara Eliya)")
destination = st.text_input("Enter Destination Location (e.g., Colombo)")

distance = None

if st.button("📏 Calculate Distance"):
    if origin and destination:
        try:
            result = gmaps.distance_matrix(origin, destination, mode='driving')
            distance_meters = result['rows'][0]['elements'][0]['distance']['value']
            distance = distance_meters / 1000  # Convert to km
            st.success(f"✅ Distance: {distance:.2f} km")
            st.session_state.distance = distance
        except Exception as e:
            st.error(f"Error calculating distance: {e}")
    else:
        st.warning("⚠️ Please enter both origin and destination.")

# Use previously calculated distance from session if available
distance = st.session_state.get("distance", None)

if st.button("📊 Predict Shelf Life"):
    if distance is not None:
        input_data = np.array([[temperature, humidity, transport_time, distance]])
        prediction = model.predict(input_data)[0]

        st.success(f"✅ Estimated Shelf Life Remaining: {prediction:.2f} days")

        st.session_state.prediction = prediction
        st.session_state.input_data = {
            "Temperature": temperature,
            "Humidity": humidity,
            "Transport Time (hrs)": transport_time,
            "Distance (km)": distance,
            "Predicted Shelf Life (days)": prediction
        }
    else:
        st.warning("⚠️ Please calculate the distance first.")

# Show download button if prediction is made
if "prediction" in st.session_state:
    report_df = pd.DataFrame([st.session_state.input_data])
    csv = report_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Prediction Report as CSV",
        data=csv,
        file_name="shelf_life_report.csv",
        mime="text/csv"
    )