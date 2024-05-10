import pandas as pd
from geopy.distance import distance



df_store_new = pd.read_csv('data/geopy_address_new2.csv', encoding='utf-8', sep=',')
df_store_base = pd.read_csv('data/geopy_address_base.csv', encoding='utf-8', sep=',')

#df_store_new coloums [store_name, business_category, permission_date, situation, address, address_road, new_store_name, trans_ad, trans_ad_road, x, y]


def get_rectangle_coordinates(center_lat, center_lon, width_meters, height_meters):
    # 50m 떨어진 거리를 계산
    north = distance(meters=height_meters/2).destination((center_lat, center_lon), 0)
    east = distance(meters=width_meters/2).destination((center_lat, center_lon), 90)
    south = distance(meters=height_meters/2).destination((center_lat, center_lon), 180)
    west = distance(meters=width_meters/2).destination((center_lat, center_lon), 270)
    
    return {
        'north': (north.latitude, north.longitude),
        'east': (east.latitude, east.longitude),
        'south': (south.latitude, south.longitude),
        'west': (west.latitude, west.longitude)
    }

depen_store = pd.DataFrame(columns=df_store_new.columns)
print(len(df_store_new))


# 인허가일자 2020~2021 가게 주변에 다른 가게 있는지 check and list-up
for i in range(len(df_store_new)):
    x_value = df_store_new['x'][i]
    y_value = df_store_new['y'][i]
    result_coord = get_rectangle_coordinates(y_value, x_value, 50, 50)
    store_count = 0
    try:
        for k in range(len(df_store_base)):
            if ((result_coord['north'][0] > df_store_base['y'][k] and result_coord['south'][0] < df_store_base['y'][k]) and
                (result_coord['east'][1] > df_store_base['x'][k] and result_coord['west'][1] < df_store_base['x'][k])):
                store_count += 1

                if store_count >= 2:
                    depen_store.loc[i] = df_store_new.loc[i]
                    break

    except:
        continue

# DataFrame 합친 후 중복 제거
combined_df = pd.concat([df_store_new, depen_store])
unique_df = combined_df.drop_duplicates(subset='store_name')

unique_df.to_csv('data/uniqe_store_data.csv', encoding='utf-8')
print(len(unique_df))
