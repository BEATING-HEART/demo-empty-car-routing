import numpy as np
import heapq
from parameters import (
    MATRIX_P,
    MATRIX_MU,
    MATRIX_Q,
    VECTOR_LAMBDA,
    REGION_NUM,
    CAR_NUM,
    CONST_PASSENGER_ARRIVAL,
    CONST_FULLCAR_ARRIVAL,
    CONST_EMPTYCAR_ARRIVAL
)
from utils import random_allocation
from event import Event

class Simulator:
    
    def __init__(self):
        self.P = MATRIX_P
        self.mu = MATRIX_MU
        self.Q = MATRIX_Q
        self.lbd = VECTOR_LAMBDA
        self.F = np.zeros((REGION_NUM, REGION_NUM))
        # self.E = np.array([[800, 0],[0, 400]])
        self.E = np.diag(random_allocation(CAR_NUM, REGION_NUM))
        
        self.time = 0
        self.cnt = 0
        
        self.heap = [Event(0, CONST_PASSENGER_ARRIVAL, None, i) for i in range(REGION_NUM)]
        heapq.heapify(self.heap)
        
        self.pass_arrived = np.zeros(REGION_NUM)
        self.pass_satisfied = np.zeros(REGION_NUM)
        
    def clear_cnt(self):
        self.pass_arrived = np.zeros(REGION_NUM)
        self.pass_satisfied = np.zeros(REGION_NUM)
        
    # def have_car(self, i):
    #     if(self.E[i][i] > 0):
    #         return True
    #     return False
        
    def pass_arrival_handler(self, e):
        
        # e: passenger arrival event.
        next_pass_arrival_time = e.time + np.random.exponential(scale = 1 / (self.lbd[e.dest] * CAR_NUM))
        heapq.heappush(self.heap, Event(next_pass_arrival_time, CONST_PASSENGER_ARRIVAL, None, e.dest))
        
        self.pass_arrived[e.dest] += 1          # passenger arrival.
        if(self.E[e.dest][e.dest] > 0):
            self.E[e.dest][e.dest] -= 1         # an empty car will be allocated to the passenger.
            self.pass_satisfied[e.dest] += 1    # the passenger is satisfied.
        
            # e_new: full car arrival event.
            e_new_source = e.dest
            e_new_dest = np.random.choice(np.arange(REGION_NUM), p = self.P[e_new_source])
            # e_new_time = e.time + self.mu[e_new_source][e_new_dest]
            e_new_time = e.time + 1 / self.mu[e_new_source][e_new_dest]
            
            heapq.heappush(self.heap, Event(e_new_time, CONST_FULLCAR_ARRIVAL, e_new_source, e_new_dest))
            
            self.F[e_new_source][e_new_dest] += 1
        
    def fullcar_arrival_handler(self, e):
        # e: full car arrival event.
        self.F[e.source][e.dest] -= 1
        
        # e_new: empty car routing arrival event.
        e_new_source = e.dest
        e_new_dest = np.random.choice(np.arange(REGION_NUM), p = self.Q[e_new_source])
        self.E[e_new_source][e_new_dest] += 1
        if(e_new_dest == e_new_source):
            return
        
        # e_new_time = e.time + self.mu[e_new_source][e_new_dest]
        e_new_time = e.time + 1 / self.mu[e_new_source][e_new_dest]
        heapq.heappush(self.heap, Event(e_new_time, CONST_EMPTYCAR_ARRIVAL, e_new_source, e_new_dest))
        
    def emptycar_arrival_handler(self, e):
        self.E[e.source][e.dest] -= 1
        self.E[e.dest][e.dest] += 1
        
    def get_event(self):
        return heapq.heappop(self.heap)    
    
    def run_cnt(self, e_cnt = 1e5, e_cnt_window = None):
        cnt = 0
        if e_cnt_window == None:
            e_cnt_window = e_cnt
        while(cnt < e_cnt):
            e = self.get_event()
            cnt += 1
            if(e.type == CONST_PASSENGER_ARRIVAL): self.pass_arrival_handler(e)
            elif(e.type == CONST_FULLCAR_ARRIVAL): self.fullcar_arrival_handler(e)
            else: self.emptycar_arrival_handler(e)
            
            if(cnt % e_cnt_window == 0):
                print("******* cnt = {!r} *******".format(cnt))
                availability = self.pass_satisfied / self.pass_arrived
                print("availability:", np.round(availability, decimals=5))
                # print(np.dot(availability, self.lbd))
                print("utality:", np.dot(availability, self.lbd) / np.sum(self.lbd))
                print("time:", e.time)
                print("")
                self.clear_cnt()
    
    def run_time(self, time = 300, time_window = None):
        t = 0
        t_old = 0
        if time_window == None:
            time_window = time
        while(t < time):
            e = self.get_event()
            t = e.time
            if(e.type == CONST_PASSENGER_ARRIVAL): self.pass_arrival_handler(e)
            elif(e.type == CONST_FULLCAR_ARRIVAL): self.fullcar_arrival_handler(e)
            else: self.emptycar_arrival_handler(e)
            
            if(np.floor(t) % time_window == 0 and np.floor(t) != t_old):
                print("******* time = {!r} *******".format(np.floor(t)))
                availability = self.pass_satisfied / self.pass_arrived
                print("availability:", np.round(availability, decimals=5))
                # print(np.dot(availability, self.lbd))
                print("utality:", np.dot(availability, self.lbd) / np.sum(self.lbd))
                print("time:", e.time)
                print("")
                self.clear_cnt()
                t_old = np.floor(t)
            
            

simulator = Simulator()