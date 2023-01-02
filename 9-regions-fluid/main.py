import cvxpy as cp
import numpy as np

from parameters import (
    REGION_NUMBER,
    TRAVEL_MATRIX_P,
    RECIPROCAL_MU_MATRIX,
    CUSTOMER_ARRIVIAL_LAMBDA
)



if __name__ == "__main__":
    
    p_matrix = cp.Parameter((REGION_NUMBER, REGION_NUMBER), nonneg=True, value=TRAVEL_MATRIX_P)  # ok
    lambda_vector = cp.Parameter(REGION_NUMBER, nonneg=True, value=CUSTOMER_ARRIVIAL_LAMBDA)   # ok
    # mu_matrix = cp.Parameter((REGION_NUMBER, REGION_NUMBER), nonneg=True, value=RECIPROCAL_MU_MATRIX)    # ok
    mu_matrix = cp.Parameter((REGION_NUMBER, REGION_NUMBER), nonneg=True, value=np.reciprocal(RECIPROCAL_MU_MATRIX))    # ok
    
    availability_vector = cp.Variable(REGION_NUMBER, pos=True)
    e_matrix = cp.Variable((REGION_NUMBER, REGION_NUMBER), pos=True)
    f_matrix = cp.Variable((REGION_NUMBER, REGION_NUMBER), pos=True)
    
    
    obj_expression = 0
    sup_reward = 0
    car_sum = 0
    constraints = []
    # constraints += [sum(e_matrix) + sum(f_matrix) == 1]
    for i in range(REGION_NUMBER):
        for j in range(REGION_NUMBER):
            obj_expression += availability_vector[i] * lambda_vector[i] * p_matrix[i, j]    # objective function
            sup_reward += lambda_vector.value[i] * p_matrix.value[i][j] # sup_reward (availability = 1)
            # sup_reward += lambda_vector.value[i] * availability_vector.value
            constraints += [lambda_vector[i] * p_matrix[i, j] * availability_vector[i] == mu_matrix[i, j] * f_matrix[i, j]]
            # if j != i:
            #     constraints += [mu_matrix[i, j] * e_matrix[i, j] <= mu_matrix[:, i] @ f_matrix[:, i]]
            constraints += [e_matrix[i, j] >= 0, e_matrix[i, j] <= 1, f_matrix[i, j] >= 0, f_matrix[i, j] <= 1]
            car_sum += (e_matrix[i, j] + f_matrix[i, j])
            
        # constraints += [mu_matrix[:, i] @ e_matrix[:, i] - mu_matrix[i, i] * e_matrix[i, i] <= lambda_vector[i] * availability_vector[i]]
        # constraints += [lambda_vector[i] * availability_vector[i] <= mu_matrix[:, i] @ e_matrix[:, i] - mu_matrix[i, i] * e_matrix[i, i] + mu_matrix[:, i] @ f_matrix[:, i]]
        constraints += [lambda_vector[i] * availability_vector[i] + mu_matrix[i, :] @ e_matrix[i, :] - mu_matrix[i, i] * e_matrix[i, i] 
                        == mu_matrix[:, i] @ e_matrix[:, i] - mu_matrix[i, i] * e_matrix[i, i] + mu_matrix[:, i] @ f_matrix[:, i]]
        constraints += [availability_vector[i] >= 0, availability_vector[i] <= 1]
        # constraints += [(1-availability_vector[i]) * e_matrix[i][i] == 0]
    constraints += [car_sum == 1]    
    

    
    obj_func = cp.Maximize(obj_expression)
    prob = cp.Problem(obj_func, constraints)
    
    prob.solve()
    
    print(prob.status)
    print(prob.value)
    # print(sup_reward)
    # print(prob.value / sup_reward)
    
    # tmp = 0
    # for i in range(REGION_NUMBER):
    #     tmp += lambda_vector.value[i] * availability_vector.value[i]
    # print(tmp)    
    
    # print(np.round(availability_vector.value, decimals=5))
    # print(np.round(e_matrix.value, decimals=5))
    # print(np.round(f_matrix.value, decimals=5))
    
    # print(p_matrix.value)
    # print(mu_matrix.value)
    # print(lambda_vector.value)
    
    # print(np.dot(availability_vector.value, lambda_vector.value))
    # print(np.sum(lambda_vector.value))
    
    print(np.dot(availability_vector.value, lambda_vector.value) / np.sum(lambda_vector.value))
    
    
    
    # print(p_matrix.value)
    # print(mu_matrix.value)
    # print(lambda_vector.value)
    
    q_matrix = np.zeros((REGION_NUMBER, REGION_NUMBER))
    for i in range(REGION_NUMBER):
        denominator = mu_matrix.value[:, i] @ f_matrix.value[:, i]
        for j in range(REGION_NUMBER):
            if i == j:
               q_matrix[i, j] = lambda_vector.value[i] * availability_vector.value[i] - (mu_matrix.value[:, i] @ e_matrix.value[:, i] - mu_matrix.value[i, i] * e_matrix.value[i, i])
            else:
                q_matrix[i, j] = mu_matrix.value[i, j] * e_matrix.value[i, j]
            q_matrix[i, j] /= denominator
    
    print(np.round(q_matrix, decimals=5))
    # print(np.sum(TRAVEL_MATRIX_P, axis=1))
    # print(np.reciprocal(RECIPROCAL_MU_MATRIX))

    # print(p_matrix.value[i, :] @ mu_matrix.value[i, :])