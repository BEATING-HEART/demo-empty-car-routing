import os, sys
sys.path.append(os.getcwd())    # 添加根目录为path

from data.initial import CAR_DISTRIBUTION_INITIAL, TRAVEL_MATRIX_P

if __name__ == "__main__":
    print(CAR_DISTRIBUTION_INITIAL)
    print(TRAVEL_MATRIX_P)


# https://cloud.tencent.com/developer/article/1642626 泊松过程的模拟