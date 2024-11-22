# RDD of Database

## Database

- 사용할 데이터베이스 명칭은 'parkingissue'로 통일한다.
- 해당 데이터베이스 접근은 데이터베이스 로그인한 유저에 따라 권한을 다르게 설정한다.
    - 로그인 시킬 유저의 목록은 이 후 후술한다.

## Login, Access

- 관리자 'root'의 정보는 관리자 페이지에 기록한다.
    - 관리자의 로그인 기록정보는 별도의 알람으로 접속기록 및 처리내용을 확인하도록 한다.
    - 관리자는 모든 정보 확인이 가능하도록 설정한다.
    
- 유저 'login'의 정보는 아래와 같이 생성한다.
    - 'login'의 로그인 기록정보는 시스템 log로 서버에 별도의 파일로 1일 단위로 저장되어야 한다.
        - 이 때, 기록되어야 하는 내용은 다음과 같다.
            - 접속 시도 IP
            - 접속 시도를 하고자 하는 유저의 uid
            - 해당 로그인 시도에 대한 성공 실패 결과
            - 접속 시도 시각
    - 'login' 유저의 비밀번호는 login으로 유지한다.
    - 'login' 유저의 접근 권한은 아래 테이블로 한정한다.
        - 'user_info'의 SELECT 권한
        - 'manager_info'의 SELECT 권한
    - 유저의 login process가 종료되면 연결을 해제한다.

- 유저 'signup_user'의 정보는 아래와 같이 생성한다.
    - 'signup_user'의 로그인 기록정보는 시스템 log로 서버에 별도의 파일로 1일 단위로 저장되어야 한다.
        - 이 때, 기록되어야 하는 내용은 다음과 같다.
            - 접속 시도 IP
            - 생성된 uid
            - 생성된 uid가 어떤 방식으로 가입했는지
                - 일반 회원가입
                - 간편 회원가입 : 네이버
                - 간편 회원가입 : 카카오
            - 생성 시각
    - 'signup_user'의 비밀번호는 관리자 페이지에 기록한다.
    - 'signup_user'유저의 접근 권한은 아래 테이블로 한정한다.
        - 'user_info'의 INSERT 권한
        - 'manager_info'의 INSERT 권한
    - 유저의 signup process가 종료되면 연결을 해제한다.

- 유저 'common_user'의 정보는 아래와 같이 생성한다.
    - 'common_user'의 로그인 기록정보는 시스템 log로 서버에 별도의 파일로 1일 단위로 저장되어야 한다.
        - 이 때, 기록되어야 하는 내용은 다음과 같다.
            - 접속 중인 IP
            - 접속중인 유저의 uid
            - 접속중인 유저가 DB에 요청한 내용
                - 'parkingarea_info'의 SELECT 요청
                - 'parkingarea_opertime'의 INSERT, UPDATE, DELETE 요청
                - 'parkingarea_operfee'의 INSERT, UPDATE, DELETE 요청
                - 'parkingarea_real'의 SELECT 요청
                - 'user_bookmarks'의 SELECT 요청
                - 'festival_info'의 SELECT 요청
            - 요청 시각
    - 'common_user'의 비밀번호는 'common_user'로 유지한다.
    - 'common_user'유저의 접근 권한은 아래 테이블로 한정한다.
        - 'user_info'의 SELECT 권한
        - 'parkingarea_info'의 SELECT 권한
        - 'parkingarea_opertime'의 INSERT, UPDATE, DELETE 권한
        - 'parkingarea_operfee'의 INSERT, UPDATE, DELETE 권한
        - 'parkingarea_real'의 SELECT 권한
        - 'user_bookmarks'의 INSERT, SELECT, DELETE, UPDATE 권한
        - 'festival_info'의 SELECT 권한
    - 유저가 page를 종료하거나, log out 프로세스를 진행하면 연결을 종료한다.

- 유저 'manage_user'의 정보는 아래와 같이 생성한다.
     - 'manage_user'의 로그인 기록정보는 시스템 log로 서버에 별도의 파일로 1일 단위로 저장되어야 한다.
        - 이 때, 기록되어야 하는 내용은 다음과 같다.
            - 접속중인 IP
            - 접속중인 유저의 mid
            - 접속중인 유저가 DB에 요청한 내용
                - 'parkingarea_info'의 SELECT 요청
                - 'parkingarea_opertime'의 INSERT, UPDATE, DELETE 요청
                - 'parkingarea_operfee'의 INSERT, UPDATE, DELETE 요청
                - 'parkingarea_real'의 SELECT 요청
                - 'user_bookmarks'의 SELECT, INSERT, DELETE, UPDATE 요청
                - 'festival_info'의 SELECT, INSERT, DELETE, UPDATE 요청
            - 요청 시각
    - 'manage_user'의 비밀번호는 관리자 페이지에 기록한다
    - 'manage_user'유저의 접근 권한은 아래 테이블로 한정한다.
        - 'user_info'의 SELECT 권한
        - 'parkingarea_info'의 SELECT 권한
        - 'parkingarea_opertime'의 INSERT, UPDATE, DELETE 요청
        - 'parkingarea_operfee'의 INSERT, UPDATE, DELETE 요청
        - 'parkingarea_real'의 SELECT 권한
        - 'user_bookmarks'의 INSERT, SELECT, DELETE, UPDATE 권한
        - 'festival_info'의 SELECT, INSERT, DELETE, UPDATE 권한
    - 유저가 page를 종료하거나, log out 프로세스를 진행하면 연결을 종료한다.

    -

- 유저 'airflow_updater'의 정보는 아래와 같이 생성한다.
    - 'airflow_updater'의 로그인 기록정보는 시스템 log로 서버에 별도의 파일로 1일단위로 저장되어야 한다.
        - 이 때, 기록되어야 하는 정보는 다음과 같다.
            - 접속 시간
            - UPDATE, DELETE, INSERT 시도된 쿼리 전문
            - 해당 쿼리의 처리 결과
    - 'airflow_updater'의 비밀번호는 관리자 페이지에 기록한다.
    - 'airflow_updater'유저의 접근 권한은 아래 테이블로 한정한다.
        - 'parkingarea_info'의 INSERT, UPDATE, DELETE 요청
        - 'parkingarea_opertime'의 INSERT, UPDATE, DELETE 요청
        - 'parkingarea_operfee'의 INSERT, UPDATE, DELETE 요청
        - 'parkingarea_real'의 INSERT, UPDATE, DELETE 요청
        - 'festival_info'의 INSERT, UPDATE, DELETE 요청
    - airflow process가 종료되면 연결을 해제한다.

- 이 아래는 추가해야할 별도의 유저, 관리자가 있다면 WBS, 회의록 내용과 함께 추가한다.

## Tables

### About Login

- 테이블 'user_info'는 아래와 같이 정의한다.
    1. 'uid' : user_id로 유저 식별자로 사용한다. 테이블 삽입시 자동 생성 및 자동 증가되도록 설정해야한다.
        - int형 숫자의 데이터형태로 저장한다.
        - Primary Key로 지정한다.
    2. 'id' : 보통 id라고 식별되는 컬럼. 간편로그인 기능이 있기 때문에 해당 컬럼은 not null에서 해제되어야 한다.
        - Varchar(255)자로 저장한다.
        - NULL값이 가능하다.
    3. 'pw' : 보통 password로 식별되는 컬럼. 간편로그인 기능이 있기 때문에 해당 컬럼은 not null에서 해제되지만, id칸이 있을때는 빈 값으로 존재할 수 없어야 한다.
        - Varchar(255)자로 저장한다.
        - NULL값이 가능하다.
        - 보안을 위해 해당 필드는 NULL이 아닐경우 절대로 평문저장을 진행해선 안된다.
    4. 'naver_id' : 네이버 API를 사용하여 로그인되거나 회원가입할 시 API과 소통할때 로그인 정보를 활용할 수 있는 naver의 id를 저장한다.
    5. 'kakao_id' : 카카오 API를 사용하여 로그인되거나 회원가입할 시 API과 소통할때 로그인 정보를 활용할 수 있는 kakao의 id를 저장한다.

- 테이블 'manager_info'는 아래와 같이 정의한다.
    1. 'mid' : manager_id로 유저 식별자로 사용한다. 테이블 삽입시 자동 생성 및 자동 증가되도록 설정해야한다.
        - int형 숫자의 데이터형태로 저장한다.
        - Primary Key로 지정한다.
    2. 'id' : 보통 id라고 식별되는 컬럼. 간편로그인 기능을 지원하지 않기 때문에, 해당 컬럼은 Not Null속성이 지정되어야 한다.
        - varchar(255)자로 저장한다.
        - 반드시 채워져있어야 한다.
    3. 'pw' : 보통 password로 식별되는 컬럼. 빈 값으로 존재해선 안된다.
        - Varchar(255)자로 저장한다.
        - 반드시 채워져 있어야 한다.
        - 보안을 위해, 해당 필드는 절대로 평문저장을 진행해선 안된다.

### About User

- 테이블 'user_bookmarks'는 아래와 같이 정의한다.
    1. 'uid' : 식별자로 테이블 'user_info'의 'uid'와 동일하다.
        - FK와 PK 동시속성을 가진다.
    - 이 이하는 회의를 통해 추가한다.

- 테이블 'manager_bookmarks'는 아래와 같이 정의한다.
    1. 'mid' : 식별자로 테이블 'manager_info'의 'mid'와 동일하다.
        - FK와 PK 동시속성을 가진다.
    - 이 이하는 회의를 통해 추가한다.

- 테이블 'manager_fastival'는 아래와 같이 정의한다.
    - 회의를 통해 추가필요.

### About API

- 테이블 'parkingarea_info'는 아래와 같이 정의한다.
    1. 'pid' : 식별자로 삽입시 자동 증가되도록 설정한다.
    2. 'park_id' : 주차장 관리번호.
        - Primary Key로 설정한다.
    3. 'park_nm' : 주차장 이름. 없는 경우도 있어서 삽입시 어떻게 처리할지 논의가 필요함.
    4. 'park_addr' : 주차장 주소.
    5. 'park_lo' : 주차장 주소에 대한 위도
    6. 'park_la' : 주차장 주소에 대한 경도
    7. 'page_no' : API 재호출을 위한 해당 주차장 페이지번호

- 테이블 'parkingarea_opertime'은 아래와 같이 정의한다.
    1. 'park_id' : 외래키로 parkingarea_info의 park_id를 가져온다.
        - FK, PK 동시속성으로 설정한다.
    2. 'mon_opentime' : 월요일 운영시작시각
    3. 'mon_closetime' : 월요일 운영종료시각
    4. 'tue_opentime' : 화요일 운영시작시각
    5. 'tue_closetime' : 화요일 운영종료시각
    6. 'wed_opentime' : 수요일 운영시작시각
    7. 'wed_closetime' : 수요일 운영종료시각
    8. 'thu_opentime' : 목요일 운영시작시각
    9. 'thu_closetime' : 목요일 운영종료시각
    10. 'fri_opentime' : 금요일 운영시작시각
    11. 'fri_closetime' : 금요일 운영종료시각
    12. 'sat_opentime' : 토요일 운영시작시각
    13. 'sat_closetime' : 토요일 운영종료시각
    14. 'sun_opentime' : 일요일 운영시작시각
    15. 'sun_closetime' : 일요일 운영종료시각
    16. 'holi_opentime' : 휴일 운영시작시각
    17. 'holi_closetime' : 휴일 운영종료시각

- 테이블 'parkingarea_operfee'는 아래와 같이 정의한다.
    1. 'park_id' : 외래키로 parkingarea_info의 park_id를 가져온다.
        - FK, PK 동시속성으로 설정한다.
    2. 'free_time' : 기본시간
    3. 'basic_fee' : 기본요금
    4. 'adit_time' : 추가 단위시간
    5. 'adit_fee' : 추가 단위시간당 요금
    6. 'daily_fee' : 1일권 요금
    7. 'monthly_fee' : 1달정액권 요금

- 테이블 'festival_info'는 아래와 같이 정의한다.
    1. 'fid' : index. 삽입시 자동증가되도록 설정한다.
        - Primary Key로 설정한다.
    2. 'title' : 행사 제목
    3. 'address' : 행사 진행 주소
    4. 'eventstartdate' : 행사 시작일
    5. 'eventenddate' : 행사 종료일
    6. 'tel' : 행사 대표번호
    7. 'firstimage' : 행사 메인 화면으로 이미지 저장된 주소를 입력
    8. 'firstimage2' : 행사 썸네일 화면으로 이미지 저장된 주소를 입력
    9. 'mapx' : 행사 주소의 좌표 중 위도
    10. 'mapy' : 행사 주소의 좌표 중 경도


