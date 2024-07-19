import json

file_path = '/home/chuaie/workspace/projects/data_preprocessing_review/data/final_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # 상위 10개의 키와 값을 출력
        keys = list(data.keys())
        for key in keys[:10]:
            print(f"{key}: {data[key]}")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno}")
except Exception as e:
    print(f"An error occurred: {e}")
