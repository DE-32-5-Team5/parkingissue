# DevNote
- RDD : [RDD for Database](https://github.com/DE-32-5-Team5/parkingissue/blob/document/document/4_Requirements_Definition_Document_of_Database.md)

## 데이터베이스 구축

- 구축환경 : Docker
- Log 추적 및 데이터 저장을 위한 Log 테이블 별도 생성
- Dockerfile을 통한 구동 성공 및 테이블 정상 삽입 확인.

## 데이터베이스 접속

``` bash
$ pwd
<your>/<installation>/<dir>/parkingissue/docker/database

$ docker build --build-arg MYSQL_ROOT_PASSWORD=<root_password>--build-arg MYSQL_DATABASE=parkingissue -t parkingissuedb:0.1.0 .

$ docker run parkingissuedb:0.1.0
```