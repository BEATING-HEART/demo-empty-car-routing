from ctypes.wintypes import SIZE
import numpy as np

from utils.utils import random_allocation

REGION_NUM = 2  
"""region number in the system"""

CAR_NUM = 1200
"""total car in the system"""

CAR_DISTRIBUTION_INITIAL = random_allocation(CAR_NUM, REGION_NUM)
# CAR_DISTRIBUTION_INITIAL = np.random.dirichlet(np.ones(REGION_NUM), size=1)
"""car distribucation (initial)"""

TRAVEL_MATRIX_P = np.random.dirichlet(np.ones((REGION_NUM)), size=REGION_NUM)
"""size=[r region * r region], travel probability matrix of the system."""

PASSENGER_ARRIVIAL_LAMBDA = np.array([800, 400])
"""size=[1 * r region], corresponding to the lambda of each region."""

# PASSENGER_INITIAL = np.random.poisson(PASSENGER_ARRIVIAL_LAMBDA)

# TRAVEL_TIME_MU = np.ones((REGION_NUM, REGION_NUM)) 
# """size=[r region * r region], corresponding to the parameter mu."""

EMPTY_CAR_ROUTING_MATRIX_Q = np.array([
    [1, 0],
    [0, 1]
])
"""size=[r region * r region], empty car routing matrix of the system."""

# TIME_INTERVAL = 500
# """system total running time. (epoch)"""

ORIGINAL_MATRIX_E = np.diag(CAR_DISTRIBUTION_INITIAL)
"""original empty car matrix. (all cars are empty)"""

ORIGINAL_MATRIX_F = np.zeros((REGION_NUM, REGION_NUM))
"""original full car matrix. (no car is full)"""

# ORIGINAL_AVAILABILITY = np.clip(np.divide(CAR_DISTRIBUTION_INITIAL, PASSENGER_INITIAL), 0, 1)
# """original car availability."""

# ORIGINAL_MATRIX_F_MEAN = ORIGINAL_MATRIX_F / CAR_NUM

# ORIGINAL_MATRIX_E_MEAN = ORIGINAL_MATRIX_E / CAR_NUM