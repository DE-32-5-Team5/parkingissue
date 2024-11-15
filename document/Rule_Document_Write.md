# TODO
## Branch 부여 규칙

- 기능 구현은 0.1단위로 진행
    - ex. 0.1/login

- 기능 구현이 완료된 branch는 해당 개발버전에 Pull Request 진행
    - ex. 0.1/login -> 0.1/dev

- 해당 버전의 dev branch에서 작동테스트와 기능간 테스트가 완료된 경우 DevNote.md 파일의 내용을 ReleaseNote.md에 추가하며 다른 기능들의 검수가 모두 통과될 시 release 버전으로 Pull Request를 진행한다.
    - ex. 0.1/login -> 0.1/dev
    - ex. 0.1/dbinit -> 0.1/dev
    - ex. 0.1/dev -> 0.1/release

- 해당 버전의 dev branch에서 작동테스트나 기능간 테스트가 실패할 시, dev branch는 해당 상태에서 bugfix branch를 생성하여 기능 개발자에게 전달한다.
    - ex. 0.1/login -> 0.1/dev가 실패시
    - ex. 0.1/dev -> 0.1/login_bugfix로 

- bugfix branch는 작업 완료시 dev branch에 Pull Request 진행한다. 이후 과정은 위와 동일하게 진행한다.
    - ex. 0.1/login_bugfix -> 0.1/dev -> 0.1/release


## README.md 작성 규칙
1. 소속 및 프로젝트 제목

2. 프로젝트 소개
    - 프로젝트 주제 소개 
    - 프로젝트 기획의 계기
    - 프로젝트 목표
    - 프로젝트의 기대 효과

3. 팀원 소개
    - 팀원, 역할, 담당업무를 테이블로 표시

4. 프로젝트 내용
    - 프로젝트 접근 유저 기준 프로젝트 구성
    - 프로젝트 구조 기준 프로젝트 구성
    - 프로젝트의 프로세스 소개
    - 사용된 기술 설명

5. 설치 방법
    - ReleaseNote 링크
    - 설치 방법 설명

6. 사용 방법
    - 사용 방법 설명

7. 참조 레퍼런스
    - 참조한 레퍼런스 링크

## DevNote.md 작성 규칙
- 해당 브랜치에서 요구사항 정의에 대한 issue 링크를 가장 위에 배치
- 해당 issue를 해결하기 위한 개발내용 설명
    - ex. 0.1/login DevNote.md
    ``` 
    0.1/login RDD link
    - id와 pw를 입력받아 사용자 정보 조회를 진행하는 버튼 생성
    - id를 입력받는 칸 하나, pw를 입력받는 칸 하나 총 2개의 입력칸을 받음.
    - 차후 manager와 user를 구별하기 위한 선택 창도 추가함.
    ```
- 해당 branch에서 dev branch로 PR진행시 버그로 문제가 발생했다면 해당 문서 하단에 0.0.1 단위로 발생한 문제와 해당 문제 해결에 대한 개발내용 설명을 추가한다.
    - ex. 0.1/login DevNote.md
    ```
    0.1/login RDD link
    - id와 pw를 입력받아 사용자 정보 조회를 진행하는 버튼 생성
    - id를 입력받는 칸 하나, pw를 입력받는 칸 하나 총 2개의 입력칸을 받음.
    - 차후 manager와 user를 구별하기 위한 선택 창도 추가함.

    0.1.1/login_bugfix
    - 제대로 id와 pw를 입력했음에도 로그인 정보를 확인하지 못함.
    - id값을 보낼 떄, id의 내용이 보내지는게 아닌 다른 값이 보내지고 있음.
    - id의 내용이 보내지도록 수정 완료.
    ```