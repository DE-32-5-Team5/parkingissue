import os
import json
import csv
import pandas as pd

def fun_api_call():
    import json
    import requests
    import xml.etree.ElementTree as ET

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
    dir_path = f"/opt/airflow/data/"
    filename = kwargs.get('filename')
    file_path = os.path.join(dir_path, filename)
    

    print(f"*****************  {file_path}")
    if os.path.exists(file_path):
        print("파일이 존재합니다.") 
        if filename=='edata.json':
            return 'remove_extract_log'  
        else:
            return 'remove_transform_log'
        
    else: #파일이 없음
        print("파일이 존재하지 않습니다.")
        if filename=='edata.json':
            return 'extract_empty'  
        else:
            return 'transform_empty'


def fun_remove_log(filename):
    dir_path = "/opt/airflow/data/"
    file_path = os.path.join(dir_path, filename)
  
    try:
        os.remove(file_path)
        print(f"{file_path} 파일이 삭제되었습니다.")
    except OSError as e:
        print(f"오류 발생: {e}")


def fun_save_log():
    
    dir_path = "/opt/airflow/data/"
    filename = "edata.json"

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"{dir_path} 디렉토리가 생성되었습니다.")
        else:
            print(f"{dir_path} 디렉토리가 이미 존재합니다.")
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")
    
    # 파일 경로 설정
    file_path = os.path.join(dir_path, filename)

    API_KEY = os.getenv('API_KEY')

    totalcnt=1
    currentcnt=0
    pagenum = 1
    First = True
    json_data=[]

    while currentcnt < totalcnt:
        data = call(pagenum,API_KEY)

        print("*" * 100)
        print(data)
        json_data.append(data)



        if First:
            # totalcnt = data['totalCount'] 
            totalcnt= 30
            First=False
   
        currentcnt+=int(data['numOfRows'])
        pagenum+=1

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print("파일에 내용이 성공적으로 작성되었습니다.")
    except Exception as e:
        print(f"파일 작성 중 오류가 발생했습니다: {e}")


def fun_trans():
    # log 읽기
    dir_path = "/opt/airflow/data/"
    json_filename = "edata.json"
    csv_filename = "tdata.csv"
    json_file_path = os.path.join(dir_path, json_filename)
    csv_file_path = os.path.join(dir_path,csv_filename)

    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)         
        else:
            print(f"경로에 파일이 존재하지 않습니다.")
    except Exception as e:
        print(f"파읽 읽는 중 오류 발생: {e}")
    


    header = ['park_id', 'park_nm', 'park_addr', 'park_la', 'park_lo', 'page_no']
    if (not os.path.exists(csv_file_path)) or (os.path.getsize(csv_file_path) == 0):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header) 
            print("헤더가 추가되었습니다.")


    for d in data:
        print("*"*30)
        print(d)
        pagenum = d['pageNo']
        for prk_data in d['PrkSttusInfo'] :
            
            parkid = prk_data['prk_center_id']
            parknm = prk_data['prk_plce_nm']
            parkaddr = prk_data['prk_plce_adres']
            parkla = prk_data['prk_plce_entrc_la']
            parklo = prk_data['prk_plce_entrc_lo']
            

            row = f"{parkid},{parknm},{parkaddr},{parkla},{parklo},{pagenum}\n"
        
            with open(csv_file_path, mode='a', encoding='utf-8') as file:
                file.write(row)



def fun_2parquet():
    import shutil

    dir_path = "/opt/airflow/data/"
    file_name = "tdata.csv"
    path = os.path.join(dir_path, file_name)
    df = pd.read_csv(path)
    print("^"*1000)
    print(df.isnull().sum())
    df = df.fillna('')
    grouped = df.groupby('page_no')

    p_dir_path = f"{dir_path}parquet"
    #이미 존재하면 먼저 삭제하고
    try:
        if os.path.exists(p_dir_path): 
            shutil.rmtree(p_dir_path)
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")

    # parquet 폴더 생성
    try:
        os.makedirs(p_dir_path)
    except Exception as e:
        print(f"디렉토리 생성 중 오류 발생: {e}")
    

    print(df['park_id'][2:-1])
    print(df['park_nm'][1:-1])
    print(df['park_addr'][1:-1])
    print(df['park_la'][1:-1])
    print(df['park_lo'][1:-1])
    print(df['page_no'].astype('int'))


    # 각 page_no별로 데이터를 Parquet로 저장
    for page_no, group in grouped:
        # 각 page_no에 대해 parquet 파일로 저장    
        output_file = f"{dir_path}/parquet/parkinginfo_{page_no}.parquet"
        group.to_parquet(output_file, index=False)
        print(f"Page {page_no} 데이터가 {output_file}로 저장되었습니다.")



def fun_load():
    import glob
    from mysql.connector import Error
    import mysql.connector

    try:
        # MySQL 연결 설정
        passwd = os.getenv('DB_PW')  # 환경 변수에서 DB 비밀번호 가져오기

        conn = mysql.connector.connect(
            host="parkingissue_database",
            port=3306,
            user="root",
            password=passwd,
            database="parkingissue"
        )

        # 연결 성공 여부 확인
        if conn.is_connected():
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    
    try: 
        cursor = conn.cursor()
        # DELETE 쿼리 실행
        delete_query = "DELETE FROM parkingarea_info;"
        cursor.execute(delete_query)
        print("데이터가 삭제되었습니다.")
        
        # AUTO_INCREMENT 초기화 쿼리 실행
        alter_query = "ALTER TABLE parkingarea_info AUTO_INCREMENT = 1;"
        cursor.execute(alter_query)
        print("AUTO_INCREMENT가 초기화되었습니다.")

    except Error as e:
        print(f"테이블 초기화 오류 발생!!  {e}")

    folder_path = '/opt/airflow/data/parquet'
    parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))
    parquet_files.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

    for file in parquet_files:
        try:
            # 파일 존재 여부 확인
            if os.path.exists(file) and os.path.isfile(file):
                # parquet 파일 읽기
                df = pd.read_parquet(file)
                print(f"파일명: {os.path.basename(file)}")
                print(df)  
                print("-" * 50)

                # 한 번에 INSERT 하기
                if not df.empty:
                    insert_query = """
                    INSERT INTO parkingarea_info (park_id, park_nm, park_addr, park_la, park_lo, page_no) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    # DataFrame을 리스트로 변환
                    data = [tuple(x) for x in df[['park_id', 'park_nm', 'park_addr', 'park_la', 'park_lo', 'page_no']].values]
                    cursor = conn.cursor()
                    cursor.executemany(insert_query, data)  # 여러 행을 한 번에 삽입
                    conn.commit()
                    print(f"{len(data)}개의 데이터가 삽입되었습니다.")
                else:
                    print("DataFrame이 비어 있습니다.")
            else:
                print(f"파일이 존재하지 않거나 잘못된 경로입니다: {file}")
        except Exception as e:
            # 오류 발생 시 처리
            print(f"파일 {os.path.basename(file)}을(를) 읽는 중 오류 발생: {e}")

    if conn.is_connected():
        cursor.close()
        conn.close()
        print("DB connection closed.")


def call(pagenum,API_KEY):
    import requests
    import json

    url = 'http://apis.data.go.kr/B553881/Parking/PrkSttusInfo'
    params ={'serviceKey' : API_KEY, 
             'pageNo' : pagenum, 
            #  'numOfRows' : '10000', 
             'numOfRows' : '2', 
             'format' : '2'
             }
    
    response = requests.get(url, params=params)
    decoded_data = response.content.decode('utf-8')
    data = json.loads(decoded_data)
    return data
    

