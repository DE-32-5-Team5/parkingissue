#!/bin/bash
set -e

# Spark master 노드 실행
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master &

# Spark worker 노드 실행 (현재 컨테이너를 워커로 사용)
#$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker $SPARK_MASTER_URL &

# 컨테이너가 종료되지 않도록 대기
tail -f /dev/null

