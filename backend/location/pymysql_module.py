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

def select_park_info(park_id):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            # Prepare SQL query
            # i = parkid
            # f = 가격
            # o = 운영 시간
            sql = """
            SELECT
                i.park_id AS park_id,
                f.basic_charge AS fee,
                o.wee_orn_st AS wee_orn_st,
                o.wee_orn_et AS wee_orn_et,
                o.wk_orn_st AS wk_orn_st,
                o.wk_orn_et AS wk_orn_et,
                o.hol_orn_st AS hol_orn_st,
                o.hol_orn_et AS hol_orn_et,
                TIME_TO_SEC(TIMEDIFF(o.wee_orn_et, o.wee_orn_st)) AS weekly,
                TIME_TO_SEC(TIMEDIFF(o.wk_orn_et, o.wk_orn_st)) AS weekend,
                TIME_TO_SEC(TIMEDIFF(o.hol_orn_et, o.hol_orn_st)) AS holiday
            FROM
                parkingarea_info AS i
            LEFT JOIN
                parkingarea_fee AS f ON i.park_id = f.park_id
            LEFT JOIN
                parkingarea_opertime AS o ON i.park_id = o.park_id
            WHERE
                i.park_id = %s;
            """
            # Execute the query with proper parameterization
            cursor.execute(sql, (park_id,))
            result = cursor.fetchone()
            return result

def related_data(text):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT park_nm AS {text}
            FROM parkingarea_info
            WHERE park_nm LIKE '%{text}%'
            LIMIT 5;
            """
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result