import os
import json
import pandas as pd
import time
from datetime import datetime
import requests
import re
import shutil
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from mysql.connector import Error
import mysql.connector
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

session = requests.Session()

def fun_conn():
    retry = Retry(
        total=5,  # 재시도 횟수
        backoff_factor=1,  # 재시도 간의 대기 시간
        status_forcelist=[500, 502, 503, 504, 408],  # 재시도할 상태 코드
        method_whitelist=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    result = call(1,1)
    if result.get('resultMsg') == 'SUCCESS':
            print("------연결에 성공했습니다-------")
            return True
    else:
        print("------연결에 실패했습니다-------")
        raise

def fun_rmdir(**kwargs):
    dirname = kwargs['value'] #Edata
    base_path = "/opt/airflow/Data/REAL"
    dir_path = os.path.join(base_path, dirname)

    if os.path.exists(base_path):
        # base_path는 존재하지만 Edata 폴더가 없으면 생성
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print(f" ##### '{dirname}' 폴더가 생성되었습니다.")
        else:
            # Edata 폴더가 존재하면 삭제
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)
            print(f" ##### '{dirname}' 폴더 삭제 후 다시 생성되었습니다.")
    else:
        # base_path가 없으면 REAL 폴더를 먼저 생성하고 Edata도 생성
        # os.makedirs(base_path)
        os.mkdir(base_path)
        os.mkdir(dir_path)
        print(f" #####'{base_path}'와 '{dirname}' 폴더가 생성되었습니다.")


def call(pageno, numOfrow):
    API_KEY = os.getenv('API_KEY')

    url = 'http://apis.data.go.kr/B553881/Parking/PrkRealtimeInfo'
    params ={'serviceKey' : API_KEY,
             'pageNo' : pageno,
             'numOfRows' : numOfrow,
             'format' : '2'
             }

    attempt = 0  # 시도 횟수
    while True:
        if attempt==5:
            print("최대 재시도 횟수를 초과하였습니다. 30분 후 다시 시도합니다.")
            time.sleep(1800)
            attempt=0


        try:
            response = session.get(url, params=params)

            # 응답 상태 코드 확인
            if response.status_code == 200:

                # 본문이 비어 있으면 재시도
                if not response.text.strip():
                    print("응답 본문이 비어있습니다. 재시도 중...")
                    attempt += 1

                # JSON 파싱 오류 발생 시 재시도
                try:
                    data = response.json()
                    return data
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                    print("응답 본문:", response.text)
                    attempt += 1
                    continue

            # 상태 코드가 200이 아니면 재시도
            else:
                print(f"응답 상태 코드 오류: {response.status_code}")
                attempt += 1
                continue

        # 요청 오류 발생 시 재시도
        except requests.exceptions.RequestException as e:
            print(f"요청 예외 발생: {e}")
            attempt += 1
            continue


def fun_fetch():
    dir_path = "/opt/airflow/Data/REAL/Edata"
    totalcnt = 16620 #1
    currentcnt = 300 #0
    pagenum = 4 #1
    First = False ##True

    while currentcnt < totalcnt:
        json_data = []
        file_path = os.path.join(dir_path, f"page_{pagenum}.json")
        data = call(pagenum, 100)
        print(f" ######### page_{pagenum}")
        json_data.append(data)

        if First:
            totalcnt = int(data['totalCount'])
            # totalcnt = 30
            First = False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("파일에 내용이 성공적으로 작성되었습니다.")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")

        currentcnt += int(data['numOfRows'])
        pagenum += 1
        time.sleep(5)

def fun_2csv():
    import random
    json_dir_path = "/opt/airflow/Data/REAL/Edata"
    csv_dir_path = "/opt/airflow/Data/REAL/Tdata"
    dummy = True

    if os.path.exists(json_dir_path):
        files = os.listdir(json_dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))

        for file in files:
            file_path = os.path.join(json_dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            page_no = data.get('pageNo')
            flattened_data = []
            for prk_data in data['PrkRealtimeInfo']:
                flattened_data.append({
                    'available': prk_data.get('pkfc_Available_ParkingLots_total', ' ') ,
                    'total': prk_data.get('pkfc_ParkingLots_total', ' '),
                    'park_id': prk_data.get('prk_center_id', ' '),
                })

            if dummy:
                random_number = random.randint(0, 30)  # 1부터 30까지의 랜덤 정수
                flattened_data.append({
                    'available':  random_number,
                    'total': 30,
                    'park_id': 'T01-00000-00001',
                })

                random_number = random.randint(0, 15)
                flattened_data.append({
                    'available':  random_number,
                    'total': 15,
                    'park_id': 'T01-00000-00002',
                })
                dummy=False


            # pandas DataFrame으로 변환
            df = pd.DataFrame(flattened_data)

            csv_path = os.path.join(csv_dir_path, f"page_{page_no}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
            print(f" page_{page_no}.csv ------ > CSV 파일이 성공적으로 저장되었습니다")
    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return

def fun_save():
    dir_path = "/opt/airflow/Data/REAL/Tdata"

    try:
        # 환경변수에서 비밀번호 가져오기
        passwd = os.getenv('DB_PW')

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host="10.0.4.80",
            port=6033,
            user="root",
            password=passwd,
            database="parkingissue"
        )

        if conn.is_connected():
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")

        cursor = conn.cursor()

        files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
        files_sort = sorted([f for f in files], key=lambda x: int(x.split('_')[-1].split('.')[0]))

        for file in files_sort:
            print(f" ////// {file} 처리 시작 ")

            file_path = os.path.join(dir_path, file)
            df = pd.read_csv(file_path, sep=';')

            for _, row in df.iterrows():
                park_id = row['park_id'] if pd.notna(row['park_id']) else ""
                park_total = row['total'] if pd.notna(row['total']) else -1
                park_available = row['available'] if pd.notna(row['available']) else -1

                #주차장 정보 없으면 Pass
                query = "SELECT * FROM parkingarea_info WHERE park_id = %s;"
                cursor.execute(query, (park_id,))
                result = cursor.fetchone()
                if not result:
                    continue

                select_query = "SELECT * FROM parkingarea_realtime WHERE park_id = %s;"
                cursor.execute(select_query, (park_id,))  # 쿼리 실행
                result = cursor.fetchall()
                if result:
                    update_query =f"""
                    UPDATE parkingarea_realtime
                    SET
                        park_total = %s,
                        park_available = %s
                    WHERE park_id = %s;
                    """
                    cursor.execute(update_query, (park_total, park_available, park_id))
                    print(f"ID {park_id} 업데이트 성공")

                else:
                    insert_query = f"""
                        INSERT INTO parkingarea_realtime (park_id, park_total, park_available)
                        VALUES (%s, %s, %s);
                    """
                    cursor.execute(insert_query, (park_id, park_total, park_available))
                    print(f"ID {park_id} 데이터 삽입 성공")

            # 변경 사항 커밋
            conn.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")


def fun_s3_tmp():
    """
    로컬 CSV 파일을 S3 버킷에 업로드합니다.
    - bucket_name: S3 버킷 이름
    - file_key: S3에 저장될 파일 경로
    - file_path: 로컬 CSV 파일 경로
    """
    try:
        s3_hook = S3Hook(aws_conn_id='aws_default')
        s3_hook.load_file(
            filename='/opt/airflow/Data/REAL/Tdata',
            key='Real/',
            bucket_name='fiveguys-s3',
            replace=True
        )
        print("s3 업로드 성공.")

    except Exception as e:
        print(f"s3 업로드 중 문제 발생 : {e}")

def fun_s3():
    """
    로컬 디렉토리 내 모든 파일을 S3 버킷에 업로드합니다.
    - bucket_name: S3 버킷 이름
    - prefix: S3에 저장될 파일의 경로(prefix)
    - directory_path: 로컬 디렉토리 경로
    """
    from datetime import datetime, timezone, timedelta

    try:
        bucket_name = 'fiveguys-s3'
        # 현재 날짜와 시간을 폴더 이름으로 사용
        # 현재 UTC 시간
        utc_now = datetime.now(timezone.utc)

        # 한국 시간 (UTC+9)으로 변환
        kst_now = utc_now + timedelta(hours=9)

        # 원하는 포맷으로 출력
        current_datetime = kst_now.strftime("%Y%m%d_%H")

        #current_datetime = datetime.now().strftime("%Y%m%d_%H")
        prefix = f"Real/{current_datetime}/"  # S3 내 저장될 경로
        directory_path = '/opt/airflow/Data/REAL/Tdata'

        # S3 연결
        s3_hook = S3Hook(aws_conn_id='aws_default')

        # 디렉토리 내 파일 순회
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                s3_key = os.path.join(prefix, file_name)  # S3 내 경로 설정

                # 파일 업로드
                s3_hook.load_file(
                    filename=file_path,
                    key=s3_key,
                    bucket_name=bucket_name,
                    replace=True
                )
                print(f"업로드 성공: {file_path} -> s3://{bucket_name}/{s3_key}")

    except Exception as e:
        print(f"s3 업로드 중 문제 발생 : {e}")
