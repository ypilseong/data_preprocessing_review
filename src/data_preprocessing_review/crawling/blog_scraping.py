import time
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from PIL import Image
import re
import os
import json
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def extract_naverBlog(url, store_name):

    #url = 'https://m.blog.naver.com/clare1/223273103611'
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ifra = soup.find('iframe', id='mainFrame')
    post_url = 'https://blog.naver.com' + ifra['src']
    print(post_url)
    

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }


    res = requests.get(post_url, headers=headers)
    soup2 = BeautifulSoup(res.text, 'html.parser')
    
    # 제목 추출
    titles = soup2.find_all('div', {'class': re.compile('^se-module se-module-text se-title-tex.*')})
    post_title = titles[0].text
    post_title = post_title.replace('\n', '')

    special_char = '\/:*?"<>|.'
    for c in special_char:
        if c in post_title:
            post_title = post_title.replace(c, '')  # 특수 문자 제거
        
    # 저장 폴더 만들기
    dir_names = post_title.replace(' ', '').replace('\n', '')
    if not os.path.exists('data/naverBlog'):
        os.mkdir('data/naverBlog')
    else:
        pass
    if not os.path.exists('data/naverBlog/' + store_name):
        os.makedirs('data/naverBlog/' + store_name)
    if not os.path.exists(f'data/naverBlog/{store_name}/' + dir_names):
        os.makedirs(f'data/naverBlog/{store_name}/' + dir_names)
    else:
        pass
    
    post_dir_name = f'data/naverBlog/{store_name}/' + dir_names
    
    # 본문 내용을 html 타입으로 저장
    # script 등 태그 제거
    [x.extract() for x in soup2.find_all('script')]
    [x.extract() for x in soup2.find_all('style')]
    [x.extract() for x in soup2.find_all('meta')]
    [x.extract() for x in soup2.find_all('noscript')]
    [x.extract() for x in soup2.find_all(text=lambda text:isinstance(text, Comment))]                
        
    html = soup2.prettify("utf-8")
    html_filename = post_title.replace('\n', '') + '.html'
    with open(post_dir_name + '/' + html_filename, 'wb') as f:
        f.write(html)                
    
    # 페이지 내용(텍스트) 추출
    contents = ''
    txt_contents = soup2.find_all('div', {'class': re.compile('^se-component se-text se-l-default')})
    for p_span in txt_contents:
        for txt in p_span.find_all('span'):
            print(txt.get_text() + '\n')
            contents += txt.get_text() + '\n'
    print(contents)

    txt_filename = post_title.replace('\n', '') + '.txt'
    with open(post_dir_name + '/' + txt_filename, 'w', encoding='utf-8') as f:
        f.write(contents)                       
    
    # 이미지 추출
    image_contents = soup2.find_all('div', {'class': re.compile('^se-component se-image')})
    image_contents.append(soup2.find_all('div', {'class': re.compile('^se-component se-imageStrip')}))

    cnt = 1
    for img in image_contents:
        try:
            for img_tag in img.find_all('img'):
                img_url = img_tag.get('data-lazy-src')
                imageObj = Image.open(requests.get(img_url, stream=True).raw)
                img_format = imageObj.format                    
                res_img = requests.get(img_url).content
                
                if img_format:
                    img_name = str(cnt) + '.' + img_format
                else:
                    img_name = str(cnt) + '.jpg'
                
                print(img_name)

                if len(res_img) > 100:  # 이미지 용량이 00 bytes 이상인 것만
                    with open(post_dir_name + '/' + img_name, 'wb') as f:
                        f.write(res_img)
                    cnt += 1    
        except:
            continue
    
    
    
    return post_dir_name, post_title


def extract_emotion_tag(url, driver,  post_dir_name, post_title, date):
    # Naver 블로그 URL 로드
    driver.get(url)
     
    # Wait until the main iframe is available and switch to it
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame')))
    
    # 스크롤 다운
    scroll_down(driver)

    # Wait until the count element is present
    count_elem = driver.find_element(By.CSS_SELECTOR, '#printPost1 > tbody > tr > td.bcc > div.post-btn.post_btn2 > div.wrap_postcomment > div.area_sympathy.pcol2 > a > div > span > em.u_cnt._count')
    count = count_elem.text.strip()
    print(f'Count: {count}')
    
    # Wait until the tag element is present
    high_tag_elem = driver.find_element(By.XPATH, '//*[@id="post_footer_contents"]/div/div[1]')
    tag_elements = high_tag_elem.find_elements(By.TAG_NAME, 'a')
    tag_count = len(tag_elements)
    print(f'태그 총 개수: {tag_count}')
    
    
    
    
    
    
    # 카테고리 이름 추출
    category_name_elem = driver.find_elements(By.CSS_SELECTOR, '#category-name > div > table.post-body > tbody > tr > td.bcc > div > h4')
    category_name = None
    if category_name_elem:
        category_name = category_name_elem[0].text.strip()
        print(f'총 게시물 개수: {category_name}')
    else:
        print('총 게시물 개수 추출 안됨')
    
    # 데이터 저장
    data = {
        'url': url,
        'category_name': category_name,
        'post_title': post_title,
        'date': date,
        'like': count,
        'tag_count': tag_count
    }

    json_filename = f'{post_dir_name}/metadata.json'
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f'Data saved to {json_filename}')
    
    return post_dir_name


def scroll_down(driver, scroll_pause_time=2):
    """스크롤 다운 함수"""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

if __name__=='__main__':
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(options=options)
    url = 'https://blog.naver.com/ancandle/223440129193'
    store_name = '흑돈가'
    extract_emotion_tag(url=url,driver=driver, post_dir_name='data/naverBlog/흑돈가/기억에남는제주시흑돼지맛집', post_title= '흑돈가')
