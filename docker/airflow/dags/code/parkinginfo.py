import os
import json
import csv
import pandas as pd
import json
import time
import requests
import re
import shutil
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
def call(pageno, numOfrow):
    API_KEY = os.getenv('API_KEY')

    url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    params ={'serviceKey' : API_KEY, 
             'pageNo' : pageno, 
             'numOfRows' : numOfrow, 
             'format' : '2'
             }

    attempt = 0  # 시도 횟수
    while True:
        if attempt==10:
            print("최대 재시도 횟수를 초과하였습니다. 10분 후 다시 시도합니다.")
            time.sleep(600)
            # session = requests.Session()
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

def fun_rmdir(**kwargs):
    dirname = kwargs['value'] #Edata
    base_path = "/opt/airflow/Data/Info"
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
        # base_path가 없으면 OP 폴더를 먼저 생성하고 Edata도 생성
        # os.makedirs(base_path) 
        os.mkdir(base_path) 
        os.mkdir(dir_path)
        print(f" #####'{base_path}'와 '{dirname}' 폴더가 생성되었습니다.")

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



def fun_fetch(**kwargs):
    startpage = kwargs['value'] #1,501,1001,1501 1708
    # print(f" %%%%%     {startpage}")
    dir_path = "/opt/airflow/Data/Info/Edata"

    First = True
    total=0
    rownum=-1

    for page in range(startpage, startpage+500):

        file_path = os.path.join(dir_path, f"page_{page}.json") 
        # data = call(page, 15)
        data = call(page, 1000)
        if First:
            total = int(data['totalCount'])
            rownum = int(data['numOfRows'])
            First=False
        print(f" ######### page_{page}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("파일에 내용이 성공적으로 작성되었습니다.")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")
            
        if page*rownum > total:
            break

def fun_2csv(**kwargs):
    startpage = kwargs['value']
    json_dir_path = "/opt/airflow/Data/Info/Edata"
    csv_dir_path = "/opt/airflow/Data/Info/Tdata"

    if os.path.exists(json_dir_path):
        files = os.listdir(json_dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
        print(files[startpage-1:startpage+10-1])
        # print(files[startpage-1:startpage+500-1])

        for file in files:
            # file = Edata/page_1.json
           
            file_path = os.path.join(json_dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            page_no = data.get('pageNo')
            
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
    
            csv_path = os.path.join(csv_dir_path, f"page_{page_no}.csv")         
            df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
            print(f" page_{page_no}.csv ------ > CSV 파일이 성공적으로 저장되었습니다")
    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return


def fun_2parquet():
    dir_path = "/opt/airflow/Tdata/"
    p_dir_path = "/opt/airflow/Pdata"

    try:
        os.makedirs(p_dir_path, exist_ok=True)
        print("Pdata 디렉토리 생성 완료")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")

    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
        
        for file in files:
                path = os.path.join(dir_path, file)
                try:
                    df = pd.read_csv(path, delimiter=';')
                    output_file = f"{p_dir_path}/{file.split('.')[0]}.parquet"
                    df.to_parquet(output_file, index=False)
                    print(f"Page {file.split('.')[0]} 데이터가 {output_file}로 저장되었습니다.")
                except Exception as e:
                    print(f"파일 {file} 처리 중 오류 발생: {e}")
        
    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return
    
def fun_save(**kwargs):
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
    
   