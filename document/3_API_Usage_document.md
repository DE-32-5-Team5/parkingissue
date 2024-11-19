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


## 4. Festival Search API
- 행사/공연/축제 정보를 날짜로 조회하는 기능입니다.
콘텐츠 타입이 “행사/공연/축제”인 경우만 유효합니다.
파라미터에 따라 제목순, 수정일순(최신순), 등록일순  정렬 검색을 제공합니다.
- Request URL : [http://apis.data.go.kr/B551011/KorService1/searchFestival1]()

    - 필수 parameter

    항목명(영문) | 항목명(국문) | 샘플데이터 | 항목설명
    :---|:---|:---|:---
    serviceKey|인증키(서비스키)|인증키|공공데이터포털에서 받은 인증키
    MobileApp|서비스명|AppTest|서비스명=어플명
    MobileOS|OS 구분|ETC|IOS, AND, WIN, ETC
    eventStartDate|행사 시작일|20241119|행사 시작일 (YYYYMMDD)

    - 부가 parameter

    항목명(영문) | 항목명(국문) | 샘플데이터 | 항목설명
    :---|:---|:---|:---
    numOfRows|한페이지결과수|10|한페이지결과수
    pageNo|페이지번호|1|페이지번호
    _type|응답메세지 형식|json|REST방식의 URL호출시 Json깂추가(디폴트 응답메세시 형식은XML)
    listYN|목록구분|Y/N|목록구분(Y=목록, N=개수)
    arrange|정렬구분|A|(A=제목순, C=수정일순, D=생성일순)       대표이미지가 반드시 있는 정렬(O=제목순, Q=수정일순, R=생성일순)


    - parameter : listYN=N 일 경우

    항목명(영문) | 항목명(국문) | 샘플데이터 | 항목설명
    :---|:---|:---|:---
    totalCnt|결과리스트갯수|1234|리턴된 리스트 갯수

    - parameter : listYN=Y 일 경우

    항목명(영문) | 항목명(국문) | 샘플데이터 | 항목설명
    :---|:---|:---|:---
    resultCode  |결과코드       |0000   |응답결과코드
    resultMsg   |결과메시지     |OK     |응답결과메시지
    numOfRows   |한페이지결과수 |10     |한페이지결과수
    pageNo      |페이지번호     |1      |현재페이지번호
    totalCount	|전체결과수	    |758     |전체결과수
    addr1       |주소           |충청남도 부여군 규암면 백제문로 388|주소(예, 서울중구다동)를응답
    addr2       |상세주소       |	-	|상세주소
    areacode    |지역코드       |34     |지역코드
    booktour    |교과서속여행지여부|0   |교과서속여행지여부(1=여행지, 0=해당없음)
    cat1	    |대분류	        |A02	|대분류코드
    cat2	    |중분류	        |A0208	|중분류코드
    cat3	    |소분류	        |A02080100	|소분류코드
    contentid	|콘텐츠ID	    |1258353	|콘텐츠ID
    contenttypeid|콘텐츠타입ID	|15	        |관광타입(관광지, 숙박등) ID
    createdtime     |등록일         |20110418095420|콘텐츠최초등록일
    eventstartdate  |행사시작일	    |20210306              |행사시작일(형식 : YYYYMMDD)
    eventenddate    |행사종료일	    |	20211030         |	행사종료일(형식 : YYYYMMDD)
    firstimage      |대표이미지(원본)|  http://tong.visitkorea.or.kr/cms/resource/54/2483454_image2_1.JPG	|원본대표이미지 (약 500*333 size) URL 응답
    firstimage2	    |대표이미지(썸네일)	|http://tong.visitkorea.or.kr/cms/resource/54/2483454_image2_1.JPG|	썸네일대표이미지(약 150*100 size) URL 응답
    cpyrhtDivCd	    |저작권 유형	|Type1	|Type1:제1유형(출처표시-권장) Type3:제3유형(제1유형 + 변경금지)
    mapx    |GPS X좌표      |126.8997016069	|GPS X좌표(WGS84 경도좌표) 응답
    mapy	|GPS Y좌표		|36.3048428766	|GPS Y좌표(WGS84 위도좌표) 응답
    mlevel	|Map Level		|6	|Map Level 응답
    modifiedtime	|수정일		|20210226112411	|콘텐츠수정일
    sigungucode	|시군구코드		|6	|시군구코드
    tel	|전화번호		|041-832-5765	|전화번호
    title	|제목		|가무악극으로 만나는 토요 상설공연  |콘텐츠제목

### 사용방안

- 먼저, 우리가 만들 행사장 정보를 종합해보면
    - 위치가 명확해야 하며,
    - 검색이 용이해야 하고,
    - 그 외의 부가정보는 상세정보에서 확인해야 한다.

    - 사용하지 않는 변수를 제거해서 보면

    #### festival_info

    항목명(영문) | 항목명(국문)
    :---|:---
    title | 행사 제목
    addr | 행사 주소 (addr1 + addr2)
    eventstartdate | 행사 시작일
    eventenddate | 행사 종료일
    firstimage | 대표 이미지
    firstimage2 | 썸네일 이미지
    mapx | 행사 위도
    mapy | 행사 경도
    tel | 행사 연락처

    다음의 정보들로 축약시켜 테이블에 저장할 수 있을 것으로 기대한다.







