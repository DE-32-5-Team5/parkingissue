#######################################################################
# easy start code                                                     #
#                                                                     #
# spark-submit \                                                      #
#  --conf spark.sql.warehouse.dir=/tmp/spark-warehouse \              #
#  --master spark://spark-master:7077 \                               #
#  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 \      #
#  /app/sample.py                                                     #
#######################################################################

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, StructField, FloatType
import requests

db_config = {
        "url": "10.0.4.80:6033",
        "user": "root",
        "password": "samdul2024$",
        "database": "parkingissue"
    }

# Kafka 스트리밍 설정
def read_from_kafka(spark, kafka_ip):
    schema = StructType([
        StructField("latitude", StringType(), True),
        StructField("longitude", StringType(), True)
    ])
    kafka_df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", f"{kafka_ip}:29091") \
        .option("subscribe", "location") \
        .option("startingOffsets", "latest") \
        .load()
    return kafka_df.selectExpr("cast(value as string) as value").select(from_json(col("value"), schema)).alias("json")

# 거리 계산 로직
def calculate_nearby_parkings(latitude, longitude, db_config):
    jdbc_url = f"jdbc:mysql://{db_config['url']}/{db_config['database']}"
    query = f"""
    SELECT park_id, park_nm, park_addr, park_lo, park_la,
        (6371 * acos(cos(radians({latitude})) * cos(radians(park_la)) *
        cos(radians(park_lo) - radians({longitude})) + sin(radians({latitude})) *
        sin(radians(park_la)))) AS distance
    FROM parkingarea_info
    WHERE park_la BETWEEN {latitude} - 0.0057 AND {latitude} + 0.0057
        AND park_lo BETWEEN {longitude} - 0.0045 AND {longitude} + 0.0045
    ORDER BY distance ASC
    LIMIT 20
    """
    # MySQL 데이터 읽기
    result_df = spark.read.format("jdbc") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("url", jdbc_url) \
        .option("user", db_config['user']) \
        .option("password", db_config['password']) \
        .option("query", query) \
        .load()
    return result_df

# FastAPI POST 요청
def send_to_fastapi(batch_df):
    url = "https://parkingissue.online/api/getlocation"
    df = batch_df.toPandas()
    print("*"*100)
    print(df.info())
    print("*"*100)
    df['park_id'] = df['park_id'].astype(str)
    df['park_nm'] = df['park_nm'].astype(str)
    df['park_addr'] = df['park_addr'].astype(str)
    df['park_lo'] = df['park_lo'].astype(float)
    df['park_la'] = df['park_la'].astype(float)
    df['distance'] = df['distance'].astype(float)

    data_list = df.to_dict(orient='records')

    try:
        response = requests.post(url, json=data_list, timeout=3)
        if response.status_code != 200:
            print(f"Error sending data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

# 배치 처리
def process_batch(batch_df, batch_id):
    for row in batch_df.collect():
        print("*"*10)
        print(row)
        print("*"*100)
        latitude = row['from_json(value)'].latitude
        longitude = row['from_json(value)'].longitude
        print(latitude)
        print(type(longitude))
        print("*"*100)
        if latitude is not None and longitude is not None:
            nearby_parking_df = calculate_nearby_parkings(latitude, longitude, db_config)
            send_to_fastapi(nearby_parking_df)

# 메인 실행
if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Spark Structured Streaming") \
        .master("spark://172.18.0.2:7077") \
        .config("jars", "mysql-connector-j-9.1.0.jar") \
        .config("spark.driver.extraClassPath", "mysql-connector-j-9.1.0.jar") \
        .config("spark.executor.extraClassPath", "mysql-connector-j-9.1.0.jar") \
        .getOrCreate()

    kafka_ip = "10.0.4.172"

    kafka_stream = read_from_kafka(spark, kafka_ip)
    query = kafka_stream.writeStream \
        .outputMode("append") \
        .foreachBatch(process_batch) \
        .start()
    query.awaitTermination()

