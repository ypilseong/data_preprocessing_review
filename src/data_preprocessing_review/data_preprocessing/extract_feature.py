import os
import json
import sys

sys.path.append('/home/chuaie/workspace/projects/data_preprocessing_review')

# 메타데이터를 가져오는 함수
def get_metadata(metadata_path):
    try:
        with open(metadata_path, 'r', encoding='utf-8') as file:
            metadata = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e} in file {metadata_path}")
        metadata = {}  # 기본값 또는 오류 처리 방식
    return metadata

# 리뷰 텍스트를 가져오는 함수
def get_review_text(review_path):
    with open(review_path, 'r', encoding='utf-8') as file:
        review_text = file.read()
    return review_text

# 이미지 파일 개수를 세는 함수
def count_images(review_folder):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    image_files = [f for f in os.listdir(review_folder) if any(f.lower().endswith(ext) for ext in image_extensions)]
    return len(image_files)

def collect_reviews(data_folder):
    stores = []
    for store in os.listdir(data_folder):
        store_path = os.path.join(data_folder, store)
        if os.path.isdir(store_path):
            for review_folder in os.listdir(store_path):
                review_path = os.path.join(store_path, review_folder)
                if os.path.isdir(review_path):
                    metadata_path = os.path.join(review_path, 'metadata.json')
                    if os.path.exists(metadata_path):
                        metadata = get_metadata(metadata_path)
                        
                        text_files = [f for f in os.listdir(review_path) if f.endswith('.txt')]
                        review_text = ""
                        if text_files:
                            review_text = get_review_text(os.path.join(review_path, text_files[0]))
                        
                        image_count = count_images(review_path)
                        
                        metadata_feature = {
                            "url": metadata.get('url', ''),
                            "title": metadata.get('post_title', ''),
                            "date": metadata.get('date', ''),
                            "week": metadata.get('week', ''),
                            "like": metadata.get('like', 0),
                            "tag_count": metadata.get('tag_count', 0),
                            "txt_len": len(review_text),
                            "img_cnt": image_count
                        }
                        
                        textual_feature = {
                            "content": review_text
                        }
                        
                        reviewer_feature = {
                            "num_post": len(text_files)
                        }
                        
                        store_data = {
                            "name": store,
                            "metadata": metadata_feature,
                            "textual": textual_feature,
                            "reviewer": reviewer_feature
                        }
                        
                        stores.append(store_data)
    
    final_data = {
        "store": stores
    }
    
    return final_data

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data_folder = '/home/chuaie/workspace/projects/data_preprocessing_review/data/naverBlog'
    output_file = '/home/chuaie/workspace/projects/data_preprocessing_review/data/final_data.json'
    final_data = collect_reviews(data_folder)
    save_json(final_data, output_file)
    print(f"Data saved to {output_file}")
