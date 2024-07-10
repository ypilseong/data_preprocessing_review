import pandas as pd

# 데이터 로드
data = pd.read_csv('data/store_data.csv', sep=',', encoding='cp949')

# 필요한 컬럼만 선택하고 컬럼명 변경
data_frame = data[['사업장명', '업종구분소분류','인허가일자', '상세영업상태명', '소재지전체주소', '도로명전체주소']]
data_frame.columns = ['store_name', 'business_category', 'permission_date', 'situation', 'address', 'address_road']

# 영업 상태인 데이터만 선택하고 '편의점' 제외
data_frame = data_frame.loc[data_frame.situation=='영업']
data_frame = data_frame[data_frame['business_category'] != '편의점']
data_frame.reset_index(drop=True, inplace=True)


# 주소와 상호명 결합
data_frame['new_store_name'] = data_frame['store_name'] + ' ' + data_frame['address_road']

# 결과를 CSV 파일로 저장
data_frame.to_csv('data/filtered_data.csv', index=False, encoding='utf-8', sep=',')

print(data_frame)
