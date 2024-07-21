import pandas as pd
from geopy.distance import distance
from shapely.geometry import Point, Polygon

def get_rectangle_coordinates(center_lat, center_lon, width_meters, height_meters):
    # 25m 떨어진 거리를 계산
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

# 파일 읽기
df_store = pd.read_csv('/Users/gyubeomlee/Desktop/Workspace/data_preprocessing_review/data/testdata.csv')
df_rental = pd.read_csv('/Users/gyubeomlee/Desktop/Workspace/data_preprocessing_review/data/rental_car_data_pretrain.csv')

# 결과 저장할 리스트 초기화
results = []

# 각 업체를 기준으로 25미터 박스를 만들고 렌터카 방문 정보 확인
for i in range(len(df_store)):
    try:
        print(f"Processing store {i+1}/{len(df_store)}: {df_store.loc[i]['store_name']}")
        x_value = df_store.loc[i]['x']
        y_value = df_store.loc[i]['y']
        store_name = df_store.loc[i]['store_name']
        
        rect_coords = get_rectangle_coordinates(y_value, x_value, 25, 25)
        bounding_box = Polygon([
            (rect_coords['west'][1], rect_coords['south'][0]),
            (rect_coords['west'][1], rect_coords['north'][0]),
            (rect_coords['east'][1], rect_coords['north'][0]),
            (rect_coords['east'][1], rect_coords['south'][0])
        ])
        
        df_rental['point'] = df_rental.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        df_rental['within'] = df_rental['point'].apply(lambda point: point.within(bounding_box))
        
        rental_within = df_rental[df_rental['within']]
        rental_within['date'] = pd.to_datetime(rental_within['time']).dt.date
        
        date_counts = rental_within.groupby('date').size().reset_index(name='counts')
        
        for idx, row in date_counts.iterrows():
            results.append({
                'store_name': store_name,
                'date': row['date'],
                'visits': row['counts']
            })
        
    except Exception as e:
        print(f"Error processing store {i+1}: {e}")

# 결과 데이터프레임으로 변환
df_results = pd.DataFrame(results)

# 결과 출력
print(df_results)

# 결과를 CSV 파일로 저장
df_results.to_csv('/Users/gyubeomlee/Desktop/Workspace/data_preprocessing_review/data/store_visits.csv', index=False)
