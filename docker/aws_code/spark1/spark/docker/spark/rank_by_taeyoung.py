from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Simple Spark App") \
    .master("spark://172.18.0.2:7077") \
    .getOrCreate()

# 샘플 데이터 생성
data = [
    ("Alice", 34),
    ("Bob", 45),
    ("Catherine", 29),
]

# 데이터프레임 생성
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# 데이터프레임 출력
print("Original Data:")
df.show()

# 데이터 변환 예시 (Age 30 이상 필터링)
filtered_df = df.filter(df["Age"] > 30)

# 필터링 결과 출력
print("Filtered Data (Age > 30):")
filtered_df.show()

# 결과를 CSV 파일로 저장
filtered_df.write.csv("/app/filtered_data.csv", header=True)

# SparkSession 종료
spark.stop()

