import configparser
from pyspark.sql import SparkSession
import pandas
import boto3
import shutil
import os

# AWS 자격 증명 파일 경로
aws_credentials_path = "/app/.aws/credentials"

# AWS 자격 증명 읽기
config = configparser.ConfigParser()
config.read(aws_credentials_path)

aws_access_key_id = config["default"]["aws_access_key_id"]
aws_secret_access_key = config["default"]["aws_secret_access_key"]

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Simple Spark App") \
    .master("spark://172.18.0.2:7077") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .getOrCreate()

s3_bucket = 'fiveguys-s3'
s3_key = '/search/search.csv'
s3_path = f"s3a://{s3_bucket}/{s3_key}"

def s3_connection(idkey, secretkey):
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=idkey,
            aws_secret_access_key=secretkey,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

try:
    # CSV 파일 읽기
    df = spark.read.csv(s3_path, header=True)
    # 데이터 확인
    df.groupBy("search_msg") \
    .agg({"search_msg": "count"}) \
    .withColumnRenamed("count(search_msg)", "count") \
    .orderBy("count", ascending=False) \
    .limit(10) \
    .select("search_msg") \
    .show()
    
    pandas_df = df.toPandas()

    # Pandas DataFrame을 CSV로 저장
    output_path = "/app/rank.csv"
    pandas_df.to_csv(output_path, index=False, encoding='utf-8')
    
    # S3에 업로드
    s3 = s3_connection(aws_access_key_id, aws_secret_access_key)
    s3.upload_file("/app/rank.csv", s3_bucket, "rank.csv")

except Exception as e:
    print(f"Error reading data from S3: {e}")

# SparkSession 종료
spark.stop()

