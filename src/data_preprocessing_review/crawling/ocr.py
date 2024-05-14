import pytesseract
import cv2

# OCR 함수
def ocr(path):

    #path = 'naverBlog/기억에남는제주시흑돼지맛집/29.JPEG'

    img_num = 1
    while True:
        try:
            image = cv2.imread(path + f'/{img_num}.JPEG')
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            text = pytesseract.image_to_string(rgb_image, lang='kor')
            print(text)
            print(img_num)
            img_num += 1
            check_text = check_word(text)

            return check_text
        except:
            break

# 단어 확인 함수
def check_word(text):
    word_list = ['수수료', '원고료', '활동비', '물품', '소정의', '제작비', '참여후']
    text = text.replace(" ", "") #공백 제거

    # 단어 포함 확인
    falase_review_word = []
    for word in word_list:
        if word in text:
            print(word)
            falase_review_word.append(text)

    return falase_review_word

# tessdata 경로 설정
#export TESSDATA_PREFIX='/home/chuaie/workspace/projects/review_confirm/tessdata'

if __name__=='__main__':
    ocr('naverBlog/기억에남는제주시흑돼지맛집')