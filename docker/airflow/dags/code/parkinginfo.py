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
        print( f" $$$ 시작 ")
        if attempt==5:
            print("최대 재시도 횟수를 초과하였습니다. 10분 후 다시 시도합니다.")
            time.sleep(600)
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
    base_path = "/opt/airflow/Info"
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
    dir_path = "/opt/airflow/Info/Edata"
    First = True
    total=0
    for page in range(startpage, startpage+500):
        if page == total:
            break

        file_path = os.path.join(dir_path, f"page_{page}.json")  
        print(f"파일경로 !!! {file_path}") 
        # data = call(page, 10)
        data = call(page, 1000)
        if First:
            total = int(data['totalCount'])
            First=False
        print(f" ######### page_{page}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("파일에 내용이 성공적으로 작성되었습니다.")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")

def fun_2csv(**kwargs):
    startpage = kwargs['value']
    json_dir_path = "/opt/airflow/Info/Edata"
    csv_dir_path = "/opt/airflow/Info/Tdata"

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


def fun_2parquet(**kwargs):
    print("fun_2parquet")

def fun_save():
    print("fun_save")





# --------------------------





# def fun_2parquet():
#     p_dir_path = "/opt/airflow/Pdata"

#     # 디렉토리 삭제
#     try:
#         if os.path.exists(p_dir_path):
#             shutil.rmtree(p_dir_path)
#             print("Pdata 디렉토리 삭제 완료")
#         else:
#             print("Pdata 디렉토리가 존재하지 않습니다.")
#     except Exception as e:
#         print(f"디렉토리 삭제 중 오류 발생: {e}")

#     # 디렉토리 생성
#     try:
#         os.makedirs(p_dir_path)
#         print("Pdata 디렉토리 생성 완료")
#     except Exception as e:
#         print(f"디렉토리 생성 중 오류 발생: {e}")

#     dir_path = "/opt/airflow/Tdata/"
#     files = os.listdir(dir_path)
#     files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
    
#     for file in files:
#         path = os.path.join(dir_path, file)
#         df = pd.read_csv(path, delimiter=';')
#         output_file = f"{p_dir_path}/{file.split('.')[0]}.parquet"
#         df.to_parquet(output_file, index=False)
#         print(f"Page {file.split('.')[0]} 데이터가 {output_file}로 저장되었습니다.")
        


# def fun_load(**kwargs):
#     import glob
#     from mysql.connector import Error
#     import mysql.connector

#     try:
#         passwd = os.getenv('DB_PW')

#         conn = mysql.connector.connect(
#             host="parkingissue_database",
#             port=3306,
#             user="root",
#             password=passwd,
#             database="parkingissue"
#         )

#         if conn.is_connected():
#             print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         return None

#     try:
#         cursor = conn.cursor()
#         delete_query = "DELETE FROM parkingarea_info;"
#         cursor.execute(delete_query)
#         alter_query = "ALTER TABLE parkingarea_info AUTO_INCREMENT = 1;"
#         cursor.execute(alter_query)

#     except Error as e:
#         print(f"테이블 초기화 오류 발생!! {e}")

#     folder_path = '/opt/airflow/Pdata'
#     parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))
#     parquet_files.sort(key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group()))

#     for file in parquet_files:
#         try:
#             if os.path.exists(file) and os.path.isfile(file):
#                 df = pd.read_parquet(file)
#                 if not df.empty:
#                     insert_query = """
#                     INSERT INTO parkingarea_info (park_id, park_nm, park_addr, park_la, park_lo, page_no) VALUES (%s, %s, %s, %s, %s, %s)
#                     """
#                     data = [tuple(x) for x in df[['park_id', 'park_nm', 'park_addr', 'park_la', 'park_lo', 'page_no']].values]
#                     cursor = conn.cursor()
#                     cursor.executemany(insert_query, data)
#                     conn.commit()
#                     print(f"{len(data)}개의 데이터가 삽입되었습니다.")
#             kwargs['ti'].xcom_push(key='final', value='Success')
#         except Exception as e:
#             print(f"파일 {os.path.basename(file)}을(를) 읽는 중 오류 발생: {e}")
#             kwargs['ti'].xcom_push(key='final', value='Fail')

#     if conn.is_connected():
#         cursor.close()
#         conn.close()
#         print("DB connection closed.")


# def fun_final(**kwargs):
#     ti = kwargs['ti']
#     final_result = ti.xcom_pull(key='final', task_ids='load_data')
#     print("-" * 50)
#     print(f"최종 실행 결과는 !! {final_result}")

#     dir_path = "/opt/airflow/Result"
#     file_path = f"{dir_path}/result.csv"

#     try:
#         if not os.path.exists(dir_path):
#             os.makedirs(dir_path)
#             print(f"{dir_path} 디렉토리가 생성되었습니다.")
#         else:
#             print(f"{dir_path} 디렉토리가 이미 존재합니다.")
#     except Exception as e:
#         print(f"디렉토리 생성 중 오류 발생: {e}")

#     header = ['date', 'result']
  
#     if not os.path.exists(file_path):
#         with open(file_path, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(header)  
#         print(f"새로운 파일 생성 및 헤더 추가됨: {file_path}")

#     airflow_execution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     new_data = [airflow_execution_date, final_result]

#     with open(file_path, mode='r+', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         rows = list(reader)

#         # 파일이 비어있거나 헤더만 있는 경우, 데이터 추가
#         if len(rows) == 1:  # 헤더만 있는 경우
#             with open(file_path, mode='a', newline='', encoding='utf-8') as file_append:
#                 writer = csv.writer(file_append)
#                 writer.writerow(new_data)  
#             print(f"헤더만 존재, 새로운 행이 추가되었습니다: {new_data}")
        
#         # 파일에 마지막 행이 있는 경우
#         elif len(rows) > 1:
#             last_row = rows[-1]
#             if last_row[0] <= airflow_execution_date:  # 마지막 행의 'date'가 에어플로우 실행 날짜보다 같거나 이전인 경우
#                 with open(file_path, mode='a', newline='', encoding='utf-8') as file_append:
#                     writer = csv.writer(file_append)
#                     writer.writerow(new_data)  # 새로운 데이터 추가
#                 print(f"새로운 행이 추가되었습니다: {new_data}")
#             else:
#                 print(f"에러: 'date' 값이 에어플로우 실행 날짜({airflow_execution_date})보다 미래입니다.")

        


    # import requests
    # import json

    # url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    # params ={'serviceKey' : API_KEY, 
    #          'pageNo' : pagenum, 
    #          'numOfRows' : '1000', 
    #         #  'numOfRows' : '3', 
    #          'format' : '2'
    #          }

    # attempt = 0  # 시도 횟수

    # while True:
    #     if attempt==10:
    #         print("최대 재시도 횟수를 초과하였습니다. 10분 후 다시 시도합니다.")
    #         time.sleep(600)
    #         attempt=0
    #         # session = requests.Session()

    #     try:
    #         response = session.get(url, params=params)

    #         # 응답 상태 코드 확인
    #         if response.status_code == 200:

    #             # 본문이 비어 있으면 재시도
    #             if not response.text.strip(): 
    #                 print("응답 본문이 비어있습니다. 재시도 중...")
    #                 attempt += 1

    #             # JSON 파싱 오류 발생 시 재시도
    #             try:
    #                 data = response.json() 
    #                 return data
    #             except json.decoder.JSONDecodeError as e:
    #                 print(f"JSON 파싱 오류: {e}")
    #                 print("응답 본문:", response.text) 
    #                 attempt += 1
    #                 continue  

    #         # 상태 코드가 200이 아니면 재시도
    #         else:
    #             print(f"응답 상태 코드 오류: {response.status_code}")
    #             attempt += 1
    #             continue  

    #     # 요청 오류 발생 시 재시도
    #     except requests.exceptions.RequestException as e:
    #         print(f"요청 예외 발생: {e}")
    #         attempt += 1
    #         continue  