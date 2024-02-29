from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 데이터베이스 연결 구성
db_config = {
    'host': '###t',
    'user': '###',
    'password': '###',
    'database': '###',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            selected_date = request.form['date']
            selected_employee = request.form['employee']
            if selected_employee == "":
                # "전체"가 선택된 경우 모든 직원의 로그를 조회합니다
                cursor.execute("SELECT * FROM wpqkf_log WHERE DATE(timestamp) = %s", (selected_date,))
            else:
                # 선택된 직원의 로그만 조회합니다
                cursor.execute("SELECT * FROM wpqkf_log WHERE DATE(timestamp) = %s AND employee_id = %s", (selected_date, selected_employee))
        else:
            # GET 요청인 경우 오늘 날짜의 모든 직원의 로그를 조회합니다
            cursor.execute("SELECT * FROM wpqkf_log WHERE DATE(timestamp) = CURDATE()")

        logs = cursor.fetchall()

        return render_template('wpqkf.html', logs=logs)

    except mysql.connector.Error as err:
        return f"오류: {err}"

    finally:
        # 데이터베이스 연결을 닫습니다.
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
