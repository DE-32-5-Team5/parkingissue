import configparser
from pyspark.sql import SparkSession

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
s3_key = '/app/search.csv'
s3_path = f"s3a://{s3_bucket}/{s3_key}"

try:
    # CSV 파일 읽기
    df = spark.read.csv(s3_path, header=True)
    # 데이터 확인
    df.show()
except Exception as e:
    print(f"Error reading data from S3: {e}")

# SparkSession 종료
spark.stop()

