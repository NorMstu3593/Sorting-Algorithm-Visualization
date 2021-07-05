import time        # 计算算法的运行时间
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def createRandomValue(number):
    # np.linspace生成平均分布在1到1000范围内的N个数
    arr = np.round(np.linspace(0, 1000, number), 0)
    np.random.seed(0)         # 使用随机种子，保证每个排序算法对同样的序列进行排序
    np.random.shuffle(arr)    # 洗牌，打乱arr的顺序
    return arr


def showplt(arr, text):
    fig, ax = plt.subplots()
    ax.bar(np.arange(0, len(arr), 1), arr, align="edge", width=0.8)
    ax.set_xlim([0, len(arr)])
    ax.set(xlabel="Index", ylabel="Value", title=text)
    plt.show()


def showRuntime(time, title):
    print(f"------ {title} -------")
    print(f"Array Sorted in {time*1000:.1f} ms ")


def InsertSort(arr):
    title = "Insertion Sort"
    t0 = time.perf_counter()   # 初始时间

    i = 1
    while i < len(arr):
        j = i
        while j > 0 and arr[j-1] > arr[j]:
            arr[j], arr[j - 1] = arr[j-1], arr[j]
            j -= 1
        i += 1

    dt = time.perf_counter() - t0  # 算法运行时间
    showRuntime(dt, title)


def QuickSort(arr):
    title = "Quick Sort"
    t0 = time.perf_counter()
    quicksort(arr, 0, len(arr) - 1)
    dt = time.perf_counter() - t0


def quicksort(A, low, high):
    if low < high:
        p = partition(A, low, high)
        quicksort(A, low, p - 1)
        quicksort(A, p + 1, high)


def partition(A, low, high):
    pivot = A[high]
    i = low
    for j in range(low, high):
        if A[j] < pivot:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[high] = A[high], A[i]
    return i

# animation


if __name__ == "__main__":
    arr = createRandomValue(100)
    showplt(arr, "Unsorted Array")
    # InsertSort(arr)
    QuickSort(arr)
    showplt(arr, "Insert Sort")
