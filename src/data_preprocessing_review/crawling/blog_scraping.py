import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from PIL import Image
import re
import os
from io import BytesIO


def extract_naverBlog(url, store_name):

    #url = 'https://blog.naver.com/clare1/223273103611'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ifra = soup.find('iframe', id='mainFrame')
    post_url = 'https://blog.naver.com' + ifra['src']
    print(post_url)
    

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
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
    imgs = soup2.find_all('img', class_='se-image-resource egjs-visble')
    # print(len(imgs))
    # print(imgs)
    cnt = 1

    for img in imgs:
        img_url = img.get('data-lazy-src')
        
        if img_url:  # 이미지 주소가 비어있지 않을 경우에만 진행
            try:
                # 이미지 가져오기
                res_img = requests.get(img_url).content
                # 이미지 포맷 확인
                imageObj = Image.open(BytesIO(res_img))
                img_format = imageObj.format
                if img_format:
                    img_name = str(cnt) + '.' + img_format.lower()  # 포맷을 소문자로 변경
                else:
                    img_name = str(cnt) + '.jpg'
                # 이미지 저장
                with open(post_dir_name + '/' + img_name, 'wb') as f:
                    f.write(res_img)
                cnt += 1
            except Exception as e:
                print(f"Error fetching image: {e}")
    # for img in imgs:
    #     # <img src=  가 아닌  data-lazy-src=  부분을 가져와야 큰 이미지임
    #     print(img.get('data-lazy-src'))  # img['data-lazy-src']
    #     img_url = img.get('data-lazy-src')
    #     ## pillow.Image로 이미지 format 알아내기
    #     imageObj = Image.open(requests.get(img_url, stream=True).raw)
    #     img_format = imageObj.format                    
    #     res_img = requests.get(img_url).content
        
    #     if img_format:
    #         img_name = str(cnt) + '.' + img_format
    #     else:
    #         img_name = str(cnt) + '.jpg'
        
    #     print(img_name)

    #     if len(res_img) > 100:  # 이미지 용량이 00 bytes 이상인 것만
    #         with open(post_dir_name + '/' + img_name, 'wb') as f:
    #             f.write(res_img)
    #         cnt += 1    
    return post_dir_name


