import os
import mysql.connector
from openpyxl import Workbook
from datetime import datetime
from mysql.connector import Error
import time
from config.config import db_config


set_week = 6

set_hour = 23

set_minute = 55

def generate_file_name():
    """
    현재 날짜와 시간을 기반으로 파일 이름 생성
    """
    current_date_time = datetime.now()
    directory = '/home/620locker/excel'  # 원하는 디렉토리 경로로 수정
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = os.path.join(directory, current_date_time.strftime("log_%Y%m%d%H%M.xlsx"))
    return file_name

def export_to_excel():
    try:
        # MySQL 데이터베이스에 연결
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("MySQL에 연결되었습니다.")

        # SQL 쿼리 실행하여 아직 엑셀로 전송되지 않은 데이터 가져오기
        cursor = connection.cursor()
        query = "SELECT * FROM wpqkf_log WHERE sent_to_excel = 0"  # 전송되지 않은 데이터만 선택
        cursor.execute(query)
        data = cursor.fetchall()

        # 새로운 Excel 파일 생성
        wb = Workbook()
        ws = wb.active

        # 데이터 추가
        for row in data:
            # 데이터 중에서 sent_to_excel 열은 제외하고 추가
            row_without_columns = [value for idx, value in enumerate(row) if idx != 4]  # sent_to_excel은 5번째 열
            ws.append(row_without_columns)

        # 파일 저장
        file_name = generate_file_name()
        wb.save(file_name)
        print(f"새로운 데이터를 {file_name} 파일에 추가 완료")

        # 전송이 완료된 데이터에 대해 플래그를 업데이트
        update_query = "UPDATE wpqkf_log SET sent_to_excel = 1 WHERE sent_to_excel = 0"
        cursor.execute(update_query)
        connection.commit()

    except Error as e:
        print(f"MySQL 오류: {e}")
    except Exception as e:
        print(f"예외가 발생했습니다: {e}")

    finally:
        # 데이터베이스 연결 닫기
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 연결이 닫혔습니다.")

while True:
    current_time = datetime.now()
    if current_time.weekday() == set_week and current_time.hour == set_hour and current_time.minute == set_minute:
        export_to_excel()
        break
    else:
        time.sleep(30)  # 60초(1분)마다 현재 시간을 확인합니다.
