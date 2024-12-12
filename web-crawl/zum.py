from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
driver = webdriver.Chrome('chromedriver-win64\chromedriver.exe', options=options)

driver.get('https://zum.com/')

ActionChains(driver).move_by_offset(797, 147).perform()

one = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[1]/div').text
two = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[2]/div').text
three = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[3]/div').text
four = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[4]/div').text
five = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[5]/div').text
six = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[6]/div').text
seven = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[7]/div').text
eight = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[8]/div').text
nine = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[9]/div').text
ten = driver.find_element(By.XPATH, '/html/body/div/div[1]/header/div[2]/div/div/div[2]/div/div[2]/ul/li[10]/div').text
print(one)
print(two)
print(three)
print(four)
print(five)
print(six)
print(seven)
print(eight)
print(nine)
print(ten)

driver.quit() # driver 종료