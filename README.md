# Fraud Detection System Documentation

## Overview
This fraud detection system utilizes machine learning (Isolation Forest) to classify financial transactions as either normal or fraudulent based on extracted feature vectors. The system integrates with Kafka for real-time transaction streaming and Redis for caching fraud alerts.

## Architecture
### Components:
1. **API Layer (FastAPI)**
   - Handles incoming transaction requests.
   - Sends transactions to Kafka for processing.
   
2. **Kafka (Message Broker)**
   - Streams transactions to be processed asynchronously.
   
3. **Fraud Detection Service**
   - Consumes Kafka messages.
   - Uses an Isolation Forest model to detect fraud.
   - Stores fraud alerts in Redis.
   
4. **Redis (Cache Storage)**
   - Stores flagged fraudulent transactions for quick retrieval.
   
## Machine Learning Model
### Model: Isolation Forest
- **Input Features:**
  - `amount`
  - `customer_id`
  - `merchant_id`
  - `feature1`
  - `feature2`
- **Training:**
  - Trained on synthetic transaction data.
  - Identifies anomalies using an unsupervised learning approach.
- **Prediction:**
  - Returns `-1` for fraudulent transactions, `1` for normal ones.

## API Endpoints
### 1. **Process Transaction**
   - **URL:** `/process_transaction/`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "transaction_id": "12345",
       "amount": 120.5,
       "customer_id": "32",
       "merchant_id": "14",
       "location": "New York",
       "timestamp": "2025-02-15T12:34:56Z",
       "feature_vector": [120.5, 32, 14, 0.8, 0.6]
     }
     ```
   - **Response:**
     ```json
     { "status": "Transaction sent for processing." }
     ```

### 2. **Retrieve Fraud Alerts**
   - **URL:** `/fraud_alerts/`
   - **Method:** `GET`
   - **Response:**
     ```json
     [
       {
         "transaction_id": "12345",
         "amount": 120.5,
         "customer_id": "32",
         "merchant_id": "14",
         "location": "New York",
         "timestamp": "2025-02-15T12:34:56Z"
       }
     ]
     ```

## Kafka & Redis Usage
### **Kafka**
- Handles asynchronous message processing.
- Allows scalability in real-time fraud detection.

### **Redis**
- Stores flagged fraudulent transactions for quick lookup.
- Avoids repeated processing of fraudulent transactions.

## Common Errors & Fixes
### 1. **Missing Fields in API Request**
   - **Error:**
     ```json
     { "detail": [{"msg": "Field required", "loc": ["body", "amount"]}] }
     ```
   - **Fix:** Ensure all required fields are included in the request.

### 2. **Invalid Feature Vector Size**
   - **Error:**
     ```plaintext
     ValueError: X has 4 features, but IsolationForest is expecting 5 features.
     ```
   - **Fix:** Ensure `feature_vector` has all required features.

## Future Improvements
- Improve fraud detection accuracy with deep learning models (e.g., LSTMs for sequential patterns).
- Enhance real-time analysis with Apache Flink or Spark Streaming.
- Implement a dashboard for monitoring transactions.

## FAQs & Presentation Questions
1. **Why use Isolation Forest for fraud detection?**
   - It’s effective for detecting outliers in an unsupervised setting.

2. **How does Kafka help in fraud detection?**
   - Kafka enables scalable, real-time streaming of transaction data.

3. **Why use Redis instead of a database for fraud alerts?**
   - Redis provides faster read/write access for real-time fraud detection.

4. **How can this system be extended to handle large-scale transactions?**
   - By deploying Kafka in a cluster and using distributed ML models.

---
This documentation provides a comprehensive overview of the fraud detection system, its architecture, API, and improvements. 🚀
