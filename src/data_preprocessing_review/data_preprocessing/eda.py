import pandas as pd
import json
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# JSON 파일 로드
with open('data/final_data_update2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 필요한 데이터 추출
stores = data['store']

# 각 store의 metadata와 reviewer를 데이터프레임으로 변환
metadata_list = []
reviewer_list = []
labels_list = []

def convert_to_int(value):
    """Convert value to int, if conversion fails return None."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

for store in stores:
    metadata = store['metadata']
    reviewer = store['reviewer']
    
    # 'num_post' 값이 빈 문자열일 때를 처리
    num_post_value = reviewer.get('num_post', '').split()
    num_post_value = num_post_value[0] if num_post_value else None

    metadata_list.append({
        'name': store['name'],
        'url': metadata.get('url', None),
        'title': metadata.get('title', None),
        'date': metadata.get('date', None),
        'week': metadata.get('week', None),
        'like': convert_to_int(metadata.get('like', None)),
        'tag_count': convert_to_int(metadata.get('tag_count', None)),
        'txt_len': convert_to_int(metadata.get('txt_len', None)),
        'img_cnt': convert_to_int(metadata.get('img_cnt', None))
    })
    
    reviewer_list.append({
        'name': store['name'],
        'num_post': convert_to_int(num_post_value)  # '맛집/카페 520개의 글'에서 숫자만 추출
    })
    
    labels_list.append({
        'name': store['name'],
        'labels': store.get('labels', [None])[0]
    })

# 데이터프레임 생성
metadata_df = pd.DataFrame(metadata_list)
reviewer_df = pd.DataFrame(reviewer_list)
labels_df = pd.DataFrame(labels_list)

# 데이터프레임 병합
df = pd.merge(metadata_df, reviewer_df, on='name')
df = pd.merge(df, labels_df, on='name')

# 날짜 형식 변환
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 데이터 프레임 출력
print("DataFrame Head:")
print(df.head())

print("\nDataFrame Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

# labels의 분포를 plot
plt.figure(figsize=(10, 6))
df['labels'].value_counts().plot(kind='bar')
plt.title('Labels Distribution')
plt.xlabel('Labels')
plt.ylabel('Count')
plt.show()

# 각 값의 분포를 plot
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))

df['like'].plot(kind='hist', ax=axes[0, 0], title='Like Distribution')
df['tag_count'].plot(kind='hist', ax=axes[0, 1], title='Tag Count Distribution')
df['txt_len'].plot(kind='hist', ax=axes[0, 2], title='Text Length Distribution')
df['img_cnt'].plot(kind='hist', ax=axes[1, 0], title='Image Count Distribution')
df['num_post'].plot(kind='hist', ax=axes[1, 1], title='Number of Posts Distribution')
df['week'].value_counts().plot(kind='bar', ax=axes[1, 2], title='Week Distribution')
df['date'].dt.year.value_counts().sort_index().plot(kind='bar', ax=axes[2, 0], title='Year Distribution')

plt.tight_layout()
plt.show()