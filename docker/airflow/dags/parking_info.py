from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

import sys
sys.path.insert(0, '/opt/airflow/dags/code')
from parkinginfo import (
    fun_conn, fun_rmdir, fun_fetch, fun_2csv, fun_2parquet, fun_save
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
    dag_id="parking_facility_information",
    schedule_interval='@monthly',
    start_date=datetime(2024,11, 1),
    catchup=True,  # 이전 날짜로 돌아감
    tags=["parking", "facility", "information"],

) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    connect = PythonOperator(
        task_id="conn.http",
        python_callable=fun_conn,
        provide_context=True,
        dag=dag,
    )
    rm_Edir = create_python_operator("rm.Edir", fun_rmdir, "Edata")
    fetch_data = PythonOperator(
        task_id="fetch.data",
        python_callable=fun_fetch,
        provide_context=True,
        dag=dag,
    )
    rm_Tdir = create_python_operator("rm.Tdir",fun_rmdir, "Tdata")
    with TaskGroup("csv_group", dag=dag) as csv_group:
        to_csv_5 = create_python_operator("2csv.5", fun_2csv, 1)
        to_csv_10 = create_python_operator("2csv.10", fun_2csv, 501)
        to_csv_15 = create_python_operator("2csv.15", fun_2csv, 1001)
        to_csv_20 = create_python_operator("2csv.20", fun_2csv,1501)

    rm_Pdir = create_python_operator("rm.Pdir",fun_rmdir, "Pdata")
    with TaskGroup("parquet_group", dag=dag) as parquet_group:
        to_parquet_5 = create_python_operator("2parquet.5", fun_2parquet, 1)
        to_parquet_10 = create_python_operator("2parquet.10", fun_2parquet, 501)
        to_parquet_15 = create_python_operator("2parquet.15", fun_2parquet, 1001)
        to_parquet_20 = create_python_operator("2parquet.20", fun_2parquet,1501)

    with TaskGroup("svae_group", dag=dag) as save_group:
        to_save_5 = create_python_operator("save.5", fun_save, 1)
        to_save_10 = create_python_operator("save.10", fun_save, 501)
        to_save_15 = create_python_operator("save.15", fun_save, 1001)
        to_saev_20 = create_python_operator("save.20", fun_save,1501)

    start >> connect >> rm_Edir
    rm_Edir >> fetch_data >> rm_Tdir
    rm_Tdir >> csv_group >> rm_Pdir
    rm_Pdir >> parquet_group >> save_group
    save_group >> end
