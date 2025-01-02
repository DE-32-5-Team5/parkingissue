import pymysql.cursors

def connect_db():
    connection = pymysql.connect(
        host='10.0.4.80',
        port=6033,
        user='root',
        password='samdul2024$',
        database='parkingissue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
# bookmarks 테이블 조회
def select_bookmarks(idtype, idcode, bookmark_longitude, bookmark_latitude):
    tableNm = "user_bookmarks" if idtype == "uid" else "manager_bookmarks"
    tableNm2 = "user_info" if idtype == "uid" else "manager_info"
    colNm = "user_id" if idtype == "uid" else "manager_id"

    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            # idcode 확인
            cursor.execute(
                f"SELECT {idtype} FROM {tableNm2} WHERE {colNm} = %s", (idcode,)
            )
            idcode_row = cursor.fetchone()
            idcode = idcode_row[f'{idtype}']

            sql = f"""
            SELECT title, address,
            (6371 * acos(cos(radians(%s)) * cos(radians(mapy)) *
            cos(radians(mapx) - radians(%s)) + sin(radians(%s)) * sin(radians(mapy)))) AS distance
            FROM festival_info
            WHERE
                fid IN (
                    SELECT fid
                    FROM {tableNm}
                    WHERE {idtype} = %s
                )
            ORDER BY distance ASC
            """

            cursor.execute(sql, (bookmark_latitude, bookmark_longitude, bookmark_latitude, idcode))
            result = cursor.fetchall()
            return result
# 북마크 삽입
def insert_bookmarks(idtype, idcode, contentid):
    if idtype not in ["uid", "mid"]:
        raise ValueError("Invalid idtype. Must be 'uid' or 'mid'.")

    # 테이블 이름 결정
    tableNm = "user_bookmarks" if idtype == "uid" else "manager_bookmarks"
    tableNm2 = "user_info" if idtype == "uid" else "manager_info"
    colNm = "user_id" if idtype == "uid" else "manager_id"

    # 데이터베이스 연결
    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            # fid 조회
            cursor.execute(
                "SELECT fid FROM festival_info WHERE contentid = %s", (contentid,)
            )
            fid_row = cursor.fetchone()
            if not fid_row:
                raise ValueError("No matching fid found for the provided contentid.")
            fid = fid_row['fid']

            # idcode 확인
            cursor.execute(
                f"SELECT {idtype} FROM {tableNm2} WHERE {colNm} = %s", (idcode,)
            )
            idcode_row = cursor.fetchone()
            idcode = idcode_row[f'{idtype}']
            if not idcode_row:
                raise ValueError("No matching idcode found for the provided idtype.")

            # 북마크 삽입
            sql = f"INSERT INTO {tableNm} ({idtype}, fid) VALUES (%s, %s)"
            cursor.execute(sql, (idcode, fid))

            # 커밋 및 성공 반환
            connection.commit()
            return True

def delete_bookmarks(idtype, idcode, contentid):
    # 테이블 이름 설정
    tableNm = "user_bookmarks" if idtype == "uid" else "manager_bookmarks"

    # 유효한 idtype 값인지 확인
    if idtype not in ["uid", "mid"]:
        raise ValueError("Invalid idtype. Must be 'uid' or 'mid'.")

    connection = connect_db()
    with connection:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = f"""
            DELETE FROM {tableNm}
            WHERE
                fid = (
                    SELECT fid FROM festival_info WHERE contentid = %s
                )
            AND
                idcode = %s
            """
            # 쿼리 실행
            result = bool(cursor.execute(sql, (contentid, idcode)))
            # 영향을 받은 행 수 반환
            return result

def check_bookmarks(idtype, idcode, contentid):
    tableNm = "user_bookmarks" if idtype == "uid" else "manager_bookmarks"
    tableNm2 = "user_info" if idtype == "uid" else "manager_info"
    colNm = "user_id" if idtype == "uid" else "manager_id"

    # 유효한 idtype 값인지 확인
    if idtype not in ["uid", "mid"]:
        raise ValueError("Invalid idtype. Must be 'uid' or 'mid'.")

    connection = connect_db()
    print("#"*100)
    print(idtype)
    print(idcode)
    print(contentid)
    print("#"*100)

    with connection:
        with connection.cursor() as cursor:
            # fid 조회
            cursor.execute(
                "SELECT fid FROM festival_info WHERE contentid = %s", (contentid,)
            )
            fid_row = cursor.fetchone()
            if not fid_row:
                raise ValueError("No matching fid found for the provided contentid.")
            fid = fid_row['fid']
            print(fid)
            print("#"*100)
            # idcode 확인
            cursor.execute(
                f"SELECT {idtype} FROM {tableNm2} WHERE {colNm} = %s", (idcode,)
            )
            idcode_row = cursor.fetchone()
            idcode = idcode_row[f'{idtype}']
            print(idcode)
            print("#"*100)
            if not idcode_row:
                raise ValueError("No matching idcode found for the provided idtype.")

            sql = f"""
            SELECT contentid
            FROM festival_info
            WHERE
                fid IN (
                    SELECT fid
                    FROM {tableNm}
                    WHERE {idtype} = %s
                ) AND contentid = %s
            """
            cursor.execute(sql, (idcode, contentid))
            result = cursor.fetchone() # 북마크했으면 True, 북마크 안했으면 False
            print("#"*100)
            print(colNm)
            print(contentid)
            print(result)
            print("#"*100)

            return bool(result)

def update_bookmarks(idtype, idcode, contentid, bookmark_nickname):
    tableNm = "user_bookmarks" if idtype == "uid" else "manager_bookmarks"

    # 유효한 idtype 값인지 확인
    if idtype not in ["uid", "mid"]:
        raise ValueError("Invalid idtype. Must be 'uid' or 'mid'.")

    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            UPDATE {tableNm}
            SET bookmark_nickname = %s
            WHERE {idtype} = %s
            """

            cursor.execute(sql, (bookmark_nickname, idcode))
            result = bool(cursor.fetchone()) # 수정했으면 True, 수정안했으면 False
            return result