# -*- coding:utf8 -*-
import os
import time
import gc
from trie import Trie

def apriori(dataset, min_sup, level=1, before_itemset=[]):
    # if level > 2:
    #     return
    print('\n----------------------------------------')
    print('Level:{}\n'.format(level))
    itemsets = []  # ['set1', 'set2', 'set3']
    itemsup = []

    # Step1. Get Itemset
    # Step2. Get Support
    if level == 1:  # 第一次特判，因為表比較好生成
        for dset in dataset:
            for d in dset:
                if not d in itemsets:  # 如果是新的資料
                    itemsets.append(d)  # 新增資料到 itemsets
                    itemsup.append(1)  # 並且新增 1 到 itemsup
                else:
                    itemsup[itemsets.index(d)] += 1  # 若已經有出現過，則將對應 index 的 itemsup 增加 1
    else:  #  
        # 儲存可能會出現的 itemset
        # 先抓取所有的 prefix 和 d
        save_prefix = {}
        for dset in before_itemset:
            if level == 2:  # 特判第二層
                prefix = tuple('')  # 若是第二層假設他的 prefix 皆為空字串
                dset = [dset]
            else:  # 若不是第二層將 prefix 取出來
                prefix = tuple(dset[:-1])  # prefix 為陣列的最開始到倒數第二個(第一個之前)
            if not prefix in save_prefix:  # 如果是新的 prefix
                save_prefix[prefix] = [dset[-1]]  # 記錄到 save_prefix 這個 dictionary
            else:
                save_prefix[prefix].append(dset[-1])  # 若不是新的則將陣列最後一個加入

        # 將同一個 prefix 的 d 做 cross 後前面加上 prefix
        print('Cross')
        if level != 2:  # 特判第二層，若不是第二層不用下列的檢查，就不需要轉成特定的 set 型態
            before_itemset = set(map(tuple, before_itemset))
        for prefix, sets in save_prefix.items():  # 將 save_prefix 讀出來開始處理
            # print(prefix, sets)
            for i in range(len(sets)):  # 巢狀迴圈
                for j in range(i+1, len(sets), 1):  # 將所有相同 prefix 的 d 做 cross
                    temp_items = []
                    if level == 2:  # 特判第二層，第二層則不用做檢查
                        temp_items = [sets[i], sets[j]]
                        temp_items.sort()
                        itemsets.append(temp_items)
                    else:
                        temp_items = list(prefix) + [sets[i], sets[j]]
                        temp_items.sort()
                        # 這邊是檢查如果 cross 後的 itemset 子集合不在 before_itemset 的話不採用
                        check_flag = True
                        for x in range(level-2, -1, -1):
                            if not tuple(temp_items[:x] + temp_items[x+1:]) in before_itemset:
                                check_flag = False
                                break
                        if check_flag:
                            itemsets.append(temp_items)

        if len(itemsets) == 0:  # 特判如果 itemsets 長度為零表示已經沒有必要繼續做下去了
            print('done.')
            return

        print('Create Itemset Tree')  # 建立 Itemsets 的字典樹，以便計算次數使用
        item_tree = Trie()
        for i, items in enumerate(itemsets):
            item_tree.insert(items, i)

        print('Count')  # 開始計算各個 Itemset 的數量
        itemsets_len = len(itemsets)
        itemsup = [0] * itemsets_len  # 先建立一個與 Itemset 長度一樣的0陣列
        for dset in dataset:  # 開始對所有資料進行迴圈
            flag = [item_tree.root]  # 紀錄 flag，flag 為走過的位置
            for d in dset:
                for fi in range(len(flag)-1, -1, -1):  # 對所有走過的位置進行位置
                    child_index = flag[fi].get_index(d)  # 尋找是否存在在小孩裡
                    if child_index != -1:  # 如果存在
                        if not flag[fi].child[child_index].is_leaf():  # 如果不是葉節點
                            flag.append(flag[fi].child[child_index])  # 將走到的這個點記錄下來
                        else:  # 若是葉節點
                            itemsup[flag[fi].child[child_index].extend_i] += 1  # 將對應的 itemsup 值增加 1
                            
        print('Delete Itemset Tree')
        del item_tree  # 清除字典樹已釋放記憶體
        gc.collect()
        
    # Step3. Delete values below threshold
    # 砍掉低於門檻(min_sup)的資料
    cnt = 0
    while True:
        if itemsup[cnt] < min_sup:
            del itemsets[cnt]
            del itemsup[cnt]
        else:
            cnt += 1
        if cnt >= len(itemsets):
            break
    print('itemsets length: {}'.format(len(itemsets)))
    for x in range(len(itemsets)):
        print('{} {}'.format(itemsets[x], itemsup[x]))

    apriori(dataset=dataset, min_sup=min_sup, level=level+1, before_itemset=itemsets)


if __name__ == "__main__":
    now = time.time()
    os.chdir(os.path.realpath(os.path.dirname(__file__)))  # ?

    # filename = 'small.txt'
    # filename = 'T15I7N0.5KD1K.txt'
    filename = 'T10I4D100K.dat'
    split_text = ' '
    # split_text = ','

    min_sup = 1000

    dataset = []
    with open(filename, 'r', encoding='utf8') as f:
        for line in f.readlines():
            temp = line.strip().split(split_text)
            temp = list(map(int, temp))
            temp.sort()
            dataset.append(temp)

    # for x in range(10):
    #     print('{: 3d} {}'.format(x + 1, dataset[x]))

    apriori(dataset=dataset, min_sup=min_sup)
    print('Used: {:.3f} sec'.format(time.time()-now))
