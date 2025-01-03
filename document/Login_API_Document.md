# Login API Usage Document

## Introduce

- 본 문서는 로그인 로직에 대한 사용 설명서로써 API 사용 방법과 개발 사유에 대해 적혀있습니다.


## Login Services
### Personal Login Service

- 호출 함수명 : login_personal_service()
- 호출 필요 인자 : personal_user_model (Model) - user_id, user_pw
- 호출 엔드포인트 : api/login/common/personal
- 기능 : 일반회원의 id, pw기반 로그인 시도시 사용자 인증을 담당
- 반환 값 : 인증 성공시 JWT 토큰을 반환, 그렇지 않을 경우 HTTP 예외 에러를 반환

- 사용 구역 : login page에서만 사용.


### Enterprise Login Service

- 호출 함수명 : login_enterprise_service()
- 호출 필요 인자 : enterprise_user_model (Model) - manager_id, manager_pw
- 호출 엔드포인트 : api/login/common/enterprise
- 기능 : 기업회원의 id, pw기반 로그인 시도시 사용자 인증을 담당
- 반환 값 : 인증 성공시 JWT 토큰을 반환, 그렇지 않을 경우 HTTP 예외 에러를 반환

- 사용 구역 : login page에서만 사용.

### Naver Simple Login Service

- 호출 함수명 : login_naver_service()
- 호출 필요 인자 : naver_user_model (Model) - naver_id
- 호출 엔드포인트 : api/login/simple/naver
- 기능 : 네이버 간편 로그인 인증을 통과한 유저가 해당 네이버 계정을 통해 접속 시도시 사용자 인증을 담당
- 반환 : 인증 성공시 JWT 토큰을 반환, 그렇지 않을 경우 HTTP 예외 에러를 반환 (현재는 304 Redirect로 회원가입 페이지로 자동전환)

- 사용 구역 : logincallback/naver.html 페이지에서만 사용

### Kakao Simple Login Service
- 호출 함수명 : login_kakao_service()
- 호출 필요인자 : kakao_user_model (Model) - kakao_id
- 호출 엔드포인트 : api/login/simple/kakao
- 기능 : 카카오 간편 로그인 인증을 통과한 유저가 해당 카카오 계정을 통해 접속 시도시 사용자 인증을 담당
- 반환 : 인증 성공시 JWT 토큰을 반환, 그렇지 않을 경우 HTTP 예외 에러를 반환 (현재는 304 Redirect로 회원가입 페이지로 자동전환, 해당 페이지 개발중)

- 사용 구역 : logincallback/kakao.html 페이지에서만 사용 (개발중)

## Authentication Services
### Authentication Token Creation Service
- 호출 함수명 : create_jwt_token()
- 호출 필요 인자 : user_information & encode_information
- 호출 엔드포인트 : Not Exist
- 기능 : 로그인 성공한 유저일 경우 해당 유저의 정보를 담은 토큰을 발급해 반환하는 역할을 담당
- 반환 : JWT 토큰

- 사용 구역 : login 페이지에서만 사용

### Authentication Token Refresh Service
- 호출 함수명 : check_user_service()
- 호출 필요 인자 : user's authentication token (JWT Token)
- 호출 엔드포인트 : api/login/isuser
- 기능 : 토큰을 검증하여 유저의 정보를 반환 
- 반환 값 : user_verified_code (int)

- 사용 구역 : front 화면전환시 사용되어야 함함

### User Token Authentication Service
- 호출 함수명 : update_token_service()
- 호출 필요 인자 : user's authentication token (JWT Token)
- 호출 엔드포인트 : api/login/refreshtoken
- 기능 : 동일한 토큰에 만료일자를 새로 부여해 반환
- 반환 값 : new_user_authentication token (JWT Token)

- 사용 구역 : Authentication Token Refresh Service 호출 이후 정상 유저일시 호출되어 토큰 갱신

### User Information Decode Service
- 호출 함수명 : decode_user_information_service()
- 호출 필요 인자 : user's authentication token (JWT Token)
- 호출 엔드포인트 : api/login/decodeinfo
- 기능 : 필요시 토큰을 전송해 사용자 정보를 반환받는 역할
- 반환 값 : dict : user_id & user_type

- 사용 구역 : mypage 페이지에서 사용자 정보를 받아와야할때 사용용
