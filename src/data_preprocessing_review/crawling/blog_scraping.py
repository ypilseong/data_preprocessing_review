import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from PIL import Image
import re
import os



def extract_naverBlog(url, store_name):

    #url = 'https://blog.naver.com/clare1/223273103611'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ifra = soup.find('iframe', id='mainFrame')
    post_url = 'https://blog.naver.com' + ifra['src']
    print(post_url)


    res = requests.get(post_url)
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
    if not os.path.exists('naverBlog'):
        os.mkdir('naverBlog')
    else:
        pass
    if not os.path.exists('naverBlog/' + store_name):
        os.makedirs('naverBlog/' + store_name)
    if not os.path.exists(f'naverBlog/{store_name}' + dir_names):
        os.makedirs(f'naverBlog/{store_name}' + dir_names)
    else:
        pass
    
    post_dir_name = f'naverBlog/{store_name}' + dir_names
    
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
        # <img src=  가 아닌  data-lazy-src=  부분을 가져와야 큰 이미지임
        print(img.get('data-lazy-src'))  # img['data-lazy-src']
        img_url = img.get('data-lazy-src')
        ## pillow.Image로 이미지 format 알아내기
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
    return post_dir_name

extract_naverBlog('https://blog.naver.com/clare1/223273103611')
