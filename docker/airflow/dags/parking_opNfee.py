from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

import sys
sys.path.insert(0, '/opt/airflow/dags/code')
from opNfee import (
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



# DAG 정의
with DAG(
    dag_id="parking_operate_fee",
    schedule_interval='@monthly',
    start_date=datetime(2024, 11, 28),
    catchup=False,  # 이전 날짜로 돌아가지 않도록 설정
    tags=["parking", "operator", "fee"],
    max_active_tasks=4

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
    with TaskGroup("fetch_group", dag=dag) as fetch_group:
            fetch_5 = create_python_operator("fetch.5", fun_fetch, 1)
            fetch_10 = create_python_operator("fetch.10", fun_fetch, 501)
            fetch_15 = create_python_operator("fetch.15", fun_fetch, 1001)
            fetch_20 = create_python_operator("fetch.20", fun_fetch,1501)

    rm_Tdir = create_python_operator("rm.Tdir",fun_rmdir, "Tdata")
    with TaskGroup("csv_group", dag=dag) as csv_group:
        to_csv_5 = create_python_operator("2csv.5", fun_2csv, 1)
        to_csv_10 = create_python_operator("2csv.10", fun_2csv, 501)
        to_csv_15 = create_python_operator("2csv.15", fun_2csv, 1001)
        to_csv_20 = create_python_operator("2csv.20", fun_2csv,1501)

    rm_Pdir = create_python_operator("rm.Pdir",fun_rmdir, "Pdata")
    # with TaskGroup("parquet_group", dag=dag) as parquet_group:
    #     to_parquet_5 = create_python_operator("2parquet.5", fun_2parquet, 1)
    #     to_parquet_10 = create_python_operator("2parquet.10", fun_2parquet, 501)
    #     to_parquet_15 = create_python_operator("2parquet.15", fun_2parquet, 1001)
    #     to_parquet_20 = create_python_operator("2parquet.20", fun_2parquet,1501)

    to_parquet = PythonOperator(
        task_id="save.parquet",
        python_callable=fun_2parquet,
        provide_context=True,
        dag=dag,
    )

    save_DB = PythonOperator(
        task_id="save.task",
        python_callable=fun_save,
        provide_context=True,
        dag=dag,
    )

    start >> connect >> rm_Edir
    rm_Edir >> fetch_group >> rm_Tdir
    rm_Tdir >> csv_group >> rm_Pdir
    rm_Pdir >> to_parquet >> save_DB >> end
