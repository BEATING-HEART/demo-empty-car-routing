# passenger generator
import numpy as np
from data.constants import CONVERGED

# https://www.liaoxuefeng.com/wiki/1016959663602400/1017318207388128

def passenger_generator(rate):
    """passenger gererator with poisson arrival. The parameter of poisson arrival is rate."""
    t = 0
    # yield event
    while(not CONVERGED):
        time_interval = np.random.exponential(scale=1/rate, size=None)
        t += time_interval
        # yield event
        
        # pass