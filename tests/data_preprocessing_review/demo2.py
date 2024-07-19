import sys
sys.path.append('/home/chuaie/workspace/projects/data_preprocessing_review/src/data_preprocessing_review/crawling')
from get_blog_url import get_blog_url
from blog_scraping import extract_naverBlog, extract_emotion_tag
from ocr_img import ocr
from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


import pandas as pd


def main(path, start):

    df = pd.read_csv(path, sep=',', encoding='utf-8')
    df = df[start:]
    store_data = df['new_store_name'].tolist()

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(options=options)

    df_blog = pd.DataFrame(columns=['store_name', 'blog_url', 'result', 'word'])
    blog_count = 0
    store_count = 0
    for i in store_data:
        store_count += 1
        try:
            df_blog_url = get_blog_url(driver,i)
            for k in range(len(df_blog_url)):
                if ((df_blog_url['date'][k] > pd.to_datetime('2020-01-01', format='%Y-%m-%d')) and
                    (df_blog_url['date'][k] < pd.to_datetime('2021-12-31', format='%Y-%m-%d'))):
                    try:
                        blog_count += 1
                        post_dir_name, post_title = extract_naverBlog(df_blog_url['blog_url'][k], i)
                        extract_emotion_tag(url=df_blog_url['blog_url'][k],driver=driver, post_dir_name=post_dir_name, post_title=post_title, date=df_blog_url['date'][k], week=df_blog_url['day_of_week'][k])
                        review_word = ocr(post_dir_name)
                        if review_word is not None:
                            if review_word == '내돈내산':
                                df_blog = df_blog.append({'store_name': i, 'blog_url': k, 'result': 'True', 'word': review_word}, ignore_index=True)
                            else:
                                df_blog = df_blog.append({'store_name': i, 'blog_url': k, 'result': 'False', 'word': review_word}, ignore_index=True)
                        df_blog.to_csv('/home/chuaie/workspace/projects/data_preprocessing_review/data/blog_crawling_data.csv', index=False)
                    except:
                        blog_count += 1
                        print(f'skip blog Number {blog_count}')
                        continue
        except Exception as e:
            print(f'Skip store Number {store_count}: {i}: {e}')
            continue
    driver.quit()
    # df_blog.to_csv('/home/chuaie/workspace/projects/review_confirm/data/blog_crawling_data.csv', index=False)


if __name__ =='__main__':
    start = int(2035)
    main('/home/chuaie/workspace/projects/data_preprocessing_review/data/filtered_data_with_date_xy.csv', start)
