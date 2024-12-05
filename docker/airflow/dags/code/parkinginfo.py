import os
import json
import csv

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
    if os.path.exists(file_path): #폴더가 존재하면
        if filename=='edata.json':
            return 'remove_extract_log'  
        else:
            return 'remove_transform_log'
    
    else:
        print("폴더가 존재하지 않습니다.")
        if filename=='edata.json':
            return 'extract_empty'  
        else:
            return 'transform_empty'

def fun_remove_log(filename):
    # path = "/opt/airflow/Edata/"
    dir_path = "opt/airflow/data"
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
            totalcnt= 5
            First=False
   
        currentcnt+=int(data['numOfRows'])
        pagenum+=1

    # 파일에 내용 작성
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def fun_trans():
    # log 읽기
    dir_path = "/opt/airflow/Edata/"
    filename = "data.json"
    csv_filename = 'data.csv'
    json_file_path = os.path.join(dir_path, filename)
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
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header) 
            print("헤더가 추가되었습니다.")

    # 필요한 것만 뽑아내기
    for d in data:
        print("*"*30)
        print(d)
        pagenum = d['pageNo']
        for prk_data in d['PrkSttusInfo'] :
            prk_list =[]
            parkid = prk_data['prk_center_id']
            parknm = prk_data['prk_plce_nm']
            parkaddr = prk_data['prk_plce_adres']
            parkla = prk_data['prk_plce_entrc_la']
            parklo = prk_data['prk_plce_entrc_lo']
            prk_list.append([parkid, parknm, parkaddr, parkla, parklo, pagenum])

            with open(csv_file_path, mode='a') as file:
                # 리스트를 쉼표로 구분한 문자열로 변환
                row = ','.join(map(str, prk_list)) + '\n'
                file.write(row)


        

def fun_conn():
    print(f"fun_conn")

def fun_load():
    print(f"fun_load")



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
    

