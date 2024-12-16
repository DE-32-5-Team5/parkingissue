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

def call(apiname,nor, pn, listyn, typeid, contentid='' ):
    API_KEY = os.getenv('API_KEY2')
    attempt = 0  # 시도 횟수

    if apiname.startswith('r-'):
        url = 'http://apis.data.go.kr/B551011/KorService1/areaBasedList1'
        params ={'serviceKey' : API_KEY,
                'MobileOS' : 'ETC',
                'MobileApp' : 'parkingissue',
                'numOfRows' :nor,
                'pageNo' : pn,
                '_type' : 'json',
                'listYN' :  listyn, #N이면 숫자(개수) Y이면 목록
                'arrange' : 'A', # 정렬구분 (A=제목순, C=수정일순, D=생성일순) 대표이미지가반드시있는정렬(O=제목순, Q=수정일순, R=생성일순)
                'contentTypeId' : typeid  #15:축제, 39:음식점
                }
    else:
        url = 'http://apis.data.go.kr/B551011/KorService1/detailIntro1'
        params ={'serviceKey' : API_KEY,
                'MobileOS' : 'ETC',
                'MobileApp' : 'parkingissue',
                'numOfRows' :nor,
                'pageNo' : pn,
                '_type' : 'json',
                'contentTypeId' : typeid,  #15:축제, 39:음식점
                'contentId' : contentid
                }

    while True:
        if attempt==10:
            print("최대 재시도 횟수를 초과하였습니다. 10분 후 다시 시도합니다.")
            time.sleep(600)
            attempt=0

        try:
            response = session.get(url, params=params,stream=True)

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

def fun_mkdir(**kwargs):
    dirname = kwargs['value']
    if dirname == 'HP':
        base_path = "/opt/airflow"
    else:
        base_path = "/opt/airflow/HP"

    dir_path = os.path.join(base_path, dirname)

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        print(f" ##### '{dirname}' 폴더 삭제 후 다시 생성되었습니다.")
    else:
        os.mkdir(dir_path)
        print(f" #####'{dirname}' 폴더가 생성되었습니다.")


def fetch_data(api_name, typeid):
    dir_path = '/opt/airflow/HP'
    result = call(api_name, 1, 1, 'N', typeid)
    totalCnt = int(result['response']['body']['items']['item'][0]['totalCnt'])
    print(f"***** Total Count: {totalCnt}")

    curCnt = 0
    pn = 1
    listyn = 'Y'
    nor=100

    while totalCnt > curCnt:
        file_path = f"{dir_path}/{api_name[2:].capitalize()}/page_{pn}.json"
        data = call(api_name, nor, pn, listyn, typeid)
        pn += 1
        curCnt += nor
        print(f" ----- 현재 {pn - 1} 페이지 호출 .")

        # 데이터 저장
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"파일에 내용이 성공적으로 작성되었습니다: {file_path}")
        except Exception as e:
            print(f"파일 작성 중 오류가 발생했습니다: {e}")


def fun_fetch(**kwargs):
    api_name = kwargs['value']

    api_settings = {
        'r-festival': '15',
        'r-food': '39',
    }

    if api_name in api_settings:
        typeid = api_settings[api_name]
        fetch_data(api_name, typeid)
    else:
        print(f"알 수 없는 API 이름: {api_name}")

def fetch_intro(fid,typeid):
    data = call('intro',1, 1, '', typeid, fid )
    event_data = data['response']['body']['items']['item'][0]
    eventstartdate = event_data['eventstartdate']
    eventenddate = event_data['eventenddate']
    return eventstartdate,eventenddate


def fun_2csv(**kwargs):
    #Json 파일 읽어서 필요한 부분만 추출하기
    #넘어오는 값은 Festival이랑 Food

    content_type = kwargs['value']  #Festival | Food
    json_dir_path = f"/opt/airflow/HP/{content_type}"
    csv_dir_path = f"/opt/airflow/HP/{content_type}_CSV"


    if os.path.exists(json_dir_path):
        files = os.listdir(json_dir_path)
        files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))

        for file in files:
            page_no = re.search(r'\d+', file).group()
            file_path = os.path.join(json_dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            d_list = []
            for d in data['response']['body']['items']['item']:
                fid = d.get('contentid', ' ')
                typeid = d.get('contenttypeid',' ')
                if content_type == "Festival":
                    eventstartdate, eventenddate = fetch_intro(fid,typeid)
                else:
                    eventstartdate=""
                    eventenddate=""

                d_list.append({
                    'fid' : fid,
                    'title' : d.get('title', ' '),
                    'address' : d.get('addr1', ' '),
                    'eventstartdate' : eventstartdate,
                    'eventenddate' : eventenddate,
                    'tel' : d.get('tel', ' '),
                    'firstimage' : d.get('firstimage', ' '),
                    'firstimage2' : d.get('firstimage2', ' '),
                    'mapx' : d.get('mapx', ' '),
                    'mapy' : d.get('mapy', ' ')
                })


            # pandas DataFrame으로 변환
            df = pd.DataFrame(d_list)

            csv_path = os.path.join(csv_dir_path, f"page_{page_no}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
            print(f" page_{page_no}.csv --  CSV 파일이 성공적으로 저장되었습니다")

    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return

def fun_save(**kwargs):
    print("fun_save")
    import glob
    from mysql.connector import Error
    import mysql.connector

    content_type = kwargs['value']  #Festival_CSV | Food_CSV
    csv_path = f"/opt/airflow/HP/{content_type}"

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
        files = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
        for file in files:
            file_path = os.path.join(csv_path, file)
            df = pd.read_csv(file_path, delimiter=';')
            for index, row in df.iterrows():
                #fid = row['fid']
                #title = row['title']
                #address = row['address']
                #eventstartdate = row['eventstartdate']
                #eventenddate = row['eventenddate']
                #tel = row['tel']
                #firstimage = row['firstimage']
                #firstimage2 = row['firstimage2']
                #mapx = row['mapx']
                #mapy = row['mapy']

                fid = "" if pd.isna(row['fid']) else row['fid']
                title = ""  if pd.isna(row['title']) else row['title']
                address = "" if pd.isna(row['address']) else row['address']
                eventstartdate = None if pd.isna(row['eventstartdate']) else row['eventstartdate']
                eventenddate = None if pd.isna(row['eventenddate']) else row['eventenddate']
                tel = "" if pd.isna(row['tel']) else row['tel']
                firstimage = "" if pd.isna(row['firstimage']) else row['firstimage']
                firstimage2 = "" if pd.isna(row['firstimage2']) else row['firstimage2']
                mapx = "" if pd.isna(row['mapx']) else row['mapx']
                mapy = "" if pd.isna(row['mapy']) else row['mapy']

                # 해당 fid가 이미 존재하는지 확인
                cursor.execute("SELECT COUNT(*) FROM fastival_info WHERE fid = %s", (fid,))
                result = cursor.fetchone()

                if result[0] > 0:  # fid가 존재하면 업데이트
                    update_query = """
                        UPDATE fastival_info
                        SET title = %s, address = %s, eventstartdate = %s, eventenddate = %s,tel = %s, firstimage = %s, firstimage2 = %s, mapx = %s, mapy = %s
                        WHERE fid = %s
                    """

                    cursor.execute(update_query, (title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy, fid))
                    print(f"값 업데이트 완료 - id:{fid}")

                else:  # fid가 존재하지 않으면 삽입
                    insert_query = """
                        INSERT INTO fastival_info (fid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (fid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy))
        print(f"데이터 업데이트 완료 - id: {fid}")

        # 커밋하여 변경사항 저장
        conn.commit()



    except Error as e:
        print(f"에러발생 : {e}")
        raise

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")