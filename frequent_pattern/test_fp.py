from time import time

from fpgrowth import FP_growth
from trandataset import FrequentItemSet, read_csv
from fptree import FPTree, FPTransaction
from apriori import apriori

start = time()

dataset = read_csv('dataset/chess.dat', FPTransaction)
# print(FrequentItemSet(dataset))
total = len(dataset)
p = 0.80
print("data size:{}, min_support:{:.3f}%, support_count:{}"
      .format(total, p * 100, int(p * total)))
min_support = int(p * total)

mined_pattern = FrequentItemSet(
    FP_growth(
        FPTree.createTree(dataset, min_support),
        FPTransaction(support=0),
        min_support
    )
)
end = time()
time1 = end - start

start = time()

dataset = read_csv('dataset/chess.dat', set)
mined_pattern2 = apriori(dataset, min_support)
end = time()
time2 = end - start

print("\n\napriori: {}s".format(time2))
print(mined_pattern2)

print("\n\nFP-tree: {}s".format(time1))
print(mined_pattern)

