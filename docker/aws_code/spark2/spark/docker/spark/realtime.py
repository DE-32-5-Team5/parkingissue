import configparser
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, avg, reduce
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import boto3

# AWS 자격 증명 파일 경로
aws_credentials_path = "/app/.aws/credentials"

# AWS 자격 증명 읽기
config = configparser.ConfigParser()
config.read(aws_credentials_path)

aws_access_key_id = config["default"]["aws_access_key_id"]
aws_secret_access_key = config["default"]["aws_secret_access_key"]

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Optimized Spark App") \
    .master("spark://172.18.0.2:7077") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.sql.shuffle.partitions", 50) \
    .config("spark.default.parallelism", 100) \
    .getOrCreate()

times = [f"{i:02d}" for i in range(8, 21)]
s3_bucket = 'fiveguys-s3'

# S3 연결 함수
def s3_connection(idkey, secretkey):
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=idkey,
            aws_secret_access_key=secretkey,
        )
        print("S3 bucket connected!")
        return s3
    except Exception as e:
        print(f"S3 connection error: {e}")
        return None

# 혼잡도 계산 함수
def calculate_confusion(df):
    return df.withColumn(
        "confusion",
        when(col("total") > 0, (col("total").cast("float") - col("available").cast("float")) / col("total").cast("float"))
        .otherwise(None)
    ).select("park_id", "confusion")

# 특정 시간대 혼잡도 계산 및 저장
def process_time(s3, time):
    try:
        prefix = "Real/"
        response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=prefix)
        if 'Contents' not in response:
            print(f"No data found for time {time}.")
            return None

        df_list = []
        for obj in response['Contents']:
            dir_name = obj['Key'].split('/')[1]
            parts = dir_name.split('_')
            if len(parts) == 2 and parts[1] == time:
                s3_path = f"s3a://{s3_bucket}/Real/{dir_name}"
                df = spark.read.format("csv") \
                    .option("header", "true") \
                    .option("inferSchema", "true") \
                    .option("delimiter", ";") \
                    .load(s3_path).cache()
                df = calculate_confusion(df)
                df_list.append(df)

        if df_list:
            combined_df = df_list[0]
            for df in df_list[1:]:
                combined_df = combined_df.union(df)

            result_df = combined_df.groupBy("park_id").agg((avg("confusion") * 100).alias(time))
            result_df.show()

            # CSV 저장 및 업로드
            output_time_path = f"{time}.csv"
            result_df.coalesce(1).toPandas().to_csv(output_time_path, index=False, encoding='utf-8')
            s3.upload_file(output_time_path, s3_bucket, f"confusion_rate/{output_time_path}")
        else:
            print(f"No matching data for time {time}.")
    except Exception as e:
        print(f"Error processing time {time}: {e}")

# 병렬 처리 및 전체 데이터 병합
def main():
    try:
        s3 = s3_connection(aws_access_key_id, aws_secret_access_key)
        if not s3:
            return

        # 병렬 처리
        #with ThreadPoolExecutor(max_workers=5) as executor:
        #    executor.map(lambda t: process_time(s3, t), times)

        # 최종 파일 병합
        confusion_df_list = []
        prefix = "confusion_rate/"
        response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=prefix)
        for obj in response['Contents'][1:]:
            file_name = obj['Key'].split('/')[1]
            s3_path = f"s3a://{s3_bucket}/confusion_rate/{file_name}"
            df = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .load(s3_path)
            df.unpersist()
            confusion_df_list.append(df)  # confusion_df_list에 df 추가
        for df in confusion_df_list:
            if "park_id" in df.columns and "08" in df.columns:
                merged_df = df

        for df in confusion_df_list:
            if "08" not in df.columns:
                merged_df = merged_df.join(df, on='park_id', how='left_outer')
                merged_df.show()
                merged_df.printSchema()
        merged_df = merged_df.dropDuplicates(["park_id"])
        total_pandas_df = merged_df.toPandas()
        total_pandas_df.to_csv("total.csv", index=False, encoding='utf-8')
        s3.upload_file("total.csv", s3_bucket, "total.csv")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

