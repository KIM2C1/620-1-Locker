import mysql.connector

# 데이터베이스 연결 구성
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'wpqkf',
}

try:
    # 데이터베이스 연결
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        cursor = connection.cursor()

        # 데이터베이스와 테이블 이름
        database_name = 'wpqkf'
        table_name = 'wpqkf_log'

        # 테이블 내용을 가져오는 쿼리
        query = f"SELECT * FROM {database_name}.{table_name};"

        # 쿼리 실행
        cursor.execute(query)

        # 결과 가져오기
        table_contents = cursor.fetchall()

        # 테이블 내용 출력
        print(f"{table_name} 테이블 내용:")
        for row in table_contents:
            print(row)

except mysql.connector.Error as err:
    print(f"오류: {err}")

finally:
    # 연결 종료
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("데이터베이스 연결 종료.")
