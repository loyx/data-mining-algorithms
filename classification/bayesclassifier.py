""" naive bayesia nclassifier """
import sys

from util import *


def classifier(model_path, test_path, result_path, class_index=-1):
    with open(model_path, "r") as fp:
        lines = fp.readlines()
        attributes = eval(lines[0].strip())
        train_class_index = eval(lines[1].strip())
        classes = eval(lines[2].strip())
        values = eval(lines[3].strip())
        model_data = eval(lines[4].strip())

    test_data = list(csvReader(test_path))

    if class_index == -1:
        class_index = len(test_data[0]) - 1
    if class_index != train_class_index:
        raise Exception("标签属性不一致")

    for instance in test_data[1:]:
        max_post_hyp = -1
        g_label = ""
        for cid, label in enumerate(classes):
            post_hyp = 1
            for index, value in enumerate(instance):
                if index != class_index:
                    aid = attributes.index(test_data[0][index])
                    vid = values[aid].index(value)
                    post_hyp *= model_data[cid][aid][vid]
            if post_hyp > max_post_hyp:
                max_post_hyp = post_hyp
                g_label = label
        instance[class_index] = g_label

    csvWriter(test_data, result_path)


def main():
    try:
        _, model_path, test_path, result_path = sys.argv
    except ValueError:
        model_path = "bayes.model"
        test_path = "test.csv"
        result_path = "result.csv"
    classifier(model_path, test_path, result_path)


if __name__ == '__main__':
    main()
