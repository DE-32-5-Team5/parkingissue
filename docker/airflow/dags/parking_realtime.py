ifrom datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

import sys
sys.path.insert(0, '/opt/airflow/dags/code')
from parkingrealtime import (
    fun_conn, fun_rmdir, fun_fetch, fun_2csv, fun_save, fun_s3
)

default_args = {
    'retries': 3,  # 모든 태스크에 기본적으로 3회 재시도
    'retry_delay': timedelta(minutes=5),  # 재시도 간 5분 간격
}


def create_python_operator(task_id, python_callable, value, t_rule='all_success'):
    """PythonOperator 생성 함수"""
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        provide_context=True,
        dag=dag,
        trigger_rule=t_rule,
        op_kwargs={'value': value},
        retries=5,
        retry_delay=timedelta(seconds=30)
    )



with DAG(
    dag_id="parking_realtime",
    #schedule_interval='@monthly',
    schedule_interval='@hourly',
    start_date=datetime(2024, 11, 1),
    catchup=False,  # 이전 날짜로 돌아가지 않도록 설정
    tags=["parking", "real", "time"],

) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    connect = PythonOperator(
        task_id="conn.http",
        python_callable=fun_conn,
        provide_context=True,
        dag=dag,
    )
    #rm_Edir = create_python_operator("rm.Edir", fun_rmdir, "Edata")
    #fetch_data = PythonOperator(
        #task_id="fetch.data",
        #python_callable=fun_fetch,
        #provide_context=True,
        #dag=dag,
    #)

    rm_Tdir = create_python_operator("rm.Tdir",fun_rmdir, "Tdata")
    trans_data = PythonOperator(
        task_id="trans.data",
        python_callable=fun_2csv,
        provide_context=True,
        dag=dag,
    )

    save_task = PythonOperator(
        task_id="save.task",
        python_callable=fun_save,
        provide_context=True,
        dag=dag,
    )

    s3_up_task = PythonOperator(
            task_id="s3.upload",
            python_callable=fun_s3
    )

    spark_task = SSHOperator(
        task_id='spark',
        ssh_conn_id='ssh_spark',  # Airflow의 SSH 연결 ID
        command='sudo docker exec spark-batch-worker /opt/spark/bin/spark-submit --master spark://spark-master:7077 /app/realtime.py',
        dag=dag,
    )

    #start >> connect >> rm_Edir >> fetch_data >> end
    #start >> connect >> rm_Edir >> fetch_data >> rm_Tdir >> trans_data >> s3_up_task >>  save_task >> end
    start >> connect >> rm_Tdir >> trans_data >>  s3_up_task >>  spark_task  >> save_task >>  end
