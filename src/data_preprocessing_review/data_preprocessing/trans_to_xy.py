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
def geocoding(store_ad, type):
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

    df = pd.read_csv('data/filtered_data.csv', sep=',', encoding='utf-8')
    df['trans_ad'] = df['address'].apply(get_addrs)
    df['trans_ad_road'] = df['address_road'].apply(get_addrs)

    df['x'] = ''
    df['y'] = ''
    
    # 일일 횟수 제한 4만건 -> 0508 3만건 진행
    success_count = 0
    for i in range(len(df)):
        address = df.loc[i]['trans_ad_road']
        try:
            x_value, y_value = geocoding(address, type="road")
            if x_value is not None and y_value is not None:
                df.at[i, 'x'] = x_value
                df.at[i, 'y'] = y_value
                success_count += 1
            else:
                print(f"Failed to geocode address: {address}, skipping to the next one.")
                success_count += 1
                continue  # 데이터를 찾을 수 없으면 다음 번호로 넘어감
        except Exception as e:
            print(f"An error occurred at index {i}: {e}")
            break
    
    print(f"Successfully processed {success_count} addresses.")
    

    nulls = df[df['y'] == 0]
    null_index = list(nulls.index)

    for i in null_index:
        address = df.loc[i]['trans_ad']
        x_value, y_value = geocoding(address, type="parsel")
        df.at[i, 'x'] = x_value
        df.at[i, 'y'] = y_value


    df.to_csv('data/geopy_address6.csv', encoding='utf-8')