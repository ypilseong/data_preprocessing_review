import pandas as pd
from pyproj import Proj, transform
import folium

df = pd.read_csv('data/체류빈도_2021_07.csv', encoding='cp949', sep=',')

proj_1 = Proj(init='epsg:5178')
proj_2 = Proj(init='epsg:4326')

converted = transform(proj_1, proj_2, df['xcoord'].values, df['ycoord'].values)
df['lon'] = converted[0]
df['lat'] = converted[1]

print(df[:20])
