# DevNote
- RDD : [RDD for Database](https://github.com/DE-32-5-Team5/parkingissue/blob/document/document/4_Requirements_Definition_Document_of_Database.md)

## 데이터베이스 구축

- 구축환경 : Docker
- Log 추적 및 데이터 저장을 위한 Log 테이블 별도 생성
- Dockerfile을 통한 구동 성공 및 테이블 정상 삽입 확인.

## 데이터베이스 접속

``` bash
$ pwd
<your>/<installation>/<dir>/parkingissue/docker

$ docker compose -f db-compose.yml up -d
[+] Running 2/2
 ✔ Network docker_default           Created                                                                        0.2s
 ✔ Container parkingissue_database  Started                                                                        0.4s
```

### env setting

``` bash
$ pwd
<your>/<installation>/<dir>/parkingissue/docker

$ cat .db_env
MYSQL_ROOT_PASSWORD=<password_1>
MYSQL_DATABASE=<password_2>
LOGIN_PASSWORD=<password_3>
USER_PASSWORD=<password_4>
EXPORTER_PASSWORD=<password_5>
AIRFLOW_PASSWORD=<password_6>
```

- 비밀번호는 별도의 문서 확인바람.