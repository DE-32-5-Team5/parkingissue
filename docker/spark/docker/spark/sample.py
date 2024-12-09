from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, FloatType
import requests

# Kafka 스트리밍 설정
def read_from_kafka(spark, kafka_ip):
    schema = StructType([
        StructField("user_lo", FloatType(), True),
        StructField("user_la", FloatType(), True)
    ])
    kafka_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", f"{kafka_ip}:9092") \
        .option("subscribe", "location") \
        .option("startingOffsets", "latest") \x
        .load()
    return kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# 거리 계산 로직
def calculate_nearby_parkings(df, db_config):
    # db_config: dict with keys ('url', 'user', 'password', 'table')
    user_lo = df.col('user_lo')
    user_la = df.col('user_la')

    jdbc_url = f"jdbc:mysql://{db_config['url']}/{db_config['database']}"
    query = f"""
        SELECT park_id, park_nm, park_addr, park_lo, park_la,
        (6371 * acos(cos(radians({user_la})) * cos(radians({user_lo})) *
        cos(radians({user_la}) - radians({user_lo})) + sin(radians({user_la})) *
        sin(radians({user_lo})))) AS distance
        FROM parkingarea_info
        WHERE park_la BETWEEN {user_la} - 0.0057 AND {user_la} + 0.0057
          AND park_lo BETWEEN {user_lo} - 0.0045 AND {user_lo} + 0.0045
        ORDER BY distance ASC LIMIT 20
    """
    return df.crossJoin(spark.read.format("jdbc")
                   .option("url", jdbc_url)
                   .option("user", db_config['user'])
                   .option("password", db_config['password'])
                   .option("query", query)
                   .load())

# FastAPI POST 요청
def send_to_fastapi(df):
    url = "http://10.0.4.74:8000/api/getlocation"
    df.foreachBatch(lambda batch_df, _: batch_df.toPandas().apply(
        lambda row: requests.post(url, json=row.to_dict(), timeout=3), axis=1))

# 메인 실행
if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Spark Structured Streaming") \
        .master("spark://172.19.0.2:7077") \
        .getOrCreate()

    kafka_ip = "10.0.4.172"
    db_config = {
        "url": "10.0.4.80",
        "user": "airflow",
        "password": "zxcv0987^%",
        "database": "parkingissue"
    }

    kafka_stream = read_from_kafka(spark, kafka_ip)
    processed_stream = calculate_nearby_parkings(kafka_stream, db_config)

    processed_stream.writeStream \
        .foreachBatch(send_to_fastapi) \
        .start() \
        .awaitTermination()

