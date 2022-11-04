# passenger generator
from operator import index
import numpy as np
from data.constants import E_PASSENGER_ARRIVE
from models.event import Event
from models.heap import heap


# https://www.liaoxuefeng.com/wiki/1016959663602400/1017318207388128

converged = False

def passenger_generator(rate, region_index):
    """passenger gererator with poisson arrival. The parameter of poisson arrival is rate."""
    t = 0
    heap.push(Event(0,region_index, t, E_PASSENGER_ARRIVE), t)
    yield('region' + str(region_index) + 'arrival')

    while(not converged):
        time_interval = np.random.exponential(scale=1/rate, size=None)
        t += time_interval
        heap.push(Event(0,region_index, t, E_PASSENGER_ARRIVE), t)
        yield

    
        # yield event
        # pass

def get_passenger_gen_arr(region_number, passenger_arrival_lambda):
    p_gen_arr = []
    r_index = 1
    for _lambda in passenger_arrival_lambda:
        gen = passenger_generator(_lambda, r_index)
        next(gen)
        p_gen_arr.append(gen)
        r_index += 1
        # p_gen_arr.append
    return p_gen_arr