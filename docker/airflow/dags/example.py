import sys
sys.path.insert(0, '/opt/airflow/dags/code')

from parkinginfo import (
    fun_api_call, fun_branch, fun_remove_log, fun_save_log, 
    fun_trans, fun_load,fun_2parquet
)
from datetime import datetime
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

def create_python_operator(task_id, python_callable,t_rule='all_success'):
    """PythonOperator 생성 함수"""
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        provide_context=True,
        dag=dag,
        trigger_rule=t_rule,
    )

def create_python_operator_op(task_id, python_callable, filename):
    """PythonOperator 생성 함수"""
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        provide_context=True,
        dag=dag,
        op_kwargs={'filename': filename}
    )

def create_branch_operator(task_id, python_callable, filename):
    """BranchPythonOperator 생성 함수"""
    return BranchPythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        dag=dag,
        op_kwargs = {'filename':filename},
    )

# DAG 정의
with DAG(
    dag_id="parking_facility_information",
    schedule_interval='@daily',
    start_date=datetime(2024, 11, 28),
    catchup=False,  # 이전 날짜로 돌아가지 않도록 설정
    tags=["parking", "facility", "information"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # 첫 번째 줄 - API 호출 및 추출 작업
    api_call = create_python_operator('api_call', fun_api_call)
    extract_branch = create_branch_operator('extract_branch', fun_branch, "edata.json")
    extract_empty = EmptyOperator(task_id="extract_empty")
   
    remove_extract_log = create_python_operator_op('remove_extract_log', fun_remove_log, "edata.json")
    save_extract_log = create_python_operator('save_extract_log', fun_save_log,'all_done')

    # 첫 번째 줄 작업 순서: start -> api_call_check -> extract_data_branch -> [remove_extract_log, save_extract_log]
    start >> api_call >> extract_branch
    extract_branch >> [remove_extract_log, extract_empty]
    remove_extract_log >> save_extract_log

    # 두 번째 줄 - 변환 및 적재 작업
    transform = create_python_operator('transform', fun_trans,'all_done')

    transform_branch = create_branch_operator('transform_branch', fun_branch, "tdata.csv")
    transform_empty = EmptyOperator(task_id="transform_empty")
    remove_transform_log = create_python_operator_op('remove_transform_log', fun_remove_log, "tdata.csv")

    save_transform_log = create_python_operator('save_transform_log', fun_2parquet)

    load_data = create_python_operator('load_data', fun_load)

    # 두 번째 줄 작업 순서: save_extract_log -> data_transformation -> transform_data_branch -> [remove_transform_log, save_transform_log] -> connect_to_db -> load_data_to_db -> end
    # save_extract_log >> transform >> transform_branch
    save_extract_log >> transform_branch >> [remove_transform_log, transform_empty]
    remove_transform_log >> transform >> save_transform_log

    save_transform_log >> load_data >> end
