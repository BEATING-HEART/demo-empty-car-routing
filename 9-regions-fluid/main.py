import cvxpy as cp
import numpy as np

from parameters import (
    TRAVEL_MATRIX_P,
    RECIPROCAL_MU_MATRIX,
    CUSTOMER_ARRIVIAL_LAMBDA
)



if __name__ == "__main__":
    
    p_matrix = cp.Parameter((9, 9), nonneg=True, value=TRAVEL_MATRIX_P)  # ok
    
    lambda_arrival = cp.Parameter(9, nonneg=True, value=CUSTOMER_ARRIVIAL_LAMBDA)   # ok

    mu_matrix = cp.Parameter((9, 9), nonneg=True, value=np.reciprocal(RECIPROCAL_MU_MATRIX))    # ok
    
    
    
    print(p_matrix.value[0])
    # print((p_matrix @ p_matrix).value)
    
    # print(RECIPROCAL_MU_MATRIX)
    # print(mu_matrix.value)
    
    # pass
