""" naive bayesian learner"""
import sys

from util import *


def learner(data_path, model_path, class_index=-1, laplacian=True):
    data = list(csvReader(data_path))

    ''' get info '''
    attributes = data[0]
    att_len = len(data[0])
    values = [set() for _ in range(att_len)]
    labels = []
    if class_index == -1:
        class_index = att_len-1

    for instance in data[1:]:
        for index, value in enumerate(instance):
            values[index].add(value)
            if index == class_index:
                labels.append(value)

    values = list(map(list, values))
    classes = values[class_index]
    del values[class_index]

    class_cnt = [0] * len(classes)
    model_data = [[[.0 for _ in v] for v in values] for _ in classes]
    for ins_ind, instance in enumerate(data[1:]):
        for att_ind, value in enumerate(instance):
            if att_ind != class_index:
                if att_ind >= class_index:
                    att_ind -= 1
                class_ind = classes.index(labels[ins_ind])
                value_ind = values[att_ind].index(value)
                model_data[class_ind][att_ind][value_ind] += 1
            else:
                class_cnt[classes.index(value)] += 1

    for cid, _ in enumerate(classes):
        for aid, value in enumerate(values):
            lap = len(value)
            for vid, _ in enumerate(value):
                frequent = model_data[cid][aid][vid]
                c = class_cnt[cid]
                if laplacian:
                    frequent += 1
                    c += lap
                model_data[cid][aid][vid] = (frequent/c)

    ''' write model file'''
    with open(model_path, 'w') as fp:
        fp.write(str(attributes) + '\n')
        fp.write(str(class_index) + '\n')
        fp.write(str(classes) + '\n')
        fp.write(str(values) + '\n')
        fp.write(str(model_data) + '\n')


def main():
    try:
        _, data_path, model_path, lap = sys.argv
    except ValueError:
        data_path = "train.csv"
        model_path = "bayes.model"
        lap = True
    learner(data_path, model_path, laplacian=lap)


if __name__ == '__main__':
    main()
