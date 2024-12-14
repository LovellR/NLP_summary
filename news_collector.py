import pymysql
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def collect_news():

    # 현재 시간을 가져와서 분과 초를 0으로 설정
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    # 데이터베이스 연결 설정
    conn = pymysql.connect(host='localhost', port=3305, user='root', password='root', db='issue', charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 조건부 SQL 쿼리 실행
        #cur.execute("SELECT `idkeyword`, `word` FROM keyword WHERE `time` = '2024-12-12 19:00:00'")
        cur.execute("SELECT `idkeyword`, `word` FROM keyword WHERE `time` = ", (now.strftime('%Y-%m-%d %H:%M:%S'),))
        keywords = cur.fetchall()

        # 웹드라이버 설정
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("lang=ko_KR")
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        driver = webdriver.Chrome('chromedriver-win64\chromedriver.exe', chrome_options=options)

        for keyword in keywords:
            search_query = keyword['word']
            base_url = f"https://search.naver.com/search.naver?where=news&query={search_query}&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0&office_category=0&service_area=0"
            driver.get(base_url)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/section/div[1]/div[2]/ul/li'))
            )

            news_count = len(driver.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/section/div[1]/div[2]/ul/li'))

            print(news_count)

            for index in range(1, news_count + 1):
                try:
                    xpath = f'/html/body/div[3]/div[2]/div[1]/div[1]/section/div[1]/div[2]/ul/li[{index}]/div[1]/div/div[2]/a[2]'
                    anchor = driver.find_element(By.XPATH, xpath)
                    href = anchor.get_attribute('href')
                    text = anchor.text
                    print(text)

                    driver.get(href)
                    
                    try:
                        # 첫 번째 시도
                        content = driver.find_element(By.XPATH, "//*[@itemprop='articleBody']").text
                    except NoSuchElementException:
                        try:
                            content = driver.find_element(By.ID, "articleText").text
                        except NoSuchElementException:
                            try:
                                content = driver.find_element(By.CLASS_NAME, "news_contents").text
                            except NoSuchElementException:
                                try:
                                    content = driver.find_element(By.CLASS_NAME, "view_article").text
                                except NoSuchElementException:
                                    try:
                                        content = driver.find_element(By.CLASS_NAME, "read").text
                                    except NoSuchElementException:
                                        content = "Content not found"
                    
                    if len(content) > 3333:
                        continue
                    print(content)
                    driver.back()

                    # 검색된 내용을 데이터베이스에 저장
                    cur.execute("INSERT INTO news (`idkeyword`, `content`) VALUES (%s, %s)", (keyword['idkeyword'], content))
                    conn.commit()
                except NoSuchElementException:
                    print(f"No such element for index {index}, skipping...")
                    continue
        driver.quit()

    finally:
        conn.close()

if __name__ == '__main__':
    collect_news()
