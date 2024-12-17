from confluent_kafka import Producer
import json

# Kafka 설정
KAFKA_BROKER = "10.0.4.172:29091"  # Kafka 브로커 주소
KAFKA_TOPIC = "location"       # 메시지를 보낼 Kafka 토픽

# Producer 콜백 함수 (메시지가 성공적으로 전송되었을 때 호출)
def delivery_callback(err, msg):
    if err is not None:
        print(f"카프카 메시지 전송 실패: {err}")
    else:
        print(f"카프가 메시지 전송 성공  TOPIC: {msg.topic()} [{msg.partition()}]")

# Kafka Producer 생성
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Kafka에 메시지 보내는 함수
def send_to_kafka(message: dict):
    producer.produce(KAFKA_TOPIC, json.dumps(message), callback=delivery_callback)
    producer.flush()  # 버퍼에 쌓인 메시지를 보내기 위해 flush() 호출
