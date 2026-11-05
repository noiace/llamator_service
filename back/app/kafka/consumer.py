from confluent_kafka import Consumer, KafkaError
import json

from worker.tasks import run_custom_llm_test
from database.crud import create_pending_report
from config import KAFKA_CONSUMER_TOPIC as kafka_topic
from config import KAFKA_BOOTSTRAP_SERVER as kafka_server

print("=== 1. ЗАПУСК КОНСЬЮМЕРА (ИМПОРТЫ ПРОШЛИ УСПЕШНО) ===", flush=True)
consumer = Consumer({
    'bootstrap.servers': kafka_server,
    'group.id': 'red-team-llamator-group',
    'enable.auto.commit': False,
    'auto.offset.reset': 'earliest'
})

# Временно захардкодим топик, чтобы точно совпадало с Go
debug_topic = "core_attack_topic"
consumer.subscribe([debug_topic])

print(f"=== 2. ПОДПИСАЛИСЬ НА ТОПИК {debug_topic}, ЖДЕМ СООБЩЕНИЙ... ===", flush=True)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(f"Ошибка Kafka: {msg.error()}")
            continue

    raw_message = msg.value().decode('utf-8')
    print(f"ПОЙМАНО СООБЩЕНИЕ ИЗ GO: {raw_message}")

    attack_data = json.loads(msg.value().decode('utf-8'))

    if attack_data.get("tool_name") != "llamator":
        print(f"ПРОПУСК: не совпал tool_name (получено: {attack_data.get('tool_name')})")
        consumer.commit(message=msg)
        continue

    report_id = create_pending_report(attack_data)

    print(f"=== 4. ЗАПИСЬ СОЗДАНА В БД, REPORT_ID: {report_id} ===", flush=True)

    run_custom_llm_test.delay(report_id)
    print("=== 5. ЗАДАЧА УСПЕШНО ОТПРАВЛЕНА В CELERY! ===", flush=True)
    consumer.commit(message=msg)