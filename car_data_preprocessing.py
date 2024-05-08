import pandas as pd
from geopy.distance import distance


#df_car = pd.read_csv('data/체류빈도_2021_07.csv', encoding='cp949', sep=',')
df_store = pd.read_csv('data/geopy_address.csv', encoding='utf', sep=',')

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

ip_store = pd.DataFrame(columns=df_store.columns)
print(len(df_store))

for i in range(len(df_store)):
    x_value = df_store['x'][i]
    y_value = df_store['y'][i]
    result_coord = get_rectangle_coordinates(y_value, x_value, 50, 50)
    try:
        for k in range(i+1,len(df_store)):
            if ((result_coord['north'][0] > df_store['y'][k] and result_coord['south'][0] < df_store['y'][k]) and
                (result_coord['east'][1] > df_store['x'][k] and result_coord['west'][1] < df_store['x'][k])):
                df_store.drop([k], axis=0, inplace=True)
                df_store.drop([i], axis=0, inplace=True)
    except:
        continue


print(len(df_store))
