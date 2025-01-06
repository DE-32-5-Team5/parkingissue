import os
import json
import time
import pandas as pd
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.ssh.operators.ssh import SSHOperator


from airflow.operators.python import (
        PythonOperator,
        PythonVirtualenvOperator,
        BranchPythonOperator
)

import sys
sys.path.insert(0, '/opt/airflow/dags/code')

from ranking import (
    fun_con, fun_s3, fun_from_s3
)

with DAG(
    'rank',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': True,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3),
    },
    #max_active_runs=1,
    #max_active_tasks=3,
    description='Real-time search term ranking',
    schedule_interval='@hourly',
    start_date=datetime(2024, 12, 23),
    catchup=False,
    tags=['search','rank'],

) as dag:
    start=EmptyOperator(task_id='start')
    end=EmptyOperator(task_id='end')



    kafka_task = PythonOperator(
            task_id="kafka",
            python_callable=fun_con,
    )

    s3_up_task = PythonOperator(
            task_id="s3.upload",
            python_callable=fun_s3
    )

    spark_task = SSHOperator(
        task_id='spark',
        ssh_conn_id='ssh_spark',  # Airflow의 SSH 연결 ID
        command='sudo docker exec spark-batch-worker /opt/spark/bin/spark-submit --master spark://spark-master:7077 /app/rank.py',
        #params={"arg1": "example_value"},
        dag=dag,
    )

    #s3_down_task = PythonOperator(
            #task_id='s3.download',
            #python_callable=fun_from_s3
    #)

    start >> kafka_task >> s3_up_task >> spark_task >>  end
