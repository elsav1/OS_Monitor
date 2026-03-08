import os
import sqlite3
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib


MODEL_PATH = "anomaly_detector_pipeline.joblib"
DB_PATH = "system_logs.db"


def load_historical_data(db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cpu_usage, memory_usage, disk_usage, network_usage, swap_usage FROM logs")
        data = cursor.fetchall()
        conn.close()

        if not data:
            print("No historical data found in the database. Generating random data for training.")
            # Generate random data with 5 features if no data is found
            return np.random.rand(1000, 5) * 100
        else:
            print(f"Loaded {len(data)} records from the database.")
            return np.array(data)
    except Exception as e:
        print(f"Error loading historical data from database: {e}. Generating random data for training.")
        # Fallback to random data if database loading fails
        return np.random.rand(1000, 5) * 100


def train_anomaly_detection_pipeline(data, model_save_path=MODEL_PATH):
    print("Building and training anomaly detection pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', IsolationForest(contamination=0.01, random_state=42))
    ])

    pipeline.fit(data)
    joblib.dump(pipeline, model_save_path)
    print(f"Model training completed and pipeline saved to {model_save_path}.")


def train_model_from_historical_data():
    data = load_historical_data()
    train_anomaly_detection_pipeline(data)


if __name__ == '__main__':
    train_model_from_historical_data()
