import os, sys
import numpy as np

from models.heap import heap
from models.event import Event
from generator.pgen import passenger_generator, get_passenger_gen_arr
from data.initial import (
    PASSENGER_ARRIVIAL_LAMBDA, 
    REGION_NUM,
    TRAVEL_MATRIX_P,
    EMPTY_CAR_ROUTING_MATRIX_Q,
    ORIGINAL_MATRIX_E,
    ORIGINAL_MATRIX_F
)
from data.constants import (
    E_PASSENGER_ARRIVE,
    E_FULL_CAR_ARRIVE,
    E_EMPTY_CAR_ARRIVE,
    TIME_INTERVAL,
    EPOCH_NUM
)

sys.path.append(os.getcwd())    # 添加根目录为path

print(TRAVEL_MATRIX_P)

# 初始化生成器
passenger_gen_arr = get_passenger_gen_arr(REGION_NUM, PASSENGER_ARRIVIAL_LAMBDA)
"""passenger generator. 下标需要加减"""
# print(passenger_gen_arr)

# 初始化E矩阵和F矩阵
full_car_matrix = ORIGINAL_MATRIX_F
empty_car_matrix = ORIGINAL_MATRIX_E
# print("full car matrix", full_car_matrix)
# print("empyt car matrix", empty_car_matrix)
# heap.print_heap()

# 初始化区域编号数组
region_index_arr = np.arange(start=1, stop=REGION_NUM+1)
# print(region_index_arr)

# 初始化系统时间(按单位时间记)
time_index = 0

passenger_arrived_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA) 
passenger_satisfied_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA)

def passenger_arrive(event):
    # passenger arrive 事件 from=0
    # 乘客到达，马上生成下一个乘客
    next(passenger_gen_arr[event._to - 1])
    # heap.print_heap()
    passenger_arrived_count[event._to-1] += 1
    
    # 乘客到达，有车，则available，则被满足
    if(empty_car_matrix[event._to-1][event._to-1] != 0):
        passenger_satisfied_count[event._to-1] += 1
        # 乘客将从 event._to 出发。 当地空车数-1
        empty_car_matrix[event._to-1][event._to-1] -= 1
        
        # 下面生成乘客到达事件。
        passenger_travel_from = event._to       # 乘客出发地即为乘客生成地
        passenger_travel_to = np.random.choice( # 根据矩阵P随机选择到达地
            region_index_arr, p=TRAVEL_MATRIX_P[passenger_travel_from-1]
        )
        # print(passenger_travel_from, TRAVEL_MATRIX_P[passenger_travel_from-1], np.sum(TRAVEL_MATRIX_P[passenger_travel_from-1]))
        passenger_travel_time = 1
        
        event_passenger_travel = Event(
            passenger_travel_from,
            passenger_travel_to,
            event._time + passenger_travel_time,
            E_FULL_CAR_ARRIVE
        )
        heap.push(event_passenger_travel, event._time + passenger_travel_time)
        
        # 同时，满车矩阵更新
        full_car_matrix[passenger_travel_from-1][passenger_travel_to-1] += 1
        
        # print("full car matrix\n", full_car_matrix)
        # print("empyt car matrix\n", empty_car_matrix)
        # print("***")
    
    # 如果没有车，那么顾客流失
    else:
        pass
    
    
def full_car_arrive(event):
    # 满车到达，首先第一件事，满车矩阵减少了。
    full_car_matrix[event._from-1][event._to-1] -= 1
    
    # 多了一辆空车，但问题在于要不要调度。先生成空车调度到达事件。
    empty_car_routing_from = event._to  # 空车调度出发点就是满车到达点。
    empty_car_routing_to = np.random.choice( # 根据矩阵P随机选择到达地
        region_index_arr, p=EMPTY_CAR_ROUTING_MATRIX_Q[empty_car_routing_from-1]
    )
    empty_car_matrix[empty_car_routing_from-1][empty_car_routing_to-1] += 1 # 空车矩阵增加
    if(empty_car_routing_from == empty_car_routing_to):
        return  # 无需空车调度
    empty_car_routing_time = 1
    empty_car_routing_event = Event(
        empty_car_routing_from,
        empty_car_routing_to,
        event._time + empty_car_routing_time,
        E_EMPTY_CAR_ARRIVE
    )
    heap.push(empty_car_routing_event, event._time + empty_car_routing_time)
           
    
def empty_car_arrive(event):
    empty_car_matrix[event._from-1][event._to-1] -= 1
    empty_car_matrix[event._to-1][event._to-1] += 1


if __name__ == "__main__":

    epoch = 0
    timestamp_list = []
    
    # 处理事件队列（堆）
    while(not heap.empty()):
        item = heap.pop()
        cur_event = item[2]
        # print(cur_event)
        
        if(cur_event._etype == E_PASSENGER_ARRIVE):
            passenger_arrive(cur_event)
        elif(cur_event._etype == E_FULL_CAR_ARRIVE):
            full_car_arrive(cur_event)
        elif(cur_event._etype == E_EMPTY_CAR_ARRIVE):
            empty_car_arrive(cur_event)
           
        
        timestamp = np.floor(cur_event._time)
        
        if((timestamp + 1) % TIME_INTERVAL == 0 and timestamp not in timestamp_list):
            # print(timestamp)
            timestamp_list.append(timestamp)
            epoch += 1
            availability = np.divide(passenger_satisfied_count, passenger_arrived_count)
            print(availability)
            # passenger_satisfied_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA)
            # passenger_arrived_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA)
            
        if(epoch == EPOCH_NUM):
            break
        

        



    