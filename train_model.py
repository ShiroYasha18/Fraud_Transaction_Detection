import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

np.random.seed(42)
data = pd.DataFrame({
    "amount": np.random.normal(100, 50, 1000),
    "customer_id": np.random.randint(1, 100, 1000),
    "merchant_id": np.random.randint(1, 50, 1000),
    "feature1": np.random.rand(1000),
    "feature2": np.random.rand(1000),
})

labels = np.where(np.random.rand(1000) < 0.05, 1, -1)

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(data)

joblib.dump(model, "fraud_model.pkl")
print("Fraud detection model saved!")
