from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='kafka-server:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)

def send_location(latitude: float, longitude: float):
    """위도와 경도 데이터를 Kafka 'location' 토픽에 전송"""
    data = {'latitude': latitude, 'longitude': longitude}
    producer.send('location', data)
    producer.flush()  # 메시지가 Kafka에 전송될 때까지 기다림
    print(f"Location sent: {data}")

# 테스트용 함수 호출
if __name__ == "__main__":
    send_location(37.5665, 126.9780)  # 예시 위도, 경도 (서울시청)
