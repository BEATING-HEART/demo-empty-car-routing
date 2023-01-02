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