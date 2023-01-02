import numpy as np
import heapq
from parameters import MATRIX_P, CONST_PASSENGER_ARRIVAL, MATRIX_MU
from simulator import simulator
from utils import random_allocation

if __name__ == '__main__':
    
    # test = None
    # print(test)
    # print(simulator.pass_total)
    # for i in range(10): 
    #     e = heapq.heappop(simulator.heap)
    #     if (e.type == CONST_PASSENGER_ARRIVAL):
    #         simulator.pass_arrival_handler(e)
        
        # print(heapq.nsmallest(9, simulator.heap))
        
        
        
    # simulator.run(e_cnt=1e6)
    # simulator.run_time(time=300, time_window=20)
    simulator.run_cnt(e_cnt=1e6, e_cnt_window= 1e5)
    # print(simulator.E)
    # print(simulator.heap)