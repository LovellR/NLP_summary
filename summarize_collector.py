import requests
import pymysql
from datetime import datetime


def collect_summary():
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

    # API 엔드포인트 URL
    url = "http://175.205.226.157:5000/summarize"

    try:
        # `keyword` 테이블에서 조건에 맞는 키워드 가져오기
        #cur.execute("SELECT `idkeyword`, `word` FROM keyword WHERE `time` = '2024-12-12 19:00:00'")
        cur.execute("SELECT `idkeyword`, `word` FROM keyword WHERE `time` = %s", (now.strftime('%Y-%m-%d %H:%M:%S'),))
        keywords = cur.fetchall()

        if not keywords:
            print("조건에 맞는 키워드가 없습니다.")
            exit()

        # 각 키워드에 대해 관련 뉴스 가져오기
        for keyword in keywords:
            idkeyword = keyword['idkeyword']

            cur.execute("SELECT `idnews`, `idkeyword`, `content` FROM news WHERE `idkeyword` = %s", (idkeyword,))
            news_list = cur.fetchall()

            if not news_list:
                print(f"키워드 {idkeyword}에 대한 뉴스가 없습니다.")
                continue

            # 각 뉴스에 대해 API 요청 및 요약 결과 처리
            for news in news_list:
                text = news['content']

                if text.strip().lower() == "content not found":
                    print(f"뉴스 ID {news['idnews']}의 내용이 'Content not found'입니다. 건너뜁니다.")
                    continue

                # 전송할 데이터
                data = {
                    "text": text
                }

                try:
                    # POST 요청 보내기
                    response = requests.post(url, json=data)

                    # 응답 확인 및 처리
                    if response.status_code == 200:
                        try:
                            summary = response.json().get("summary")
                            print(f"요약 결과: {summary}")

                            try:
                                # 요약 결과를 데이터베이스에 저장
                                try:
                                    cur.execute(
                                        "INSERT INTO summary (`idnews`, `summary`) VALUES (%s, %s)", 
                                        (news['idnews'], summary)
                                    )
                                    conn.commit()  # 데이터베이스 변경 사항 저장
                                except pymysql.DataError as e:  # 데이터 길이 초과 등 데이터 관련 오류 처리
                                    print(f"데이터베이스 삽입 오류 - 뉴스 ID {news['idnews']}: {e}")
                                    continue
                                except pymysql.MySQLError as e:  # 기타 MySQL 관련 오류 처리
                                    print(f"데이터베이스 예외 발생 - 뉴스 ID {news['idnews']}: {e}")
                                    continue
                            except Exception as e:
                                print(f"예기치 않은 오류 발생 - 뉴스 ID {news['idnews']}: {e}")
                                continue

                        except ValueError:  # JSON 디코딩 실패 시
                            print(f"JSON 디코딩 실패 - 뉴스 ID {news['idnews']}: 응답 내용이 비어있거나 유효하지 않습니다.")
                            continue
                    else:
                        print(f"요약 요청 실패 - 뉴스 ID {news['idnews']}: {response.status_code}, {response.text}")
                        continue
                except requests.exceptions.RequestException as e:
                    print(f"요약 요청 중 예외 발생 - 뉴스 ID {news['idnews']}: {e}")
                    continue

    except Exception as e:
        print("오류 발생:", e)
        

    finally:
        # 커넥션 닫기
        conn.close()

if __name__ == '__main__':
    collect_summary()