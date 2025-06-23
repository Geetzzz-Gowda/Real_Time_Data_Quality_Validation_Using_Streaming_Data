import streamlit as st
import pandas as pd
import glob
import time
import os

st.title("Real-Time Sensor Data Quality Dashboard")

DATA_PATH = "C:/Users/geeta/spark_output/*.json"

@st.cache_data(ttl=10)
def load_data():
    files = glob.glob(DATA_PATH)
    if not files:
        return pd.DataFrame()
    # Read all JSON files into one dataframe
    df = pd.concat((pd.read_json(f, lines=True) for f in files), ignore_index=True)
    return df

placeholder = st.empty()

while True:
    df = load_data()
    if df.empty:
        placeholder.info("Waiting for data...")
    else:
        # Show metrics
        total = len(df)
        anomalies = len(df[df["anomaly"] == -1])
        normal = total - anomalies

        placeholder.metric("Total Records", total)
        placeholder.metric("Anomalies Detected", anomalies)
        placeholder.metric("Normal Records", normal)

        # Show recent data table
        st.dataframe(df.sort_values(by="timestamp", ascending=False).head(20))

    time.sleep(5)  # refresh every 5 seconds
