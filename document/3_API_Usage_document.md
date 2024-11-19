# API Usage Document

## 1. Parking Area Infomation API
- [API Request URL](http://apis.data.go.kr/B553881/Parking)
- 3개의 부문으로 나뉘어짐
    - 주차장 시설정보 (PrkSttusInfo)
    - 주차장 운영정보 (PrkOprInfo)
    - 주차장 이용정보 (PrkRealtimeInfo)

### 주차장 시설정보
- 주차정보시스템에 수집된 전국 주차장 정보의 시설정보를 조회하는 기능
- Request URL : [http://apis.data.go.kr/B553881/Parking/PrkSttusInfo]()
- 아래 4가지 필수 입력사항 존재
    - serviceKey : 인증키
    - numOfRows  : 한 페이지의 결과 수
    - pageNo : 조회할 페이지 번호
    - format : 응답형식 (XML : 1, JSON : 2)

- 아래 표의 데이터 형식으로 데이터 콜백

|코드|변수명|설명|예시|
|:---|:---|:---|:---|
|resultCode|결과코드|결과코드|00|
|resultMsg|결과메세지|결과메세지|SUCCESS|
numOfRows|한 페이지 결과 수|한 페이지 결과 수|10
pageNo|페이지 수|조회된 페이지 번호|1
totalCount|데이터 총 개수|데이터 총 개수|100
PrkSttusInfo|주차장정보 리스트|주차장정보 리스트|
prk_center_id|주차장 관리 ID   (또는 확장ID) |주차장 관리 ID   (또는 확장ID) |12345-67890-12345-12-1
prk_plce_nm|주차장명|주차장명|서울시 망원동 주차장
prk_plce_adres|주차장 도로명 주소   (도로명주소 공백 시 지번주소) |주차장 도로명 주소   (도로명주소 공백 시 지번주소) | 서울시 망원동 월드컵로 1길|
prk_plce_entrc_la|위도| 주차장 좌표 : 위도 | 35.879337
prk_plce_entrc_lo|경도| 주차장 좌표 : 경도 | 128.628764
prk_cmprt_co|주차장의 총 주차 구획 수 | 주차장의 총 주차 구획 수| 100

### 사용방안
- 현재 해당 API 호출로는 Database에 Insert or Update를 통해 해당 주차장 정보들을 주입하는 방법이 유리할 것으로 사료됨.
- 이를 통해 데이터베이스 테이블 parkingarea_info에는 다음의 정보들이 필요할 것으로 생각됨
    #### parkingarea_info

    코드명|변수명
    :---|:---
    index | 숫자 (자동증가)
    prk_center_id | 주차장 관리 id
    prk_plce_nm | 주차장명
    prk_plce_adres | 주차장 주소
    prk_plce_entrc_la | 위도
    prk_plce_entrc_lo | 경도
    page | 해당 데이터가 위치되어 있는 페이지 (pageNo와 동일)

## 2. Parking Area Operation API
- 주차정보시스템에 수집된 전국 주차장 정보의 시설정보를 조회하는 기능.
- Request URL : [http://apis.data.go.kr/B553881/Parking/PrkOprInfo]()
- 아래 4가지 필수 입력사항 존재
    - serviceKey : 인증키
    - numOfRows  : 한 페이지의 결과 수
    - pageNo : 조회할 페이지 번호
    - format : 응답형식 (XML : 1, JSON : 2)

- 아래 표의 데이터 형식으로 데이터 콜백

|코드|변수명|설명|예시|
|:---|:---|:---|:---|
resultCode|결과코드|결과코드|00
resultMsg|결과메세지|결과메세지|SUCCESS
numOfRows|한 페이지 결과 수|한 페이지 결과 수|10
pageNo|페이지 수|조회된 페이지 번호|1
totalCount|데이터 총 개수|데이터 총 개수|100
prk_center_id|주차장 관리 ID|주차장 관리 ID|12345-67890-12345-12-1
Monday ~ Sunday | 요일 | 요일별 주차장 운영시간 |
Holiday | 휴일 | 휴일 주차장 운영시간 |
opertn_start_time | 운영시작 시각 | 주차장 운영 시작 시각 | 080000 
opertn_end_time | 운영종료 시각 | 주차장 운영 종료 시각 | 200000
opertn_bs_free_time | 주차장 기본회차(기본무료)시간 | 주차장 기본회차(기본무료)시간 | 30
parking_chrge_bs_time | 주차장 기본시간 | 주차장 기본시간 | 30
parking_chrge_bs_chrg | 주차장 기본요금 | 주차장 기본요금 | 1500
parking_chrge_adit_unit_time | 주차장 추가단위시간 | 주차장 추가단위 시간 | 30 
parking_chrge_adit_unit_chrge | 주차장 추가 단위시간당 요금 | 주차장 추가 단위시간당 요금 | 1000
parking_chrge_one_day_chrge | 1일 정액권 금액 | 1일 정액권 금액 문의 | 10000
parking_chrge_mon_unit_chrge | 1달 정액권 금액 | 1달 정액권 금액 | 250000

### 사용방안
- 해당 API 자료들은 준 고정된 형태로 고객이 정보 탐색차 요청이 빈번할 것으로 보임
- 따라서 해당 내용을 일일히 API 요청하는것보다 API의 값을 DB에 설치해서 유저 요청시 DB에서 가져오는것이 효율적일 것으로 사료됨
- 이를 통해 데이터베이스 테이블을 두개로 만들어서 시간대별 운영정보와 가격별 운영정보를 분리해 저장하는 식으로 진행할 것을 추천함.
    #### parkingareaoper_time

    코드명|변수명
    :---|:---
    prk_center_id | 주차장 관리 id
    Mo_open_time | 월요일 운영시작 시각
    Mo_close_time | 월요일 운영종료 시각
    Tu_open_time | 화요일 운영시작 시각
    Tu_close_time | 화요일 운영종료 시각
    We_open_time | 수요일 운영시작 시각
    We_close_time | 수요일 운영종료 시각
    Th_open_time | 목요일 운영시작 시각
    Th_close_time | 목요일 운영종료 시각
    Fr_open_time | 금요일 운영시작 시각
    Fr_close_time | 금요일 운영종료 시각
    Sa_open_time | 토요일 운영시작 시각
    Sa_close_time | 토요일 운영종료 시각
    Su_open_time | 일요일 운영시작 시각
    Su_close_time | 일요일 운영종료 시각
    Ho_open_time | 휴일 운영시작 시각
    Ho_close_time | 휴일 운영종료 시각


    #### parkingareaoper_fee

    코드명|변수명
    :---|:---
    prk_center_id | 주차장 관리 id
    opertn_bs_free_time | 주차장 기본 시간
    parking_chrge_bs_chrg | 주차장 기본요금
    parking_chrge_adit_unit_time | 주차장 추가 단위시간 
    parking_chrge_adit_unit_chrge | 주차장 추가요금
    parking_chrge_one_day_chrge | 1일 정액권 가격
    parking_chrge_mon_unit_chrge | 1달 정액권 가격

## 3. Parking Area Realtime API
- 주차정보시스템에 수집된 전국 주차장 정보의 실시간 주차면수 정보를 조회하는 기능
- Request URL : [http://apis.data.go.kr/B553881/Parking/PrkRealtimeInfo]()
- 아래 4가지 필수 입력사항 존재
    - serviceKey : 인증키
    - numOfRows  : 한 페이지의 결과 수
    - pageNo : 조회할 페이지 번호
    - format : 응답형식 (XML : 1, JSON : 2)

- 아래 표의 데이터 형식으로 데이터 콜백

|코드|변수명|설명|예시|
|:---|:---|:---|:---|
resultCode|결과코드|결과코드|00
resultMsg|결과메세지|결과메세지|SUCCESS
numOfRows|한 페이지 결과 수|한 페이지 결과 수|10
pageNo|페이지 수|조회된 페이지 번호|1
totalCount|데이터 총 개수|데이터 총 개수|100
prk_center_id|주차장 관리 ID|주차장 관리 ID|12345-67890-12345-12-1
pkfc_ParkingLots_total | 주차장 주차가능 총 구획 수 | 주차장 주차가능 총 구획 수 | 140
pkfc_Available_ParkingLots_total | 주차장의 총 주차가능 구획 수 | 주차장의 총 주차가능 구획 수 | 42

### 사용방안
- 가장 많이 사용될 것으로 보이는 API로 최대한 효율적으로 사용되게끔 요청을 보내야 할 것으로 사료됨. (해당부분은 논의가 필요)
- 데이터베이스에는 테이블 하나를 삽입하여 사용하는것이 좋아보임.
    #### parkingarea_realtime

    코드명|변수명
    :---|:---
    prk_center_id | 주차장 관리 ID
    pkfc_ParkingLots_total | 주차장 주차가능 총 구획 수
    pkfc_Available_ParkingLots_total | 주차장의 총 주차가능 구획 수


## 4. 
