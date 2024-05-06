import pytesseract
import cv2


def ocr(path):

    #path = 'naverBlog/기억에남는제주시흑돼지맛집/29.JPEG'

    img_num = 1
    while True:
        try:
            image = cv2.imread(path + f'/{img_num}.JPEG')
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            text = pytesseract.image_to_string(rgb_image, lang='kor')
            print(text)
            img_num += 1
        except:
            print('finish')


def check_word(text):
    word_list = ['수수료', '원고료', '활동비', '물품', '할인', '서비스', '소정의', '제작비']
    text = text.replace(" ", "") # 중복 제거

    # 단어 포함 확인
    falase_review_word = []
    for word in word_list:
        if word in text:
            print(word)
            falase_review_word.append(word)

    return falase_review_word
#export TESSDATA_PREFIX='/home/chuaie/workspace/projects/review_confirm/tessdata'