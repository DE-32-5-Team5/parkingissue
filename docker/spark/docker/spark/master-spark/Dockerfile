# 1. Spark 기반 이미지 사용
# python 3.10 고정인듯..
FROM apache/spark:3.5.1-scala2.12-java17-python3-ubuntu

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. root 사용자로 권한 설정
USER root

# 4. 필요한 패키지 설치
RUN rm -rf /var/lib/apt/lists/* && apt-get clean && apt-get update && apt-get install -y \
    curl \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Spark 관련 환경 변수 설정
ENV SPARK_HOME=/opt/spark
# master 포트 바꾸면 아래 EXPOSE랑 master-worker 연결할때 포트도 바꿔줘야함
ENV SPARK_MASTER_URL=spark://spark-master:7077
ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3

# 6. 포트 노출
# 순서대로 worker, master, ui
EXPOSE 4040 7077 8080

# 7. Spark UI를 시작하는 스크립트 복사
COPY start-spark.sh /app/start-spark.sh
RUN chmod +x /app/start-spark.sh

# 8. Entrypoint 설정
ENTRYPOINT ["/app/start-spark.sh"]

