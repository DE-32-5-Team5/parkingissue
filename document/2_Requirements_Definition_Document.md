# 0.1/loginpage

## Function Introduce
- 사용자가 본 프로젝트에 접근시 사용자 인증을 받는 로그인 화면

## Function Requirements
- 로그인을 담당하는 화면을 제작한다.
- 로그인에는 ID와 PW가 필요하다
- PW 입력창의 경우 어떤 값을 입력하더라도 ● 표시가 되어 입력한 값이 보이지 않도록 한다.
- 로그인 시도시 입력된 ID와 PW을 이용해 시도하며 이때, 보안을 위해 get, post등에 ID와 PW가 노출되지 않도록 한다.
- 로그인 화면은 아래와 같은 화면으로 구성되도록 한다.
![image](https://github.com/user-attachments/assets/703eaff8-c7ff-484a-9994-fdf2081c0a5b)
    1. 로고 (우선순위 낮음)
    2. ID 입력창
    3. PW 입력창
    4. 로그인 시도 버튼
    5. 회원가입 버튼 (우선순위 낮음)
    6. ID/PW찾기 버튼 (우선순위 낮음)

# 0.1/logindb
## Function Introduce
- 사용자가 본 프로젝트에 접근시 사용자 인증을 확인할 Database를 구현

## Function Requirements
- MariaDB를 이용한다.
- 이 화면에서 요청하는 DB에 접근할 user설정은 다음과 같이 진행한다
``` bash
$ mariadb -u login
```
- login 유저로 진행하는 경우 어떠한 수정, 쓰기등의 권한을 주지 않도록 주의한다.

- Database는 parkingissue를 사용한다.
``` mysql
> USE parkingissue;
```

- 로그인 기능과 상호작용할 테이블은 user로 둔다.
- 로그인 쿼리는 다음과 같이 짜되 가능하다면 query injection 공격을 방어할 수 있는 쿼리가 가능하다면 해당 코드로 변경한다.
``` mysql
> SELECT CASE WHEN EXISTS (
SELECT 1 
FROM user 
WHERE id = '<request_id>' AND pw = '<request_pw>'
) THEN 1 ELSE 0 END AS result;
```

## Architecture Requirements
- Docker Compose를 이용한다.
- 