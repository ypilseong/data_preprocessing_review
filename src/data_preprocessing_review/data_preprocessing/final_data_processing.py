import json

# JSON 파일 경로
file_path = '/home/a202121010/workspace/projects/data_preprocessing_review/data/final_data.json'
output_path = '/home/a202121010/workspace/projects/data_preprocessing_review/data/final_data_update2.json'

# JSON 파일 불러오기
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 특정 단어 리스트
keywords = ['수수료', '원고료', '활동비', '물품', '소정의', '제작비', '참여후', '체험단', '내돈내산', '제공받아']

# 데이터 처리
for store in data["store"]:
    # "labels" 리스트에 값이 없으면 0을 채우기
    if not store["labels"]:
        store["labels"] = [0]
    
    # "labels" 리스트에서 0만 있으면 0 하나만 남기기
    # 다른 숫자(1, -1)가 있으면 0 모두 제거
    elif set(store["labels"]) == {0}:
        store["labels"] = [0]
    else:
        store["labels"] = [label for label in store["labels"] if label != 0]

    # "content"에 특정 단어가 있는 경우 "check_txt"에 추가
    content = store["textual"]["content"]
    if "check_txt" not in store:
        store["check_txt"] = []
    for word in keywords:
        if word in content and word not in store["check_txt"]:
            store["check_txt"].append(word)
            if word == '내돈내산':
                store["labels"] = [1]
            else:
                store["labels"] = [-1]

# 변경된 데이터를 새로운 JSON 파일로 저장
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("데이터 처리가 완료되었습니다. 결과는 final_data_update.json 파일에 저장되었습니다.")
