# -*- coding:UTF-8 -*-
import numpy
import math
import os
import sys


def my_entropy(i):
    if i == 0.0 or i == 1.0:
        return 0
    else:
        return i * math.log(i, 2)


def id3(dataset, attribute_num=None):
    # 算出預設屬性個數
    if attribute_num is None:
        attribute_num = len(dataset[0]) - 1
    # print('attribute_num', attribute_num)

    # 算出資料表總個數
    total_len = len(dataset)
    # print('total_len', total_len)

    # 算出資料表Class數量和分別的個數
    top_class_set = {}
    for i in range(total_len):
        if not dataset[i][-1] in top_class_set:
            top_class_set[dataset[i][-1]] = 1
        else:
            top_class_set[dataset[i][-1]] += 1
    # print('top_class_set', top_class_set)

    # 算出資料表的 entropy
    top_entropy = 0
    for _, v in top_class_set.items():
        top_entropy += my_entropy(v / total_len)
    top_entropy = -top_entropy
    # print('top_entropy', top_entropy)

    # 如果資料表呈現完全不雜亂則表示指向同一個答案
    if top_entropy == 0:
        for k, v in top_class_set.items():
            if v != 0:
                return {'root': k}

    # 計算資料表中最小的 entropy
    mini_entropy = {'a_index': -1, 'guard': None, 'entropy': float('inf')}
    for x in range(attribute_num):
        guard_histroy = set()
        for i in range(total_len):
            guard = dataset[i][x]
            # guard = float(guard)
            if not guard in guard_histroy: # 防止一樣的 guard 重複計算
                guard_histroy.add(guard) # 
                # print(x, guard)
                # input()  # DEBUG
                temp = [[0]*len(top_class_set), [0]*len(top_class_set)]  # [<=, >]
                temp_total = [0, 0]  # [<=, >]
                for j in range(total_len):
                    if dataset[j][x] <= guard:
                        temp[0][list(top_class_set.keys()).index(dataset[j][-1])] += 1
                        temp_total[0] += 1
                    else:  # dataset[j][attribute_num] > guard
                        temp[1][list(top_class_set.keys()).index(dataset[j][-1])] += 1
                        temp_total[1] += 1

                guard_entropy = 0
                for g in range(2):
                    temp_entropy = 0
                    for v in temp[g]:
                        if temp_total[g] != 0:
                            temp_entropy += my_entropy(v / temp_total[g])
                        else:
                            temp_entropy += 0
                    temp_entropy = -temp_entropy
                    guard_entropy += temp_entropy * temp_total[g] # 加重
                guard_entropy /= (temp_total[0] + temp_total[1]) # 平均

                if guard_entropy <= mini_entropy['entropy']:
                    mini_entropy['entropy'] = guard_entropy
                    mini_entropy['a_index'] = x
                    mini_entropy['guard'] = guard
                # print()
                # print('guard_entropy', guard_entropy)
                # print('mini_entropy', mini_entropy)
                # print(i, temp)
                # input()  # DEBUG
    # print(dataset[0][0])
    # print('mini_entropy', mini_entropy)

    # 將資料表二分 並遞迴下去
    # Do something.
    newdataset = sorted(dataset, key=lambda a:a[mini_entropy['a_index']])
    split_index = len(newdataset) - 1
    while True:
        if mini_entropy['guard'] < newdataset[split_index][mini_entropy['a_index']]:
            split_index -= 1
        else:
            split_index += 1
            break
    # print(split_index)
    # for i, x in enumerate(newdataset):
    #     print(i, x)
    # input()
    child_trees = [None] * 2
    child_trees[0] = id3(newdataset[:split_index], attribute_num)
    child_trees[1] = id3(newdataset[split_index:], attribute_num)
    result = {
        'root': mini_entropy['a_index'],
        'context': {
            'guard': mini_entropy['guard'],
            'child': child_trees
        }
    }
    return result

def draw_tree(tree, attribute, level=0):
    padding = '__' * level
    if 'context' in tree:
        print(attribute[result['root']])
        print('{}{}{}'.format(padding, '<=', tree['context']['guard']), end='---')
        draw_tree(tree['context']['child'][0], attribute, level+1)
        print('{}{}{}'.format(padding, '>', tree['context']['guard']), end='---')
        draw_tree(tree['context']['child'][1], attribute, level+1)
    else:
        print(tree['root'])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    dataset = []
    filename = 'iris.data'
    with open(filename, 'r') as f:
        for line in f.readlines():
            temp = line.strip()
            if temp != '':
                dataset.append(temp.split(','))

    '''
    TREE = {
        'root': 'petal_length',
        'context': {
            'guard': 1.9,
            'child': [
                CHILD_TREE,
                CHILD_TREE
            ]
        }
    }
    '''
    result = id3(dataset)
    print(result)
    attribute = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    print('\n\n**********\n\n')
    # print(attribute[result['root']])
    draw_tree(result, attribute)
    