from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

# headless 옵션 설정
#options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu") # 가속 사용 x
options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재(크롤링 금지 회피용)
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

# 드라이버 위치 경로 입력
driver = webdriver.Chrome('chromedriver-win64\chromedriver.exe', chrome_options=options)

driver.get('https://zum.com/')
driver.implicitly_wait(10)


# 사용해보세요!
elem = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]')

location = elem.location 
print(location)

driver.quit() # driver 종료