# -*- coding:UTF-8 -*-
import os
import sys
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets


def show_position(array, c=None):
    # if c:
    #     color = ['blue', 'green', 'red']
    #     nc = []
    #     for i in range(len(c)):
    #         nc.append(color[c[i]])
    # else:
    #     nc = None
    array = np.array(array)
    plt.figure()
    plt.scatter(array[:, 0], array[:, 1], c=c)
    plt.show()


def distance(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))


def k_means(dataset, k=2):
    # 初始化群中心
    c_list = []
    for x in range(k):
        c_list.append(dataset[x])

    # 初始化點標籤 (will be return
    d_labels = [-1] * len(dataset)

    while True:
        old_labels = d_labels.copy()
        # 計算點與群中心距離 且更新點標籤
        for x in range(len(dataset)):
            temp_mini = float("inf")
            for c in range(k):
                temp = distance(dataset[x], c_list[c])
                if temp_mini > temp:
                    temp_mini = temp
                    d_labels[x] = c
        # print(d_labels)
        # show_position(dataset, d_labels)

        # 更新群中心
        # show_position(c_list)
        for c in range(k):
            temp_p = [0, 0]
            temp_t = 0
            for i in range(len(dataset)):
                if d_labels[i] == c:
                    temp_t += 1
                    temp_p[0] += dataset[i][0]
                    temp_p[1] += dataset[i][1]
            temp_p[0] /= temp_t
            temp_p[1] /= temp_t
            c_list[c] = temp_p
        # show_position(c_list)
        if d_labels == old_labels:
            break
    return d_labels


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    # dataset = [
    #     [60, 9],
    #     [65, 10],
    #     [75, 15],
    #     [80, 11],
    #     [85, 17]
    # ]
    # dataset = []
    # with open('data.csv', 'r', encoding='utf8') as csvfile:
    #     rows = csv.reader(csvfile)
    #     for row in rows:
    #         p = list(map(int, row))
    #         dataset.append(p)
    # dataset = [[0, 0], [0, 1], [1, 1], [1, 0]]

    X1, y1=datasets.make_circles(n_samples=500, factor=0.5, noise=.05, random_state=9)
    X2, y2 = datasets.make_blobs(n_samples=100, n_features=2, centers=[[1.2,1.2]], cluster_std=[[.1]],random_state=9)
    
    dataset = np.concatenate((X1, X2))
    new_labels = k_means(dataset, 3)
    show_position(dataset, new_labels)
