from kafka import KafkaConsumer
import json
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Kafka Consumer 설정
def create_kafka_consumer():
    consumer = KafkaConsumer(
        'location',  # Kafka의 토픽명
        bootstrap_servers=['localhost:9092'],  # Kafka 서버 주소
        group_id='location-group',  # Consumer 그룹 ID
        auto_offset_reset='earliest',  # 처음부터 메시지를 받기 시작
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # 메시지 디코딩
    )
    return consumer

# 위도와 경도를 기반으로 DB에서 500m 내 주차장 정보 조회
def find_nearby_parking(lat, lon):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # SQL 쿼리 작성 (Haversine 공식을 이용하여 500m 내 주차장 조회)
    query = """
    SELECT * FROM parkingarea_info
    WHERE
    (6371 * acos(cos(radians(%s)) * cos(radians(park_la)) * cos(radians(park_lo) - radians(%s)) + sin(radians(%s)) * sin(radians(park_la)))) <= 0.5
    """
    cursor.execute(query, (lat, lon, lat))
    result = cursor.fetchall()
    connection.close()
    return result

# Kafka 메시지 처리 및 주차장 정보 조회
def process_messages():
    consumer = create_kafka_consumer()

    for message in consumer:
        location = message.value
        lat = location['latitude']
        lon = location['longitude']

        print(f"Received location - Latitude: {lat}, Longitude: {lon}")

        # 500m 내 주차장 정보 조회
        nearby_parking = find_nearby_parking(lat, lon)

        if nearby_parking:
            print("Nearby Parking Spots:")
            for parking in nearby_parking:
                print(parking)
        else:
            print("No nearby parking found.")

if __name__ == "__main__":
    process_messages()
