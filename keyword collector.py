import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

def collect_keywords():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    
    driver = webdriver.Chrome('chromedriver-win64/chromedriver.exe', options=options)
    driver.get('https://zum.com/')

    ActionChains(driver).move_by_offset(797, 147).perform()

    keywords = []
    for i in range(1, 11):
        full_text = driver.find_element(By.XPATH, f'/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[{i}]/div').text
        # 숫자와 '보합'을 제외하고 중간 내용만 추출
        parts = full_text.split()
        content = ' '.join(parts[1:-1])
        keywords.append(content)

    driver.quit()

    now = datetime.now().strftime('%Y-%m-%d %H:00:00')

    conn = pymysql.connect(host='localhost', port=3305, user='root', password='root', db='issue', charset='utf8')
    cur = conn.cursor()

    for rank, word in enumerate(keywords, 1):
        cur.execute("INSERT INTO keyword (`word`, `site`, `rank`, `time`) VALUES (%s, 'zum', %s, %s)", (word, rank, now))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    collect_keywords()
