import os
import json
import csv
import pandas as pd
import json
import time
import requests
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



def fun_api_call():
    API_KEY = os.getenv('API_KEY')
   
    if not API_KEY:
        print("API_KEY is not set or is empty. Please check your environment variables.")

    # API_KEY가 유효한지 확인
    url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    params ={'serviceKey' : API_KEY, 
             'pageNo' : 1, 
             'numOfRows' : '1', 
             'format' : '2'
             }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('resultMsg') == 'SUCCESS':
            print("API Key is valid.")
            return True
        else:
            print(f"Error !!!\n{data}")
            return False
        
    except json.decoder.JSONDecodeError:
        print("Failed to decode JSON response.")
        root = ET.fromstring(response.content)
        error_msg = root.find('.//returnAuthMsg')
        print("*"*3000)
        print(error_msg.text)
        print("*"*3000)
        return False

    
def fun_branch(*args, **kwargs):
    dir_path = f"/opt/airflow"
    dir = kwargs.get('dir')
    path = os.path.join(dir_path, dir)
    

    print(f"*****************  {path}")
    if os.path.exists(path):
        if "Edata" in path:
            print(f"{path} 폴더가 존재합니다.") 
            return 'remove_extract_log'  
        else:
            print(f"{path} 폴더가 존재합니다.") 
            return 'remove_transform_log'
        
    else: #폴더가 없음
        if "Edata" in path:
            print(f"{path} 폴더가 존재하지 않습니다.")
            return 'extract_empty'  
        else:
            print(f"{path} 폴더가 존재하지 않습니다.")
            return 'transform_empty'


def fun_remove_log(**kwargs):
    dir_path = "/opt/airflow"
    dirname = kwargs['dir']
    path = f"{dir_path}/{dirname}"
    try:
        shutil.rmtree(path)
        print(f"{path} 폴더가 삭제되었습니다.")
    except OSError as e:
        print(f"오류 발생: {e}")


def fun_save_log():
    dir_path = "/opt/airflow/Edata/"
    # filename = "edata.json"

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"{dir_path} 디렉토리가 생성되었습니다.")
        else:
            print(f"{dir_path} 디렉토리가 이미 존재합니다.")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")
    
    # 파일 경로 설정
    # file_path = os.path.join(dir_path, filename)

    API_KEY = os.getenv('API_KEY')

    totalcnt = 1
    currentcnt = 0
    pagenum = 1
    First = True
    

    while currentcnt < totalcnt:
        # json_data = []
        filename = f"page_{pagenum}.json"
        file_path = os.path.join(dir_path, filename)

        data = call(pagenum, API_KEY)

        print(f" #### PAGE {data['pageNo']}")
        # print(data)
        # json_data.append(data)

        if First:
            totalcnt = int(data['totalCount']) 
            # totalcnt = 10
            First = False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("파일에 내용이 성공적으로 작성되었습니다.")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")
   
        currentcnt += int(data['numOfRows'])
        pagenum += 1
        time.sleep(1) 



def fun_trans():
    csv_dir_path = "/opt/airflow/Tdata"
    try:
        if not os.path.exists(csv_dir_path):
            os.makedirs(csv_dir_path)
            print(f"{csv_dir_path} 디렉토리가 생성되었습니다.")
        else:
            print(f"{csv_dir_path} 디렉토리가 이미 존재합니다.")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")
    

    json_dir_path = "/opt/airflow/Edata/"
    try:
        if os.path.exists(json_dir_path):
            files = os.listdir(json_dir_path)
            files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
            
            for file in files:
                file_path = os.path.join(json_dir_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                flattened_data = []
                page_no = data['pageNo']
                for prk_data in data['PrkSttusInfo']:
                    print(prk_data)
                    flattened_data.append({
                        'park_id': prk_data.get('prk_center_id', ' ') ,
                        'park_nm': prk_data.get('prk_plce_nm', ' '),
                        'park_addr': prk_data.get('prk_plce_adres', ' '),
                        'park_la': prk_data.get('prk_plce_entrc_la', ' '),
                        'park_lo': prk_data.get('prk_plce_entrc_lo', ' '),
                        'page_no': page_no
                    })

                # pandas DataFrame으로 변환
                df = pd.DataFrame(flattened_data)
                csv_file_path = os.path.join(csv_dir_path, f"page_{page_no}.csv")       
                # CSV 파일로 저장
                df.to_csv(csv_file_path, index=False, encoding='utf-8', sep=';')
                print(f"CSV 파일이 성공적으로 저장되었습니다: {csv_file_path}")
        else:
            print(f"경로에 파일이 존재하지 않습니다.")
            return
    except Exception as e:
        print(f"파일 읽는 중 오류 발생: {e}")
        return


def fun_2parquet():
    p_dir_path = "/opt/airflow/Pdata"

    # 디렉토리 삭제
    try:
        if os.path.exists(p_dir_path):
            shutil.rmtree(p_dir_path)
            print("Pdata 디렉토리 삭제 완료")
        else:
            print("Pdata 디렉토리가 존재하지 않습니다.")
    except Exception as e:
        print(f"디렉토리 삭제 중 오류 발생: {e}")

    # 디렉토리 생성
    try:
        os.makedirs(p_dir_path)
        print("Pdata 디렉토리 생성 완료")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")

    dir_path = "/opt/airflow/Tdata/"
    files = os.listdir(dir_path)
    files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
    
    for file in files:
        path = os.path.join(dir_path, file)
        df = pd.read_csv(path, delimiter=';')
        output_file = f"{p_dir_path}/{file.split('.')[0]}.parquet"
        df.to_parquet(output_file, index=False)
        print(f"Page {file.split('.')[0]} 데이터가 {output_file}로 저장되었습니다.")
        


def fun_load(**kwargs):
    import glob
    from mysql.connector import Error
    import mysql.connector

    try:
        passwd = os.getenv('DB_PW')

        conn = mysql.connector.connect(
            host="parkingissue_database",
            port=3306,
            user="root",
            password=passwd,
            database="parkingissue"
        )

        if conn.is_connected():
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM parkingarea_info;"
        cursor.execute(delete_query)
        alter_query = "ALTER TABLE parkingarea_info AUTO_INCREMENT = 1;"
        cursor.execute(alter_query)

    except Error as e:
        print(f"테이블 초기화 오류 발생!! {e}")

    folder_path = '/opt/airflow/Pdata'
    parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))
    parquet_files.sort(key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group()))

    for file in parquet_files:
        try:
            if os.path.exists(file) and os.path.isfile(file):
                df = pd.read_parquet(file)
                if not df.empty:
                    insert_query = """
                    INSERT INTO parkingarea_info (park_id, park_nm, park_addr, park_la, park_lo, page_no) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    data = [tuple(x) for x in df[['park_id', 'park_nm', 'park_addr', 'park_la', 'park_lo', 'page_no']].values]
                    cursor = conn.cursor()
                    cursor.executemany(insert_query, data)
                    conn.commit()
                    print(f"{len(data)}개의 데이터가 삽입되었습니다.")
            kwargs['ti'].xcom_push(key='final', value='Success')
        except Exception as e:
            print(f"파일 {os.path.basename(file)}을(를) 읽는 중 오류 발생: {e}")
            kwargs['ti'].xcom_push(key='final', value='Fail')

    if conn.is_connected():
        cursor.close()
        conn.close()
        print("DB connection closed.")


def fun_final(**kwargs):
    ti = kwargs['ti']
    final_result = ti.xcom_pull(key='final', task_ids='load_data')
    print("-" * 50)
    print(f"최종 실행 결과는 !! {final_result}")

    dir_path = "/opt/airflow/Result"
    file_path = f"{dir_path}/result.csv"

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"{dir_path} 디렉토리가 생성되었습니다.")
        else:
            print(f"{dir_path} 디렉토리가 이미 존재합니다.")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")

    header = ['date', 'result']
  
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  
        print(f"새로운 파일 생성 및 헤더 추가됨: {file_path}")

    airflow_execution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_data = [airflow_execution_date, final_result]

    with open(file_path, mode='r+', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # 파일이 비어있거나 헤더만 있는 경우, 데이터 추가
        if len(rows) == 1:  # 헤더만 있는 경우
            with open(file_path, mode='a', newline='', encoding='utf-8') as file_append:
                writer = csv.writer(file_append)
                writer.writerow(new_data)  
            print(f"헤더만 존재, 새로운 행이 추가되었습니다: {new_data}")
        
        # 파일에 마지막 행이 있는 경우
        elif len(rows) > 1:
            last_row = rows[-1]
            if last_row[0] <= airflow_execution_date:  # 마지막 행의 'date'가 에어플로우 실행 날짜보다 같거나 이전인 경우
                with open(file_path, mode='a', newline='', encoding='utf-8') as file_append:
                    writer = csv.writer(file_append)
                    writer.writerow(new_data)  # 새로운 데이터 추가
                print(f"새로운 행이 추가되었습니다: {new_data}")
            else:
                print(f"에러: 'date' 값이 에어플로우 실행 날짜({airflow_execution_date})보다 미래입니다.")

        

session = requests.Session()

# Retry 설정 (최대 5번 재시도, 백오프 시간 1초)
retry = Retry(
    total=5,  # 재시도 횟수
    backoff_factor=1,  # 재시도 간의 대기 시간 (1초, 2초, 4초, 8초, ...)
    status_forcelist=[500, 502, 503, 504, 408],  # 재시도할 상태 코드
    method_whitelist=["GET"]  # GET 요청에만 적용
)
    # 세션에 어댑터 설정
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def call(pagenum,API_KEY):
    import requests
    import json

    url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    params ={'serviceKey' : API_KEY, 
             'pageNo' : pagenum, 
             'numOfRows' : '1000', 
            #  'numOfRows' : '3', 
             'format' : '2'
             }

    attempt = 0  # 시도 횟수

    while attempt < 10:
        try:
            # 요청 보내기
            response = session.get(url, params=params)

            # 응답 상태 코드 확인
            if response.status_code == 200:
                # 응답 본문이 비어 있는지 확인
                if not response.text.strip():  # 공백이나 빈 문자열인 경우
                    print("응답 본문이 비어있습니다. 재시도 중...")
                    attempt += 1
                    continue  # 본문이 비어 있으면 재시도

                # JSON 파싱 시도
                try:
                    data = response.json()  # JSON 파싱
                    return data
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                    print("응답 본문:", response.text)  # 디버깅을 위한 응답 출력
                    attempt += 1
                    continue  # JSON 파싱 오류 발생 시 재시도

            else:
                print(f"응답 상태 코드 오류: {response.status_code}")
                attempt += 1
                continue  # 상태 코드가 200이 아니면 재시도

        except requests.exceptions.RequestException as e:
            print(f"요청 예외 발생: {e}")
            attempt += 1
            continue  # 요청 오류 발생 시 재시도

    # 재시도 후에도 실패하면 None 반환
    print("최대 재시도 횟수를 초과하였습니다. 실패.")
    return None