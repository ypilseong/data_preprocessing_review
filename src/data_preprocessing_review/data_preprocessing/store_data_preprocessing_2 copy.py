import pandas as pd

# 데이터 로드
data_frame = pd.read_csv('data/geopy_address_base.csv', sep=',', encoding='utf-8')



data_frame['permission_date'] = pd.to_datetime(data_frame['permission_date'], format='%Y%m%d')
start_date = pd.to_datetime('2020-01-01')
end_date = pd.to_datetime('2021-12-31')
new_df_filter = data_frame[data_frame['permission_date'].between(start_date, end_date)]

new_df_filter['new_store_name'] = ''

def get_addrs(x):
    try:
        x1 = x.replace('제주특별자치도', '')
        x1 = x1.split(',')
        return x1[0]
    except:
        pass


new_df_filter['new_store_name'] = new_df_filter['address_road'].apply(get_addrs)

# 주소와 상호명 결합

cols = ['store_name', 'new_store_name']
new_df_filter['new_store_name'] = new_df_filter[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)


new_df_filter.to_csv('data/filtered_data_with_date.csv', index=False)

print(new_df_filter)