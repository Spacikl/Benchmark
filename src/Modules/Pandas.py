import os.path

import pandas as pd
from src.DataBase import *

class Pandas(DataBase):
    def __init__(self):
        super().__init__()

    def startTest(self):
        if os.path.exists(DataBase.path_to_file_csv) == False:
           print("File not exist")
           return

        df = pd.read_csv(DataBase.path_to_file_csv)
        for i in range(4):
            static_data = []
            for j in range(1):
                if i == 0:
                    start = time.time()
                    selected_df = df[['VendorID']]
                    grouped_df = selected_df.groupby('VendorID')
                    final_df = grouped_df.size().reset_index(name='counts')
                    static_data.append(time.time() - start)
                elif i == 1:
                    start = time.time()
                    selected_df = df[['passenger_count', 'total_amount']]
                    grouped_df = selected_df.groupby('passenger_count')
                    final_df = grouped_df.mean().reset_index()
                    static_data.append(time.time() - start)
                elif i == 2:
                    start = time.time()
                    selected_df = df[['passenger_count', 'tpep_pickup_datetime']]
                    selected_df['year'] = pd.to_datetime(
                        selected_df.pop('tpep_pickup_datetime'),
                        format='%Y-%m-%d %H:%M:%S').dt.year
                    grouped_df = selected_df.groupby(['passenger_count', 'year'])
                    final_df = grouped_df.size().reset_index(name='counts')
                    static_data.append(time.time() - start)
                elif i == 3:
                    start = time.time()
                    selected_df = df[[
                        'passenger_count',
                        'tpep_pickup_datetime',
                        'trip_distance']]
                    selected_df['trip_distance'] = selected_df['trip_distance'].round().astype(int)
                    selected_df['year'] = pd.to_datetime(
                        selected_df.pop('tpep_pickup_datetime'),
                        format='%Y-%m-%d %H:%M:%S').dt.year
                    grouped_df = selected_df.groupby([
                        'passenger_count',
                        'year',
                        'trip_distance'])
                    final_df = grouped_df.size().reset_index(name='counts')
                    final_df = final_df.sort_values(
                        ['year', 'counts'],
                        ascending=[True, False])
                    static_data.append(time.time() - start)
            self.data.append(f"Query:{i + 1} ---> {str(statistics.median(static_data))}\n")
        super().printTime("Pandas")