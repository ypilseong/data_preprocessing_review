import pandas as pd

data = pd.read_csv('data/store_data.csv', sep=',', encoding='utf-8')
data_frame = data[['사업장명', '인허가일자', '상세영업상태명', '소재지전체주소', '도로명전체주소']]
data_frame.columns = ['store_name', 'permission_date', 'situation', 'address', 'address_road']
data_frame = data_frame.loc[data_frame.situation=='영업']

area = '구좌'
new_df = pd.DataFrame(columns=data_frame.columns)
cnt = 0

# 특정 지역 추출
for i in range(len(data_frame)):
    ad = data_frame.loc[data_frame.index[i], ['address_road']]
    if str(ad['address_road']).find(area) != -1:
        new_df.loc[cnt] = data_frame.iloc[i]
        cnt += 1
    else:
        continue

new_df['new_store_name'] = ''
# 주소와 상호명 결합
for i in range(len(new_df)):
    cols = ['store_name', 'address_road']
    new_df['new_store_name'] = new_df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# 날짜 데이터 표준화 및 특정기간 추출
new_df['permission_date'] = pd.to_datetime(new_df['permission_date'], format='%Y%m%d')
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2023-12-30')
new_df_filter = new_df[new_df['permission_date'].between(start_date, end_date)]

new_df_filter.to_csv('data/filtered_data.csv', index=False)

print(new_df_filter)