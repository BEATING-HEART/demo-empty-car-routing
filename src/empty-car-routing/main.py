import os, sys
from joblib import PrintTime
sys.path.append(os.getcwd())    # 添加根目录为path

import numpy as np
from data.initial import (
    CAR_DISTRIBUTION_INITIAL,
    CAR_NUM,
    ORIGINAL_MATRIX_E,
    ORIGINAL_MATRIX_F,
    REGION_NUM, 
    TRAVEL_MATRIX_P, 
    EMPTY_CAR_ROUTING_MATRIX_Q,
    ORIGINAL_AVAILABILITY,
    PASSENGER_ARRIVIAL_LAMBDA,
    PASSENGER_INITIAL,
    TRAVEL_TIME_MU,
    # ORIGINAL_MATRIX_E_MEAN,
    # ORIGINAL_MATRIX_F_MEAN
)
from utils.utils import  matrix_round, normalize, poisson_arrival_with_capacity

def iteration(time):
    availability = ORIGINAL_AVAILABILITY
    matrix_f = ORIGINAL_MATRIX_F
    # matrix_f_mean = ORIGINAL_MATRIX_F_MEAN
    matrix_e = ORIGINAL_MATRIX_E
    # matrix_e_mean = ORIGINAL_MATRIX_E_MEAN
    passenger_matrix = PASSENGER_INITIAL
    car_distribution = CAR_DISTRIBUTION_INITIAL
    # print(np.random.poisson(800, size=int(time)))
    # print(np.cumsum(np.random.poisson(800, size=int(time))))
    for t in range(time):

        passenger_remain = passenger_matrix - car_distribution
        passenger_remain[passenger_remain < 0] = 0
        # passenger remain 剩下的乘客数
        full_car_total = passenger_matrix - passenger_remain
        # full car out total: 当前周期内新增的出发满车
        cars_remain = car_distribution - full_car_total
        # cars remain 剩下的车数

        full_car_towards = np.multiply(full_car_total, TRAVEL_MATRIX_P.T).T
        full_car_towards = matrix_round(full_car_towards)
        # full car towards 当前周期内，各方向上新增的满车。由 full car out total 分配得到

        matrix_f += full_car_towards
        # matrix f 是 full car out 在各方向上的量  包含了上一个周期剩下的，和这个周期新增的

        poisson_arrival_with_capacity_vector = np.vectorize(poisson_arrival_with_capacity)
        car_arrival_matrix = poisson_arrival_with_capacity_vector(matrix_f)
        # full car out arrival 是满车到达目的地的量，即在目的地转为了空车的量

        full_car_remain = matrix_f - car_arrival_matrix
        matrix_f = full_car_remain 
        # full car remain 是剩下的满车，也就转入了下一个周期。


        car_arrival = np.sum(car_arrival_matrix, axis=0)
        # 记录了到达不同区域空车的情况。

        empty_car_routing = np.multiply(full_car_total, EMPTY_CAR_ROUTING_MATRIX_Q.T).T
        car_distribution = car_distribution + car_arrival - np.sum(empty_car_routing, axis=)
        

        # cars_update = cars_remain + np.sum(full_car_arrival, axis=0)
        # full car arrival 满车到达之后更新空车分布

        # 计算剩下的乘客。
        # passenger_matrix -= car_distribution # 流出
        # passenger_matrix[passenger_matrix < 0] = 0 
        # passenger_matrix += 


        # 只考虑流出，计算剩下的车
        # print(passenger_matrix)
        # 人怎么变?出去的加上到达的。
            # 出去的怎么算，总和乘以可用率。（人数减去车数。）
            # 到达的怎么算，自己到自己和别人到自己。
                # 概率乘以可用率。P矩阵第i行第j列和对应区域i可用率对应相乘求和。得到人数
    # print(passenger_matrix)
    print("passenger remain", passenger_remain)
    print("cars remain", cars_remain)
    print("full car total", full_car_total)
    print("travel matrix P", TRAVEL_MATRIX_P)
    print("full car towards", full_car_towards)
    print("full car arrival", car_arrival_matrix)
    # print("cars update", cars_update)
    print("car arrival", car_arrival)
    print("routing matrix q", EMPTY_CAR_ROUTING_MATRIX_Q)
    print("empty_car_routing", empty_car_routing)

    
    print(str(time)+"xxxxxx")


if __name__ == "__main__":
    print(ORIGINAL_AVAILABILITY)
    # print(TRAVEL_MATRIX_P)
    # print(ORIGINAL_AVAILABILITY)
    iteration(1)
    # print(ORIGINAL_MATRIX_E_MEAN)
    # print(normalize(ORIGINAL_MATRIX_E, CAR_NUM))
    


# https://cloud.tencent.com/developer/article/1642626 泊松过程的模拟