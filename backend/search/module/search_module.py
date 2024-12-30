import pymysql.cursors
from db import location_db
import os
import requests
from dotenv import load_dotenv

load_dotenv()

k_key = os.getenv('KAKAO_REST')

def searchParkDB(word):
    connection = location_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT park_id, park_nm, park_addr, park_la, park_lo
            FROM parkingarea_info
            WHERE park_nm LIKE '%{word}%'
            LIMIT 1;
            """
            cursor.execute(sql,)
            result = cursor.fetchone()
            return result

def searchHotDB(word):
    connection = location_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT contentid, mapx, mapy
            FROM festival_info
            WHERE title LIKE '%{word}%'
            LIMIT 1;
            """
            cursor.execute(sql,)
            result = cursor.fetchone()
            return result

def searchAddr(word):
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {'Authorization': f'KakaoAK {k_key}'}
    params = {'query' : word, 'analyze_type' : 'similar', 'size' : 30}

    try:
        res = requests.get(url, params=params, headers=headers).json()
        
        if 'documents' in res and res['documents']:
            addr_li = res['documents'][0]
            x = addr_li['address']['x']
            y = addr_li['address']['y']
            result = {'lon' : x, 'lat' : y}
            return result
        else:
            addr_li = []
            return addr_li
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except KeyError:
        print("Unexpected response structure")
        return [] 