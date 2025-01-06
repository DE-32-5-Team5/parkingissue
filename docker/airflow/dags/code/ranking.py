import os
import json
import csv
import boto3
from kafka import KafkaConsumer
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def fun_con():
    """
    Kafka 메시지를 읽고 마지막 오프셋으로 이동.
    - 실행 시점까지 쌓인 모든 메시지를 읽고 오프셋 이동.
    - 실행 도중 새로 들어오는 메시지는 무시.
    """
    # KafkaConsumer 설정
    consumer = KafkaConsumer(
        bootstrap_servers=['10.0.4.172:29091'],
        auto_offset_reset='earliest',  # 가장 오래된 메시지부터 읽기
        enable_auto_commit=False,      # 자동 커밋 비활성화 (명시적 커밋 사용)
        group_id='fiveguys',           # 그룹 ID 설정
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # JSON 역직렬화
    )

    # 토픽 구독
    consumer.subscribe(['search'])

    # Rank 디렉토리 없으면 생성
    dir_path = "/opt/airflow/Rank"
    if not os.path.exists(dir_path):
        of.mkdir(dir_path)

    file_path=os.path.join(dir_path, "search.csv")


    try:
        print(f" --------- Consuming messages from Kafka  ---------")

        # 현재 할당된 파티션의 마지막 오프셋 가져오기
        records = consumer.poll(timeout_ms=10000)  # 파티션 초기화
        #print(f" ####### ")
        #print(records)
        end_offsets = consumer.end_offsets(consumer.assignment())

        # None 값 또는 비어 있는 파티션 처리
        if not end_offsets or any(offset is None for offset in end_offsets.values()):
            raise ValueError("오프셋을 가져오는 데 실패했습니다 .")

        #print(f"마지막 오프셋 : {end_offsets}")

        # 메시지 소비
        while True:
            #records = consumer.poll(timeout_ms=10000)  # 메시지를 배치로 가져옴

            if not records:
                print("가져올 메시지가 없습니다. 종료 !!!")
                break

            msg_list = []
            for partition, messages in records.items():
                for message in messages:
                    try:
                        # 메시지 처리 로직
                        print("*********************")
                        print(f"Message: {message.value}")
                        print("*********************")
                        msg_list.append(message.value.get('search_msg'))

                        # 메시지 처리 후 오프셋 커밋
                        consumer.commit()

                        print(f" 현재 오프셋 : {message.offset}             마지막 오프셋:{end_offsets[partition]}")
                        # 새 메시지가 마지막 오프셋 이후라면 종료
                        if message.offset == end_offsets[partition]-1:
                            print(f" 마지막 메시지까지 모두 읽었습니다. 종료 !!!.")
                            save_to_csv(file_path, msg_list)
                            return

                    except json.JSONDecodeError as e:
                        print(f"JSON Decode Error: {e}")
                        print(f"Raw Message: {message.value}")
                    except UnicodeEncodeError as e:
                        print(f"Unicode encoding error: {e}")
                    except Exception as e:
                        print(f"Unexpected error occurred while processing message: {e}")

    except Exception as e:
        print(f"Kafka consumer failed: {e}")

    finally:
        # Consumer 종료
        print("Closing Kafka consumer.")
        consumer.close()


def save_to_csv(file_path, data_list):
    """
    데이터를 CSV 파일로 저장하는 함수.

    :param file_path: 저장할 CSV 파일 경로
    :param data_list: 저장할 데이터 리스트 (딕셔너리 형태로 구성)
    """
    print(f"####### {file_path} ######")
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['search_msg'])
            writer.writeheader()
            writer.writerows({'search_msg': item} for item in data_list)
            print(f"파일이 성공적으로 저장되었습니다: {file_path}")
    except FileNotFoundError as e:
        print(f"파일 경로를 찾을 수 없습니다: {e}")
    except PermissionError as e:
        print(f"파일 쓰기 권한이 없습니다: {e}")
    except IOError as e:
        print(f"파일 쓰기 중 입출력 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"예기치 못한 오류가 발생했습니다: {e}")


def fun_s3():
    """
    로컬 CSV 파일을 S3 버킷에 업로드합니다.
    - bucket_name: S3 버킷 이름
    - file_key: S3에 저장될 파일 경로
    - file_path: 로컬 CSV 파일 경로
    """
    try:
        s3_hook = S3Hook(aws_conn_id='aws_default')
        s3_hook.load_file(
            filename='/opt/airflow/Rank/search.csv',
            key='search/search.csv',
            bucket_name='fiveguys-s3',
            replace=True
        )
        print("s3 업로드 성공.")

    except Exception as e:
        print(f"s3 업로드 중 문제 발생 : {e}")

def fun_from_s3():
    """
    S3에서 데이터를 다운로드하는 함수
    :param bucket_name: S3 버킷 이름
    :param key: S3 객체 키 (파일 경로)
    :param download_path: 로컬에 저장할 파일 경로
    """
    key = 'search/rank.csv'
    bucket_name = 'fiveguys-s3'
    download_path = '/opt/airflow/Rank/rank.csv'

    hook = S3Hook(aws_conn_id='aws_default')  # Airflow 연결 ID 사용
    hook.get_key(key, bucket_name=bucket_name).download_file(download_path)

    print(f"s3 파일 다운로드 성공 !!")
