import numpy as np

def random_allocation(total_num, group):
    """
    generate a list. The length of the list is [group]. The summation of the list is [total_num]
    """
    a = [np.random.randint(0, total_num) for i in range(group - 1)]
    a.append(0)
    a.append(total_num)
    a.sort()

    b = [a[i+1]-a[i] for i in range (group)]

    return np.array(b)


def normalize(arr, total):
    """归一化，也就是求概率"""
    return np.array(arr) / total


# def matrix_round(matrix):
#     """对矩阵进行取整"""
#     row_sum = np.sum(matrix,axis=1)
#     row, col = np.diag_indices_from(matrix)
#     matrix[row,col] = 0 # 清除对角线元素
#     matrix = np.floor(matrix)   # 其余元素向下取整
#     diag = row_sum - np.sum(matrix, axis=1)
#     matrix[row,col] = np.array(diag)
#     return matrix

# def poisson_arrival_with_capacity(lambda_):
#     temp = np.random.poisson(lambda_)
#     return lambda_ if lambda_ < temp else temp
