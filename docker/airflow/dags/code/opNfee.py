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
    base_path = "/opt/airflow/Data/OP"
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
    dir_path = "/opt/airflow/Data/OP/Edata"
    
    First = True
    total=0
    rownum=-1
    for page in range(startpage, startpage+500):
        file_path = os.path.join(dir_path, f"page_{page}.json")
        # data = call(page, 10)
        data = call(page, 1000)
        print(f" ######### {page}")
        if First:
            total = int(data['totalCount'])
            rownum=int(data['numOfRows'])
            First=False
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
    json_dir_path = "/opt/airflow/Data/OP/Edata"
    csv_dir_path = "/opt/airflow/Data/OP/Tdata"

    if os.path.exists(json_dir_path):
        files = os.listdir(json_dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
        # print(files[startpage-1:startpage+10-1])
        files = files[startpage-1:startpage+500-1]

        for file in files:
            file_path = os.path.join(json_dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            page_no = data.get('pageNo')
            opertime_data = []
            fee_data =[]

            for prk_data in data['PrkOprInfo']:
                    wee_orn_st = [prk_data.get('Monday', {}).get('opertn_start_time', ' ')]  
                    wee_orn_et = [prk_data.get('Monday', {}).get('opertn_end_time', ' ')] 

                    wk_orn_st = [prk_data.get('Saturday', {}).get('opertn_start_time', ' ')]
                    wk_orn_et = [prk_data.get('Saturday', {}).get('opertn_end_time', ' ')]

                    hol_orn_st = [prk_data.get('holiday', {}).get('opertn_start_time', ' ')]
                    hol_orn_et = [prk_data.get('holiday', {}).get('opertn_end_time', ' ')]

                    opertime_data.append({
                        'park_id': prk_data.get('prk_center_id', ' '),
                        'wee_orn_st': wee_orn_st,  
                        'wee_orn_et': wee_orn_et,  
                        'wk_orn_st': wk_orn_st,  
                        'wk_orn_et': wk_orn_et,  
                        'hol_orn_st': hol_orn_st,  
                        'hol_orn_et': hol_orn_et   
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
            print(f" op_page_{page_no}.csv --  OP_CSV 파일이 성공적으로 저장되었습니다")
            print(f" fee_page_{page_no}.csv -- FEE_CSV 파일이 성공적으로 저장되었습니다")
    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return

def fun_2parquet():
    dir_path = "/opt/airflow/Data/OP/Tdata"
    p_dir_path = "/opt/airflow/Data/OP/Pdata"

    try:
        os.makedirs(p_dir_path, exist_ok=True)
        print("Pdata 디렉토리 생성 완료")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")

    all_files = os.listdir(dir_path)
    op_files = [file for file in all_files if file.startswith('op')]
    fee_files = [file for file in all_files if file.startswith('fee')]

    op_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
    fee_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))

    # 각 파일의 데이터를 하나로 합치기
    op_combined_df = pd.concat((pd.read_csv(f"{dir_path}/{file}") for file in op_files), ignore_index=True)
    fee_combined_df = pd.concat((pd.read_csv(f"{dir_path}/{file}") for file in fee_files), ignore_index=True)

    # Parquet 파일로 저장 
    op_output_file = os.path.join(p_dir_path, "optime.parquet")
    op_combined_df.to_parquet(op_output_file, index=False)
    fee_output_file = os.path.join(p_dir_path, "fee.parquet")
    fee_combined_df.to_parquet(fee_output_file, index=False)

    print("전체 parquet 저장 완료")

       
    
def fun_save(**kwargs):
    import glob
    from mysql.connector import Error
    import mysql.connector

    
    try:
        # 환경변수에서 비밀번호 가져오기
        passwd = os.getenv('DB_PW')

        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host="parkingissue_database",
            port=3306,
            user="root",
            password=passwd,
            database="parkingissue"
        )

        if conn.is_connected():
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
        
        cursor = conn.cursor()
        parquet_files = glob.glob(kwargs.get('file_path', '*.parquet'))

        for file in parquet_files:
            print(f" ////// {file} 처리 시작 ")

            df = pd.read_parquet(file)
            
            for index, row in df.iterrows():
                record_id = row['park_id']  
                select_query = "SELECT id FROM your_table WHERE id = %s"
                cursor.execute(select_query, (record_id,))
                result = cursor.fetchone()

                 # ID 값이 있으면 업데이트
                if result:
                    update_query = """
                    UPDATE your_table
                    SET 
                        column1 = %s,
                        column2 = %s,
                        column3 = %s
                    WHERE id = %s
                    """
                    cursor.execute(update_query, (row['column1'], row['column2'], row['column3'], record_id))
                    print(f"ID {record_id} updated successfully.")
                # ID 값이 없으면 새로 추가
                else:
                    insert_query = """
                    INSERT INTO your_table (id, column1, column2, column3)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (record_id, row['column1'], row['column2'], row['column3']))
                    print(f"ID {record_id} inserted successfully.")

            # 변경 사항 커밋
            conn.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")