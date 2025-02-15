import requests
import time
import json
import random
from datetime import datetime

# API Endpoints
TRANSACTION_URL = "http://127.0.0.1:8000/process_transaction/"
FRAUD_ALERTS_URL = "http://127.0.0.1:8000/fraud_alerts/"


# Function to generate random transactions
def generate_transaction():
    return {
        "transaction_id": str(random.randint(10000, 99999)),
        "amount": round(random.uniform(10, 500), 2),
        "customer_id": str(random.randint(1, 100)),
        "merchant_id": str(random.randint(1, 50)),
        "location": random.choice(["New York", "Los Angeles", "Chicago", "Houston"]),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "feature_vector": [
            round(random.uniform(10, 500), 2),  # amount
            random.randint(1, 100),  # customer_id
            random.randint(1, 50),  # merchant_id
            round(random.uniform(0, 1), 2),  # random feature
            round(random.uniform(0, 1), 2)  # another random feature
        ]
    }


# Function to send a transaction
def send_transaction(transaction):
    response = requests.post(TRANSACTION_URL, json=transaction)
    return response.json()


# Function to check fraud alerts
def check_fraud_alerts():
    response = requests.get(FRAUD_ALERTS_URL)
    if response.status_code == 200:
        frauds = response.json()
        if frauds:
            print(f"🚨 Fraud detected: {frauds}")
            with open("fraud_logs.json", "a") as f:
                json.dump(frauds, f, indent=4)
                f.write("\n")
        return frauds
    return []


# Main loop to automate sending transactions and checking frauds
def main():
    for _ in range(100):  # Sending 10 test transactions
        transaction = generate_transaction()
        print(f"📤 Sending Transaction: {transaction}")
        response = send_transaction(transaction)
        print(f"✅ Response: {response}")
        time.sleep(1)  # Wait before sending the next transaction

    print("\n🔍 Checking Fraud Alerts...\n")
    time.sleep(3)
    check_fraud_alerts()


if __name__ == "__main__":
    main()
