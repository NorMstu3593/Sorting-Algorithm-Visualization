import time        # 计算算法的运行时间
import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class TrackArray():

    def __init__(self, arr):
        """
        初始化时，给TrackArray类一个列表进行追踪排序
        """
        self.arr = np.copy(arr)
        self.reset()           # 重置

    def reset(self):
        self.indices = []      # 索引
        self.values = []       # 值
        self.access_type = []  # 比较类型，get还是set
        self.full_copies = []  # 对每一趟进行存档（每一帧的样子）

    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])

    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):                       # len(arr)
        return self.arr.__len__()


def createRandomValue(number):
    # np.linspace生成平均分布在1到1000范围内的N个数
    arr = np.round(np.linspace(0, 1000, number), 0)
    np.random.seed(0)         # 使用随机种子，保证每个排序算法对同样的序列进行排序
    np.random.shuffle(arr)    # 洗牌，打乱arr的顺序-
    return TrackArray(arr)


def showplt(arr, text):
    fig, ax = plt.subplots()
    ax.bar(np.arange(0, len(arr), 1), arr, align="edge", width=0.8)
    ax.set_xlim([0, len(arr)])
    ax.set(xlabel="Index", ylabel="Value", title=text)
    plt.show()


def showRuntime(time, title):
    print(f"------ {title} -------")
    print(f"Array Sorted in {time*1000:.1f} ms ")


def update(frame):
    text.set_text(f" accesses = {math.floor(frame/2)}")

    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("dodgerblue")
    # 1F77B4
    idx, op = arr.GetActivity(frame)
    if op == "get":
        container.patches[idx].set_color("tomato")
    elif op == "set":
        container.patches[idx].set_color("gold")
    return (*container, text)


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
    showRuntime(dt, title)


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


def SelectSort(arr):
    title = "Select Sort"
    t0 = time.perf_counter()
    for i in range(len(arr)):
        minIndex = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        temp = arr[i]
        arr[i] = arr[minIndex]
        arr[minIndex] = temp
    dt = time.perf_counter() - t0
    showRuntime(dt, title)


def BubbleSort(arr):
    """冒泡排序"""
    title = "Bubble Sort"
    t0 = time.perf_counter()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    dt = time.perf_counter() - t0
    showRuntime(dt, title)


if __name__ == "__main__":
    arr = createRandomValue(30)
    # InsertSort(arr)
    BubbleSort(arr)
    # SelectSort(arr)

    # QuickSort(arr)

    #showplt(arr, "Insert Sort")

    FPS = 60.0
    fig, ax = plt.subplots()
    container = ax.bar(np.arange(0, len(arr), 1), arr, align="edge", width=0.8)
    ax.set_xlim([0, len(arr)])
    ax.set(xlabel="Index", ylabel="Value", title="Select Sort")
    text = ax.text(0, 1000, "")
    ani = FuncAnimation(fig, update, frames=range(
        len(arr.full_copies)), blit=True, interval=100/FPS, repeat=False)
    plt.show()
