FROM python:3.9

ARG MYSQL_DATABASE
ARG LOGIN_PASSWORD
ARG USER_PASSWORD

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .


ENV MYSQL_DATABASE = parkingissue
ENV LOGIN_PASSWORD = ${LOGIN_PASSWORD}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4090"]
