import pandas as pd
from trans_to_xy import geocoding


df = pd.read_csv('data/geopy_address_base.csv', sep=',', encoding='utf-8')


nulls = df[df['y'] == 0.0]
null_index = list(nulls.index)

for i in null_index:
    address = df.loc[i]['trans_ad']
    x_value, y_value = geocoding(address, type="parsel")
    df.at[i, 'x'] = x_value
    df.at[i, 'y'] = y_value

df.to_csv('data/geopy_address5.csv', encoding='utf-8')