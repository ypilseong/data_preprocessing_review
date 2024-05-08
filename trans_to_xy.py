import pandas as pd
from geopy.geocoders import Nominatim
import requests



def get_addrs(x):
    try:
        x1 = x.replace('제주특별자치도', '')
        x1 = x1.split(',')
        return x1[0]
    except:
        pass



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

if __name__=='__main__':

    df = pd.read_csv('data/store_data.csv', sep=',', encoding='utf-8')
    df = df[['사업장명', '인허가일자', '상세영업상태명', '소재지전체주소', '도로명전체주소']]
    df.columns = ['store_name', 'permission_date', 'situation', 'address', 'address_road']
    df = df.loc[df.situation=='영업']

    

    df['trans_ad'] = df['address'].apply(get_addrs)
    df['trans_ad_road'] = df['address_road'].apply(get_addrs)

    df['x'] = ''
    df['y'] = ''

    # 일일 횟수 제한 4만건 -> 0508 3만건 진행
    for i in range(30000):
        address = df.loc[i]['trans_ad_road']
        x_value, y_value = geocoing(address, type="road")
        df['x'][i] = x_value
        df['y'][i] = y_value




    # nulls = df[df['y'] == 0]
    # null_index = list(nulls.index)

    # for i in null_index:
    #     address = df.loc[i]['trans_ad']
    #     x_value, y_value = geocoing(address, type="parsel")
    #     df['x'][i] = x_value
    #     df['y'][i] = y_value


    df.to_csv('data/geopy_address3.csv', encoding='utf-8')