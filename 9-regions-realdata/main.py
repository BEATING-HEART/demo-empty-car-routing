from datetime import datetime
import pandas as pd
import numpy as np
import heapq

# https://github.com/tanyokwok/Di-tech

colname = [
    'order_id', 
    'driver_id', 
    'passenger_id', 
    'start_district_hash', 
    'dest_district_hash', 
    'price', 
    'time'
]

heap = []

if __name__ == "__main__":
    # reader =  pd.read_csv(
    #     '9-regions-realdata\data\order_data_2016-01-01',
    #     sep='\t', 
    #     iterator=True, 
    #     header=None, 
    #     names=colname
    # )
    # data = reader.get_chunk(100)
    
    data = pd.read_csv(
        '9-regions-realdata\data\order_data_2016-01-01',
        sep='\t', 
        header=None, 
        names=colname,
        encoding='utf-8-sig',
        parse_dates=['time']
    )
    
    start =  datetime(2016, 1, 1, 17)
    end = datetime(2016, 1, 1, 18)
    
    target = data[(data['time'] >= start) & (data['time'] < end)]
    sorted = target.sort_values(by=['time'])
    
    for index, row in sorted.iterrows():
        row_dict = row.to_dict()
        
        break
