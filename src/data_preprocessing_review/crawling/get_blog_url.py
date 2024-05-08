from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.support import expected_conditions as EC


def get_blog_url(store_data):

    url = f'https://map.naver.com/v5/search/{store_data}'
    
    # Webdriver headless mode setting
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

# BS4 setting for secondary access
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))

# Start crawling/scraping!
    try: 
        driver = webdriver.Chrome()
        res = driver.get(url)
        driver.implicitly_wait(30)

        driver.switch_to.frame("entryIframe")
        # Pagedown
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[4]').click()
        driver.find_element(By.CSS_SELECTOR, '#_subtab_view > div > a:nth-child(2)').click()
        try:
            while True:
                driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div.NSTUp > div > a').click()
                time.sleep(0.4)
            
        except Exception as e:
            print('finish')

        time.sleep(25)
        blog_url_list = []
        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.xg2_q")
        for li in li_elements:
            a_element = li.find_element(By.TAG_NAME, 'a')
            href_value = a_element.get_attribute('href')
            date_element = li.find_element(By.CSS_SELECTOR, 'div.FYQ74 > span.ZeWU8')  # Adjusted selector
            date_value = date_element.text
            blog_url_list.append((href_value, date_value))
            print(href_value, date_value)
            # print(span_value)
        driver.quit()

        return blog_url_list

    except Exception as e:
        print(e)
    # Save the file(temp)    file_name = 'naver_review_' + now.strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx    xlsx.save(file_name)
    

if __name__=='__main__':
    get_blog_url('제주시 구좌읍 평대5길 41 이로리')

    