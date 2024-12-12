import pymysql
from datetime import datetime

# 현재 시간을 가져와서 분과 초를 0으로 설정
now = datetime.now().replace(minute=0, second=0, microsecond=0)

# 데이터베이스 연결 설정
conn = pymysql.connect(host='localhost', port=3305, 
                       user='root', 
                       password='root', 
                       db='issue', 
                       charset='utf8')

# 커서 생성
cur = conn.cursor(pymysql.cursors.DictCursor)

try:
    # 조건부 SQL 쿼리 실행, 현재 시간에서 분과 초를 0으로 한 시간을 조건으로 사용
    cur.execute("SELECT `idkeyword`, `word`, `site`, `rank`, `time` FROM keyword WHERE `time` = %s", (now.strftime('%Y-%m-%d %H:%M:%S'),))

    # 결과 모두 가져오기
    rows = cur.fetchall()

    # 결과 출력
    for row in rows:
        print(f"ID: {row['idkeyword']}, Word: {row['word']}, Site: {row['site']}, Rank: {row['rank']}, Time: {row['time']}")

finally:
    # 커넥션 닫기
    conn.close()
