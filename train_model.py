# sample_training.py
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

# Simulated historical data
X_train = np.random.normal(0, 1, (1000, 2))  # e.g., temperature, humidity

model = IsolationForest(contamination=0.05)
model.fit(X_train)

# Save model
joblib.dump(model, "anomaly_model.pkl")
