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
"""travel probability matrix of the system."""

