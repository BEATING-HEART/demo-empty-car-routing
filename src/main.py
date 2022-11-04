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
    E_EMPTY_CAR_ARRIVE
)

sys.path.append(os.getcwd())    # 添加根目录为path

if __name__ == "__main__":
    
    # print(heap.empty())

    # 初始化生成器
    passenger_gen_arr = get_passenger_gen_arr(REGION_NUM, PASSENGER_ARRIVIAL_LAMBDA)
    """passenger generator. 下标需要加减"""

    full_car_matrix = ORIGINAL_MATRIX_F
    empty_car_matrix = ORIGINAL_MATRIX_E

    # print("full car matrix", full_car_matrix)
    # print("empyt car matrix", empty_car_matrix)

    region_index_arr = np.arange(start=1, stop=REGION_NUM+1)

    time_index = 0

    passenger_arrival_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA) 
    passenger_satisfied_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA)
    
    # 处理事件队列（堆）
    while(not heap.empty()):
        item = heap.pop()
        cur_event = item[2]
        print(cur_event)
        e_from = cur_event._from
        e_to = cur_event._to
        e_time = cur_event._time
        e_type = cur_event._etype
        print(empty_car_matrix)
        print(full_car_matrix)

        if(np.floor(e_time) - time_index > 1):
            time_index += 1
            # 计算availability
            availability = np.divide(passenger_satisfied_count, passenger_arrival_count)
            print("*******")
            # print(passenger_satisfied_count)
            # print(passenger_arrival_count)
            # print(full_car_matrix)
            # print(empty_car_matrix)
            print(availability)
            time_index = np.floor(e_time)
            passenger_arrival_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA) 
            passenger_satisfied_count = np.zeros_like(PASSENGER_ARRIVIAL_LAMBDA)
            # np.where(passenger_arrival_count > 0, passenger_arrival_count, 0)
            # np.where(passenger_satisfied_count > 0, passenger_satisfied_count, 0)
            if(time_index == 1):
                break

        if(e_type == E_PASSENGER_ARRIVE):
            # 乘客到达 e_to ，生成下一个到达e_to的乘客。
            try:
                next(passenger_gen_arr[e_to - 1])
                # print('passenger arrives region' + str(e_to))
                passenger_arrival_count[e_to - 1] += 1
            except StopIteration:
                print('乘客不再到达')
            
            if (empty_car_matrix[e_to - 1][e_to - 1] != 0):
                # 乘客到达e_to，且e_to这个位置有车，那么被满足。
                passenger_satisfied_count[e_to - 1] += 1

                # 随即这辆车被乘客占用，转而向下一个目的地出发。
                empty_car_matrix[e_to - 1][e_to - 1] -= 1

                # 到达区域为 e_to。随即转变为出发地
                passenger_travel_from = e_to

                # 根据P矩阵，决定乘客下一步去哪里。
                passenger_travel_to = np.random.choice(
                    region_index_arr, p=TRAVEL_MATRIX_P[passenger_travel_from-1]
                )
                
                # 生成乘客的旅行时间。
                passenger_travel_time = 1
                # passenger_travel_time = np.random.exponential(scale=1, size=None)
                
                # 生成乘客的到达目的地的事件
                event_passenger_arrival = Event(
                    passenger_travel_from, 
                    passenger_travel_to, 
                    e_time + passenger_travel_time,
                    E_FULL_CAR_ARRIVE
                )
                heap.push(event_passenger_arrival, e_time + passenger_travel_time)

                # 乘客出发，造成满车矩阵变化。
                full_car_matrix[passenger_travel_from - 1][passenger_travel_to - 1] += 1

            else:
                # 乘客到达，但没车，则乘客流失
                pass

        elif(e_type == E_FULL_CAR_ARRIVE):

            # 满车到达后，满车矩阵减少
            full_car_matrix[e_from - 1][e_to - 1] -= 1

            # 满车到达点 e_to 就是空车调度的起始点。
            empty_car_routing_from = e_to

            # 计算空车调度的目的地
            empty_car_routing_to = np.random.choice(
                region_index_arr, p=EMPTY_CAR_ROUTING_MATRIX_Q[empty_car_routing_from - 1]
            )
            # print("full car from " +str(e_from)+ " to " + str(e_to) + "arrives")
            
            # 更新空车矩阵
            empty_car_matrix[empty_car_routing_from - 1][empty_car_routing_to - 1] += 1

            # 生成空车调度事件
            if(empty_car_routing_to != empty_car_routing_from):

                empty_car_routing_time = 1
                # empty_car_routing_time = np.random.exponential(scale=1, size=None)

                # 生成空车调度到达事件
                empty_car_routing_arrive = Event(
                    empty_car_routing_from,
                    empty_car_routing_to,
                    e_time + empty_car_routing_time,
                    E_EMPTY_CAR_ARRIVE
                )
                heap.push(empty_car_routing_arrive, e_time + empty_car_routing_time)
 
        elif(e_type == E_EMPTY_CAR_ARRIVE):
            # 空车到达，更新空车矩阵。
            empty_car_matrix[e_from - 1][e_to - 1] -= 1
            empty_car_matrix[e_to - 1][e_to - 1] += 1   

        



    