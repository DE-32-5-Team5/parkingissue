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
    #API_KEY = os.getenv('API_KEY')
    API_KEY="Hzx0WsxvEWGO7C0eU5x03SIGP5Pa0Tdlgw0wg9pLiFxmoBLUKnz/1FJDgqEF6gQI2MjDywJePna39kfR8SI+Yg=="
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
    if apiname == 'intro':
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
    if apiname == 'common':
        url = 'http://apis.data.go.kr/B551011/KorService1/detailCommon1'
        params ={'serviceKey' : API_KEY,
                'MobileOS' : 'ETC',
                'MobileApp' : 'parkingissue',
                '_type' : 'json',
                'overviewYN' : 'Y',
                'contentId' : contentid
                }

    while True:
        if attempt==5:
            print("최대 재시도 횟수를 초과하였습니다.")
            #time.sleep(600)
            #attempt=0
            return True

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
    nor=100 #운영계정 변경되면 1000으로 바꾸기

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

def fetch_intro(contentid,typeid):
    data = call('intro',1, 1, '', typeid, contentid )
    print(f" {contentid} 소개정보 호출 성공")
    event_data = data['response']['body']['items']['item'][0]
    eventstartdate = event_data['eventstartdate']
    eventenddate = event_data['eventenddate']
    return eventstartdate,eventenddate

def fetch_common(contentid):
    data = call('common', 1, 1, '', '', contentid)
    print(f" {contentid} 공통정보 호출 성공")
    overview = data['response']['body']['items']['item'][0]['overview']
    return overview

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
                contentid = d.get('contentid', ' ')
                typeid = d.get('contenttypeid',' ')
                if content_type == "Festival":
                    eventstartdate, eventenddate = fetch_intro(contentid,typeid)
                else:
                    eventstartdate=None
                    eventenddate=None
                overview = fetch_common(contentid)

                d_list.append({
                    'contentid' : contentid,
                    'title' : d.get('title', ' '),
                    'address' : d.get('addr1', ' '),
                    'eventstartdate' : eventstartdate,
                    'eventenddate' : eventenddate,
                    'tel' : d.get('tel', ' '),
                    'firstimage' : d.get('firstimage', ' '),
                    'firstimage2' : d.get('firstimage2', ' '),
                    'mapx' : d.get('mapx', ' '),
                    'mapy' : d.get('mapy', ' '),
                    'description' : overview
                })


            # pandas DataFrame으로 변환
            df = pd.DataFrame(d_list)
            csv_path = os.path.join(csv_dir_path, f"page_{page_no}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
            print(f" page_{page_no}.csv --  CSV 파일이 성공적으로 저장되었습니다")

    else:
        print(f"경로에 파일이 존재하지 않습니다.")
        return

def upsert_festival_info(cursor, contentid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy, description):
    eventstartdate = None if eventstartdate == "" else eventstartdate
    eventenddate = None if eventenddate == "" else eventenddate

    insert_query = """
            INSERT INTO festival_info (contentid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(insert_query, (contentid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy, description))
    print(f"데이터 삽입 성공 - id: {contentid}")


from pathlib import Path
from mysql.connector import Error
import mysql.connector

def fun_save(**kwargs):
    print("fun_save")
    passwd = os.getenv('DB_PW')
    print(f"------ {passwd} ----")
    content_type = kwargs['value']  # Festival_CSV | Food_CSV
    csv_path = Path(f"/opt/airflow/HP/{content_type}")

    try:
        with mysql.connector.connect(
            host="10.0.4.80",
            port=6033,
            user="root",
            password=passwd,
            database="parkingissue"
        ) as conn:
            print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")

            with conn.cursor() as cursor:
                if "Festival" in content_type:
                    # 조건('_' 포함)에 맞는 행만 남긴 임시테이블 생성
                    cursor.execute("""
                    CREATE TEMPORARY TABLE temp_table AS
                    SELECT * FROM festival_info WHERE contentid LIKE '%\_%';
                    """)

                    # 기존 테이블 데이터 삭제
                    cursor.execute("DELETE fROM festival_info;")
                    cursor.execute("ALTER TABLE festival_info AUTO_INCREMENT = 1;")

                    # 임시 테이블의 데이터를 다시 삽입
                    cursor.execute("""
                    INSERT INTO festival_info (contentid,title, address,eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy,description )
                    SELECT contentid, title, address,eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy,description
                    FROM temp_table;
                    """)

                    # 임시 테이블 삭제
                    cursor.execute("DROP TEMPORARY TABLE temp_table;")
                    #cursor.execute("DELETE FROM festival_info;")
                    #cursor.execute("ALTER TABLE festival_info AUTO_INCREMENT = 1;")



                for file in csv_path.glob("*.csv"):
                    df = pd.read_csv(file, delimiter=';').fillna('')

                    for index, row in df.iterrows():
                        upsert_festival_info(
                            cursor,
                            row['contentid'],
                            row['title'],
                            row['address'],
                            row['eventstartdate'],
                            row['eventenddate'],
                            row['tel'],
                            row['firstimage'],
                            row['firstimage2'],
                            row['mapx'],
                            row['mapy'],
                            row['description']
                        )

                conn.commit()

    except Error as e:
        # 연결 실패 시 오류 메시지를 출력
        print("MySQL 연결 실패:")
        print(f"에러 코드: {e.errno}")
        print(f"에러 메시지: {e.msg}")
        print(f"SQL 상태: {e.sqlstate}")
