import streamlit as st
import numpy as np
import pandas as pd
from joblib import load

# Load the model
model = load('shelf_life_model.joblib')

st.title("🧪 Post-Harvest Shelf Life Predictor")

st.write("Enter current environmental and transport conditions:")

temperature = st.slider("🌡️ Temperature (°C)", 10, 40, 25)
humidity = st.slider("💧 Humidity (%)", 30, 100, 70)
transport_time = st.number_input("🚚 Transport Time (hours)", min_value=0.0, step=0.5)
distance = st.number_input("🛣️ Distance (km)", min_value=0.0, step=1.0)

if st.button("Predict Shelf Life"):
    input_data = np.array([[temperature, humidity, transport_time, distance]])
    prediction = model.predict(input_data)[0]
    st.success(f"✅ Estimated Shelf Life Remaining: {prediction:.2f} days")

 # Store in session for download access
    st.session_state.prediction = prediction
    st.session_state.input_data = {
        "Temperature": temperature,
        "Humidity": humidity,
        "Transport Time": transport_time,
        "Distance": distance,
        "Predicted Shelf Life": prediction
    }

# Show Download Button only after prediction
if "prediction" in st.session_state:
    report_df = pd.DataFrame([st.session_state.input_data])
    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Prediction Report as CSV", csv, "shelf_life_report.csv", "text/csv")