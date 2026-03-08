import os
import sqlite3
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'frontend-ui', 'system_logs.db')
model_save_path = os.path.join(BASE_DIR, 'isolation_forest_model.pkl')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT cpu_usage, memory_usage, disk_usage, network_usage, swap_usage FROM logs")
data = cursor.fetchall()
conn.close()

if not data:
    data = np.random.rand(1000, 5) * 100
else:
    data = np.array(data)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', IsolationForest(contamination=0.01, random_state=42))
])

pipeline.fit(data)

joblib.dump(pipeline, model_save_path)
print(f"Model trained and saved as {model_save_path}")
