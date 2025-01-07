import configparser
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, avg
# from datetime import datetime
# import pytz
import pandas
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
    .appName("Simple Spark App") \
    .master("spark://172.18.0.2:7077") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .getOrCreate()

# korea_tz = pytz.timezone("Asia/Seoul")
# now = datetime.now(korea_tz)
# date = now.strftime("%Y%m%d_%H")
times = times = [f"{i:02d}" for i in range(8,21)]
s3_bucket = 'fiveguys-s3'
# s3_key = f'/Real/{date}/'
# s3_path = f"s3a://{s3_bucket}/{s3_key}"

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


def all_time_confusion(s3, time):
    df_list = []

    # 이전에 같은 시간에 대한 혼잡도가 계산된 CSV가 있는지 확인
    prefix = "Real/"
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=prefix)

    print(len(response['Contents']))
    match_dir = []
    for i in response['Contents']:
        # 경로에서 디렉토리 부분만 가져오기
        dir_name = i['Key'].split('/')[1]
        parts = dir_name.split('_')

        # 날짜_시간 형식인지, 시간 확인
        if len(parts) == 2 and parts[1] == time:
            match_dir.append(dir_name)
          
            # 이전 데이터 읽기 및 추가
            for old_dir in match_dir:
                s3_old_path = f"s3a://{s3_bucket}/Real/{old_dir}"
                old_df = spark.read.format("csv") \
                    .option("header", "true") \
                    .option("inferSchema", "true") \
                    .option("delimiter", ";") \
                    .load(s3_old_path)
                old_df.show()
                df_list.append(old_df)
    
    for idx, df in enumerate(df_list):
        # 혼잡도 컬럼 계산, 추가
        df = df.withColumn(
            "confusion",
            when(col("total") > 0, (col("total").cast("float") - col("available").cast("float")) / col("total").cast("float"))
            .otherwise(None)
        )
        confusion_df = df.select("park_id", "confusion")
        confusion_df.show()
        df_list[idx] = confusion_df

    combined_df = df_list[0]
    for df in df_list[1:]:
        combined_df = combined_df.union(df)

    combined_result_df = combined_df.groupBy("park_id") \
    .agg(
        (avg("confusion") * 100).alias(time)  # 평균 계산 후 백분율로 변환
    )

    combined_result_df.show()

    pandas_df = combined_result_df.toPandas()

    # Pandas DataFrame을 CSV로 저장
    output_time_path = f"{time}.csv"
    pandas_df.to_csv(output_time_path, index=False, encoding='utf-8')

    # S3에 업로드
    s3.upload_file(output_time_path, s3_bucket, f"confusion_rate/{output_time_path}")


try:
    s3 = s3_connection(aws_access_key_id, aws_secret_access_key)
    # 08시 부터 20시 까지 각각 전부 통계내서 저장하기
    for time in times:
        all_time_confusion(s3, time)
    # 모든 시간들에 대한 통계들을 합쳐서 하나로 만들기
    s3_confusion_path = f"s3a://{s3_bucket}/confusion_rate/"
    total_df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(s3_confusion_path)
    total_df.show()

    # 혼잡도 csv 최종 파일 생성
    total_pandas_df = total_df.toPandas()
    total_pandas_df.to_csv("total.csv", index=False, encoding='utf-8')
    # s3에 업로드
    s3.upload_file("total.csv", s3_bucket, "total.csv")

except Exception as e:
    print(f"Error reading data from S3: {e}")
finally:
    # SparkSession 종료
    spark.stop()
