import pandas as pd
from geopy.geocoders import Nominatim
import requests

df = pd.read_csv('data/filtered_data.csv', sep=',', encoding='utf-8')

def get_addrs(x):
    x1 = x.split(' ')
    return " ".join(x1[3:5])
    
# 주소 전처리
df['trans_ad'] = df['address'].apply(get_addrs)
df['trans_ad_road'] = df['address_road'].apply(get_addrs)

# 국토교통부 geocoder open api 
def geocoing(store_ad, type):
    try:

        apiurl = "https://api.vworld.kr/req/address?"
        params = {
            "service": "address",
            "request": "getcoord",
            "crs": "epsg:4326",
            "address": store_ad,
            "format": "json",
            "type": type, #road or parsel
            "key": "68847939-BE25-31AE-931E-08FB887AB0F1"
        }
        response = requests.get(apiurl, params=params)

        ad_json = response.json()

        x_value = ad_json['response']['result']['point']['x']
        y_value = ad_json['response']['result']['point']['y']
        return x_value, y_value
    except: 
        x_value = 0
        y_value = 0
        return x_value, y_value

df['x'] = ''
df['y'] = ''

for i in range(len(df)):
    address = df.loc[i]['trans_ad_road']
    x_value, y_value = geocoing(address, type="road")
    df['x'][i] = x_value
    df['y'][i] = y_value




nulls = df[df['y'] == 0]
null_index = list(nulls.index)

for i in null_index:
    address = df.loc[i]['trans_ad']
    x_value, y_value = geocoing(address, type="parsel")
    df['x'][i] = x_value
    df['y'][i] = y_value


df.to_csv('data/geopy_address.csv', encoding='utf-8')