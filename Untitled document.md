# **Fraud Detection System**

## **Overview**

This project is a fraud detection system using **Isolation Forest**, **FastAPI**, **Kafka**, and **Redis**. It processes transactions, classifies them as fraudulent or legitimate, and stores the results for further analysis.

## **Features**

* **Real-time transaction processing**  
* **Fraud detection using Isolation Forest**  
* **Kafka for event streaming**  
* **Redis for storing fraud alerts**  
* **Automated transaction submission using `rn.py`**

## **Installation and Setup**

### **Prerequisites**

Make sure you have the following installed:

* Python 3.11+  
* Kafka  
* Redis  
* FastAPI

### **Setup Commands**

\# Clone the repository  
git clone https://github.com/your-repo/fraud-detection.git  
cd fraud-detection

\# Create a virtual environment  
python \-m venv .venv  
source .venv/bin/activate  \# On Windows use \`.venv\\Scripts\\activate\`

\# Install dependencies  
pip install \-r requirements.txt

\# Start Kafka and Redis (Ensure they are running before execution)  
kafka-server-start.sh config/server.properties  \# Start Kafka  
redis-server  \# Start Redis

## **Running the System**

### **Train and Save the Model**

python model.py

### **Start the FastAPI Server**

uvicorn app:app \--reload

### **Run `rn.py` for Automated Processing**

The `rn.py` script automates sending transactions and recording fraud alerts.

python rn.py

Running `rn.py` will:

1. Generate test transactions.  
2. Send them to the API.  
3. Record fraud alerts from Redis.

## **API Endpoints**

### **1\. Submit a Transaction**

**Endpoint:** `POST /process_transaction/`

#### **Request Format**

{  
  "transaction\_id": "12345",  
  "amount": 120.5,  
  "customer\_id": "32",  
  "merchant\_id": "14",  
  "location": "New York",  
  "timestamp": "2025-02-15T12:34:56Z",  
  "feature\_vector": \[120.5, 32, 14, 0.8, 0.6\]  
}

#### **Response**

{"status": "Transaction sent for processing."}

### **2\. Get Fraud Alerts**

**Endpoint:** `GET /fraud_alerts/`

#### **Response Example**

\[  
  {"transaction\_id": "12345", "fraud": true}  
\]

## **How Fraud is Detected**

* The Isolation Forest model is trained on a dataset with features like transaction amount, customer ID, merchant ID, and additional numeric features.  
* It classifies transactions based on the anomaly score derived from the feature vector.  
* Transactions with significantly different patterns from normal transactions are flagged as fraud.

## **Technologies Used**

* **FastAPI**: API development  
* **Scikit-Learn**: Machine learning (Isolation Forest)  
* **Kafka**: Event streaming for transactions  
* **Redis**: Storing fraud alerts  
* **Joblib**: Model persistence

## **Common Questions & Answers**

### **Q1: Why use Kafka?**

Kafka allows event-driven transaction processing, making it scalable for high-volume transactions.

### **Q2: What is the role of Redis?**

Redis stores fraud alerts in-memory for fast retrieval.

### **Q3: How does the system classify frauds?**

It uses Isolation Forest, which detects anomalies in the feature vector of transactions.

### **Q4: What happens when I run `rn.py`?**

It automatically sends transactions and records fraud alerts without manual intervention.

### **Q5: What is a normal feature vector?**

A normal feature vector consists of standard transaction behavior derived from historical data.

## **Conclusion**

This system provides an efficient way to detect fraudulent transactions in real-time using machine learning and event-driven processing.

---

**Author:** Your Name  
 **Date:** 2025-02-15

