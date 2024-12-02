import sys
sys.path.insert(0, '/opt/airflow/dags/code')

from my_python import my_task
from datetime import datetime


from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.utils.trigger_rule import TriggerRule




with DAG(
    dag_id="parking_facility_information",
    schedule_interval='@daily',
    start_date=datetime(2024, 11, 28),
    catchup=False, #이전 날짜로 돌아가지 않도록 설정
    tags=["parking","facility","information"],
) as dag:
    
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    
    python_task = PythonOperator(
        task_id='python_task',
        python_callable=my_task,
        dag=dag,
        provide_context=True,
    )

    start >> python_task >> end