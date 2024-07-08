import pandas as pd
import os
def merge_csv_files(folder_path, output_path):
    files = os.listdir(folder_path)
    csv_files= [f for f in files if f.endswith('.csv')]
    df_list = []
    for csv_file in csv_files:
        try:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path, sep=',', encoding='utf-8')
            df_list.append(df)
        except:
            print(f'Error reading file {csv_file}')
            continue
        
    merged_df = pd.concat(df_list, ignore_index=True)

    merged_df.to_csv(output_path, index=False)
    return merged_df

folder_path = '/home/chuaie/workspace/projects/review_confirm/data/Rental_car_data'
output_path = '/home/chuaie/workspace/projects/review_confirm/data/Rental_car_data/rental_car_data.csv'

car_data = merge_csv_files(folder_path, output_path)
print(len(car_data))