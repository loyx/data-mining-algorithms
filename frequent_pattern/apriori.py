""" Apriori algorithm"""
from time import time

from .trandataset import *


def apriori(dataset, support):
    """ main method """
    print("Apriori algorithm:")
    msg = "\tfrequent {}-itemset found."

    frequent_set: FrequentItemSet = findFrequent1ItemSet(dataset, support)
    print(msg.format(1))

    cnt = 2
    frequent_k = frequent_set
    while True:
        candidate = aprioriGen(frequent_k)
        for tran in dataset:
            ct = candidate.getSubset(tran)
            for ft in ct:
                ft.support += 1
        frequent_k = candidate.getSubsetWithSupport(support)
        if len(frequent_k) == 0:
            break
        frequent_set += frequent_k
        print(msg.format(cnt))
        cnt += 1
    return frequent_set


def aprioriGen(frequent_set: FrequentItemSet):
    """ generate candidate set"""
    candidate = FrequentItemSet()
    for tran1, tran2 in combinations(frequent_set, 2):  # 要求 frequent set 内部有序
        try:
            c = tran1 + tran2
        except TypeError:
            pass
        else:
            if not hasInfrequentSubset(c, frequent_set):
                candidate.addTransaction(c)
    return candidate


def hasInfrequentSubset(c: Transaction, itemset: FrequentItemSet):
    """ use prior knowledge to prune """
    for sub_tran in c.k1_Subset():
        if sub_tran not in itemset:
            return True
        return False


if __name__ == '__main__':

    start = time()

    database = "dataset/chess.dat"
    data = read_csv(database, set)
    total = len(data)
    p = 0.8
    print(database)
    print("data size:{}, min_support:{:.3f}%, support_count:{}"
          .format(total, p*100, int(p*total)))
    # frequent_itemset = apriori(data, int(p*total))
    frequent_itemset = apriori(data, 2)
    print(frequent_itemset)

    end = time()
    print("total time:{}".format(end - start))
