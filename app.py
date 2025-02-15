from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer, KafkaConsumer
from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer
import redis
import json
import joblib
import numpy as np
import threading

app = FastAPI()

# 🟢 Start Testcontainers for Redis and Kafka
redis_container = RedisContainer().start()
redis_host = redis_container.get_container_host_ip()
redis_port = redis_container.get_exposed_port(6379)
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

kafka_container = KafkaContainer().start()
kafka_bootstrap_servers = kafka_container.get_bootstrap_server()

# 🟢 Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 🟢 Load Pre-trained ML Model
model = joblib.load("fraud_model.pkl")

# 🟢 Define Kafka Topic
TOPIC_NAME = "transactions"

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    customer_id: str
    merchant_id: str
    location: str
    timestamp: str
    feature_vector: list

@app.post("/process_transaction/")
def process_transaction(transaction: Transaction):
    """Send transaction data to Kafka."""
    try:
        producer.send(TOPIC_NAME, transaction.dict())
        return {"status": "Transaction sent for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def detect_fraud(transaction_data):
    """Predict fraud and store alerts in Redis."""
    features = np.array(transaction_data['feature_vector']).reshape(1, -1)
    prediction = model.predict(features)[0]
    if prediction == 1:
        redis_client.lpush("fraud_alerts", json.dumps(transaction_data))

def consume_transactions():
    """Consume Kafka messages and detect fraud."""
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=kafka_bootstrap_servers,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    for msg in consumer:
        detect_fraud(msg.value)

# 🟢 Run Kafka Consumer in Background
threading.Thread(target=consume_transactions, daemon=True).start()

@app.get("/fraud_alerts/")
def get_fraud_alerts():
    """Retrieve fraud alerts from Redis."""
    alerts = redis_client.lrange("fraud_alerts", 0, -1)
    return [json.loads(alert) for alert in alerts]
