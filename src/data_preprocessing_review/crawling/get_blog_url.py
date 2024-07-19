from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import time
import requests

import pandas as pd

def trans_date(x):
    date = x.split('.')
    year = '20' + date[0]
    month = date[1]
    day = date[2]
    day_of_week = date[3]
    formatted_date = f'{year}-{month}-{day}'
    return formatted_date, day_of_week

def get_blog_url(driver, store_data):
    url = f'https://map.naver.com/v5/search/{store_data}'

    # Webdriver headless mode setting
    # options = webdriver.ChromeOptions()
    # #options.add_argument('headless')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")

    # BS4 setting for secondary access
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))

    # Start crawling/scraping!
    try:
        # driver = webdriver.Chrome(options=options)
        res = driver.get(url)
        driver.implicitly_wait(30)
        WebDriverWait(driver, 40).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))
        # driver.switch_to.frame("entryIframe")
        # Pagedown
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        # driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[4]').click()
        tab_link = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div')
        tag_a = tab_link.find_elements(By.TAG_NAME, 'a')
        for i in range(len(tag_a)):
            if tag_a[i].text == '리뷰':
                review_link = tag_a[i]
                break
        review_link.click()

        driver.find_element(By.CSS_SELECTOR, '#_subtab_view > div > a:nth-child(2)').click()
        try:
            while True:
                driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div.NSTUp > div > a').click()
                time.sleep(0.4)

        except Exception as e:
            print('finish click button')

        time.sleep(25)
        df_blog_url = pd.DataFrame(columns=['blog_url', 'date', 'day_of_week'])
        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.xg2_q")
        for li in li_elements:
            a_element = li.find_element(By.TAG_NAME, 'a')
            href_value = a_element.get_attribute('href')
            date_element = li.find_element(By.CSS_SELECTOR, 'div.FYQ74 > span.ZeWU8')  # Adjusted selector
            date_value = date_element.text
            formatted_date, day_of_week = trans_date(date_value)
            new_row = pd.DataFrame({'blog_url': [href_value], 'date': [formatted_date], 'day_of_week': [day_of_week]})
            df_blog_url = pd.concat([df_blog_url, new_row], ignore_index=True)
            print(href_value, formatted_date, day_of_week)
            # print(span_value)

        df_blog_url['date'] = pd.to_datetime(df_blog_url['date'], format='%Y-%m-%d')
        # driver.quit()

        return df_blog_url

    except Exception as e:
        print(e)
    # Save the file(temp)    file_name = 'naver_review_' + now.strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx    xlsx.save(file_name)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    store_data = '제주시 구좌읍 평대5길 41 이로리'
    df_blog_url = get_blog_url(driver, store_data)
    driver.quit()
    print(df_blog_url)
