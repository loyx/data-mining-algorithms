""" KNN classifier """
import sys
from queue import PriorityQueue
from util import *


def classifier(k, train_path, test_path, result_path, class_index=-1):
    train_data = list(csvReader(train_path))
    test_data = list(csvReader(test_path))

    for test in test_data[1:]:
        k_heap = PriorityQueue()
        for train in train_data[1:]:
            dist = sum(map(lambda a, b: a == b, test[:-1], train[:-1]))
            if k_heap.qsize() > k:
                k_heap.get()
            k_heap.put((dist, train[-1]))
        count = {}
        while k_heap.qsize():
            label = k_heap.get()
            try:
                count[label[1]] += 1
            except KeyError:
                count[label[1]] = 0
        max_cnt = -1
        label = ""
        for l in count.keys():
            if count[l] > max_cnt:
                max_cnt = count[l]
                label = l
        test[-1] = label

    csvWriter(test_data, result_path)


def main():
    try:
        _, k, train_path, test_path, result_path = sys.argv
    except ValueError:
        k = 3
        train_path = "train.csv"
        test_path = "test.csv"
        result_path = "result1.csv"
    classifier(k, train_path, test_path, result_path)


if __name__ == '__main__':
    main()
