import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

REDIS_URL = os.getenv("REDIS_URL")

LLM_MASTER_KEY=os.getenv("LLM_MASTER_KEY")

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")
KAFKA_CONSUMER_TOPIC = os.getenv("KAFKA_CONSUMER_TOPIC", "core_attack_topic")
KAFKA_PRODUCER_TOPIC = os.getenv("KAFKA_PRODUCER_TOPIC", "attack_result_topic")