#!/bin/bash
set -e

# Spark master 노드 실행
#$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master &

# Spark worker 노드 실행 (현재 컨테이너를 워커로 사용)
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker $SPARK_MASTER_URL &

# 필요한 시간 대기 (마스터가 준비될 때까지)
sleep 10

# Spark-submit 명령어 실행
#$SPARK_HOME/bin/spark-submit \
#  --conf spark.sql.warehouse.dir=/tmp/spark-warehouse \
#  --executor-cores 1 
#  --master $SPARK_MASTER_URL \
#  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 \
#  /app/sample.py

# 컨테이너가 종료되지 않도록 대기
tail -f /dev/null
