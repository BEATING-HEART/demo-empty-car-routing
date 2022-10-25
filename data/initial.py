import numpy as np

from utils.utils import random_allocation

REGION_NUM = 2  
"""region number in the system"""

CAR_NUM = 1200
"""total car in the system"""

CAR_DISTRIBUTION_INITIAL = random_allocation(CAR_NUM, REGION_NUM)
"""car distribucation (initial)"""