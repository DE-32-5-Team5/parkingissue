from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

import sys
sys.path.insert(0, '/opt/airflow/dags/code')
from festivalinfo import (
    fun_mkdir,fun_fetch,fun_2csv,fun_save
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

#도메인
#서버 켜놓는 시간
# 디비에 저장해야하는 이유를 기술적으로 설명해서 달라.


# DAG 정의
with DAG(
    dag_id="festival_info",
    schedule_interval='@daily',
    start_date=datetime(2024, 12, 6),
    catchup=False,  # 이전 날짜로 돌아가지 않도록 설정
    tags=["festival", "info"],
    # max_active_tasks=4

) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    with TaskGroup("mkdir", dag=dag) as mkdir_group:
        # mk_HData= create_python_operator('mk.FData', fun_mkdir, "HP")
        mk_Festival= create_python_operator('mk.Region', fun_mkdir, "Festival")
        mk_Food= create_python_operator('mk.Food', fun_mkdir, "Food")
        mk_Festival>>mk_Food


    with TaskGroup("region_group", dag=dag) as fetch_region:
        fetch_festival = create_python_operator('fetch.festival', fun_fetch, "r-festival") #지역기반 관광정보 - 축제공연행사 데이터
        fetch_food = create_python_operator('fetch.Food', fun_fetch, "r-food") #지역기반 관광정보 - 음식점 데이터

    with TaskGroup("mkdir_csv", dag=dag) as mkdir_csv_group:
        mk_Fe_CSV= create_python_operator('mk.fe_csv', fun_mkdir, "Festival_CSV")
        mk_Fo_CSV= create_python_operator('mk.fo_csv', fun_mkdir, "Food_CSV")

    with TaskGroup("2csv_group", dag=dag) as trans_region:
        tocsv_festival = create_python_operator('2csv.festival', fun_2csv, "Festival")
        tocsv_food = create_python_operator('2csv.Food', fun_2csv, "Food")

    with TaskGroup("save_db", dag=dag) as save_group:
        todb_festival = create_python_operator('2db.festival', fun_save, "Festival_CSV")
        todb_food = create_python_operator('2db.Food', fun_save, "Food_CSV")

    start >> mkdir_group >> fetch_region >> mkdir_csv_group >> trans_region>> save_group >>  end