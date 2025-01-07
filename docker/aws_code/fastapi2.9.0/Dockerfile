FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y vim

COPY . /app/

# 환경 변수 설정
ENV JWT_LOGIN_ACCESS_KEY=$JWT_LOGIN_ACCESS_KEY \
    DB_HOST=$DB_HOST \
    DB_NAME=$DB_NAME \
    DB_PORT=$DB_PORT \
    DB_USER_I=$DB_USER_I \
    DB_USER_II=$DB_USER_II \
    DB_USER_III=$DB_USER_III \
    DB_USER_IV=$DB_USER_IV \
    DB_USER_V=$DB_USER_V \
    DB_USER_VI=$DB_USER_VI \
    DB_USER_VII=$DB_USER_VII \
    DB_USER_VIII=$DB_USER_VIII \
    DB_USER_IX=$DB_USER_IX \
    DB_USER_X=$DB_USER_X \
    DB_USER_IPW=$DB_USER_IPW \
    DB_USER_IIPW=$DB_USER_IIPW \
    DB_USER_IIIPW=$DB_USER_IIIPW \
    DB_USER_IVPW=$DB_USER_IVPW \
    DB_USER_VPW=$DB_USER_VPW \
    DB_USER_VIPW=$DB_USER_VIPW \
    DB_USER_VIIPW=$DB_USER_VIIPW \
    DB_USER_VIIIPW=$DB_USER_VIIIPW \
    DB_USER_IXPW=$DB_USER_IXPW \
    DB_USER_XPW=$DB_USER_XPW \
    DB_STR_KEY=$DB_STR_KEY \
    KAKAO_REST=$KAKAO_REST

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
