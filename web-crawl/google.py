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

driver.get('https://trends.google.co.kr/trending?geo=KR')

one = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[1]/td[2]/div[1]').text
one_words = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[1]').text

two = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]').text
three = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[3]/td[2]/div[1]').text
four = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[4]/td[2]/div[1]').text
five = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[5]/td[2]/div[1]').text
six = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[6]/td[2]/div[1]').text
seven = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[7]/td[2]/div[1]').text
eight = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[8]/td[2]/div[1]').text
nine = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[9]/td[2]/div[1]').text
ten = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[10]/td[2]/div[1]').text

print(one)

driver.quit() # driver 종료