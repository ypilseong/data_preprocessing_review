import pytesseract
import cv2
import os
import csv

# OCR 함수
def ocr_directory(directory_path, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Folder Name', 'Detected Words', 'Condition'])

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(('.jpeg', '.jpg', '.png')):
                    file_path = os.path.join(root, file)
                    result, condition = ocr(file_path)
                    folder_name = os.path.basename(root)
                    writer.writerow([folder_name, ', '.join(result), condition])
                    print(f'Saved result for {file_path}')

# OCR 함수
def ocr(image_path):
    try:
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb_image, lang='kor')
        check_text, condition = check_word(text)
        print(f'{image_path}: {check_text}, {condition}')
        return check_text, condition
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return [], 'Error'

# 단어 확인 함수
def check_word(text):
    word_list = ['수수료', '원고료', '활동비', '물품', '소정의', '제작비', '참여후', '체험단', '내돈내산']
    text = text.replace(" ", "")  # 공백 제거
    check_text = []
    condition = 'True'

    # 단어 포함 확인
    for word in word_list:
        if word in text:
            if word == '내돈내산':
                check_text.append(word)
                condition = 'True'
            else:
                check_text.append(word)
                condition = 'False'
    
    return check_text, condition

if __name__ == '__main__':
    directory_path = 'data/naverBlog'
    csv_path = 'data/naverBlog/ocr_results.csv'
    ocr_directory(directory_path, csv_path)
