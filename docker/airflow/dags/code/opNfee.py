import os
import re
import json
import time
import shutil
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

def call(pageno, numOfrow):
    API_KEY = os.getenv('API_KEY')

    url = 'http://apis.data.go.kr/B553881/Parking/PrkOprInfo'
    params ={'serviceKey' : API_KEY, 
             'pageNo' : pageno, 
             'numOfRows' : numOfrow, 
             'format' : '2'
             }
    response = requests.get(url, params=params)

    attempt = 0  # 시도 횟수
    while True:
        if attempt==10:
            print("최대 재시도 횟수를 초과하였습니다. 10분 후 다시 시도합니다.")
            time.sleep(600)
            session = requests.Session()
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
    base_path = "/opt/airflow/OP"
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
        os.makedirs(base_path)  
        os.mkdir(dir_path)
        print(f" #####'{base_path}'와 '{dirname}' 폴더가 생성되었습니다.")

def fun_fetch(**kwargs):
    startpage = kwargs['value']
    dir_path = "/opt/airflow/OP/Edata"
    
    First = True
    total=0
    for page in range(startpage, startpage+10):
        if page > total:
            break
        file_path = os.path.join(dir_path, f"page_{page}.json")
        data = call(page, 10)
        # data = call(page, 1000)
        print(f" ######### {page}")
        if First:
            total = int(data['totalCount'])
            First=False
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("파일에 내용이 성공적으로 작성되었습니다.")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")

   
def fun_2csv(**kwargs):
    startpage = kwargs['value']
    json_dir_path = "/opt/airflow/OP/Edata"
    csv_dir_path = "/opt/airflow/OP/Tdata"

    if os.path.exists(json_dir_path):
        files = os.listdir(json_dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
        print(files[startpage-1:startpage+10-1])
        # print(files[startpage-1:startpage+500-1])

        for file in files:
            page_no = prk_data.get('pageNo')
            file_path = os.path.join(json_dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            opertime_data = []
            fee_data =[]
            for prk_data in data['PrkOprInfo']:
                print(f" ** {prk_data}")
                opertime_data.append({
                    'park_id': prk_data.get('prk_center_id', ' ') ,
                    'mon_opentime' : prk_data.get('Monday', {}).get('opertn_start_time',' '),
                    'mon_closetime' : prk_data.get('Monday', {}).get('opertn_end_time',' '),
                    'tue_opentime' : prk_data.get('Tuesday', {}).get('opertn_start_time',' '),
                    'tue_closetime' : prk_data.get('Tuesday', {}).get('opertn_end_time',' '),
                    'wed_opentime' : prk_data.get('Wednesday', {}).get('opertn_start_time',' '),
                    'wed_closetime' : prk_data.get('Wednesday', {}).get('opertn_end_time',' '),
                    'thu_opentime' : prk_data.get('Thursday', {}).get('opertn_start_time',' '),
                    'thu_closetime' : prk_data.get('Thursday', {}).get('opertn_end_time',' '),
                    'fri_opentime' : prk_data.get('Friday', {}).get('opertn_start_time',' '),
                    'fri_closetime' : prk_data.get('Friday', {}).get('opertn_end_time',' '),
                    'sat_opentime' : prk_data.get('Saturday', {}).get('opertn_start_time',' '),
                    'sat_closetime' : prk_data.get('Saturday', {}).get('opertn_end_time',' '),
                    'sun_opentime' : prk_data.get('Sunday', {}).get('opertn_start_time',' '),
                    'sun_closetime' : prk_data.get('Sunday', {}).get('opertn_end_time',' '),
                    'holi_opentime' : prk_data.get('Holiday', {}).get('opertn_start_time',' '),
                    'holi_closetime' : prk_data.get('Holiday', {}).get('opertn_end_time',' '),
                    
                })

                fee_data.append({
                    'park_id': prk_data.get('prk_center_id', ' ') ,
                    'free_time': prk_data.get('basic_info',{}).get('parking_chrge_bs_time',' '),
                    'basic_fee' : prk_data.get('basic_info',{}).get('parking_chrge_bs_chrge',' '),
                    'adit_time' : prk_data.get('basic_info',{}).get('parking_chrge_adit_unit_time',' '),
                    'adit_fee' : prk_data.get('basic_info',{}).get('parking_chrge_adit_unit_chrge',' '),
                    'daily_fee' : prk_data.get('fxamt_info',{}).get('parking_chrge_one_day_chrge',' '),
                    'monthly_fee' : prk_data.get('fxamt_info',{}).get('parking_chrge_mon_unit_chrge',' ')

                })

            # pandas DataFrame으로 변환
            op_df = pd.DataFrame(opertime_data)
            fee_df = pd.DataFrame(fee_data)
    
            op_csv_path = os.path.join(csv_dir_path, f"op_page_{page_no}.csv")     
            fee_csv_path = os.path.join(csv_dir_path, f"fee_page_{page_no}.csv")     
            op_df.to_csv(op_csv_path, index=False, encoding='utf-8', sep=';')
            fee_df.to_csv(fee_csv_path, index=False, encoding='utf-8', sep=';')
            print(f"OP_CSV 파일이 성공적으로 저장되었습니다: {op_csv_path}")
            print(f"FEE_CSV 파일이 성공적으로 저장되었습니다: {fee_csv_path}")
    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return


def fun_2parquet(**kwargs):
    print("fun_2parquet")

def fun_save():
    print("fun_save")


