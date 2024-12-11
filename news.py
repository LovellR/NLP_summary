from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

driver = webdriver.Chrome('chromedriver-win64\chromedriver.exe', chrome_options=options)

search_query = "걸그룹 성추행"
base_url = f"https://search.naver.com/search.naver?where=news&query={search_query}&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0&office_category=0&service_area=0"
driver.get(base_url)

news_count = len(driver.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/section/div[1]/div[2]/ul/li'))

for index in range(1, news_count + 1):
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

    print(content)
    driver.back()

driver.quit()
