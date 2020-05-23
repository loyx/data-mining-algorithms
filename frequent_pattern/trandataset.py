""" data structure for transaction data and frequent item set"""
from itertools import combinations
from array import array
from typing import Set, List


def read_csv(path, dtype):
    """ read transaction data"""

    dataset = []
    with open(path, 'r') as fp:
        for transaction in fp.readlines():
            items = transaction.split(' ')
            if items[-1] == '\n':
                del items[-1]
            transaction = dtype(map(int, items))
            dataset.append(transaction)
    return dataset


def findFrequent1ItemSet(dataset: List[Set], support):
    """ find Frequent 1-Itemset with min support count in database"""

    item_set = {}
    for transaction in dataset:
        for item in transaction:
            try:
                item_set[item] += 1
            except KeyError:
                item_set[item] = 1
    f_set = []
    for key, value in item_set.items():
        if value >= support:
            f_set.append(Transaction(key, value))
    return FrequentItemSet(sorted(f_set))  # sort frequent itemset
    # return FrequentItemSet(f_set)


class Transaction:
    """ item set with supports count """

    typecode = 'i'
    __slots__ = ['items', 'support']

    def __init__(self, iterable, support=0):
        try:
            self.items = array(self.typecode, iterable)
        except TypeError:
            self.items = array(self.typecode, [iterable])
        self.support = support

    def __eq__(self, other):
        """ transaction can compare with all iterable data"""
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __lt__(self, other):
        if len(self) != len(other):
            raise TypeError("cannot compare")
        return all(a < b for a, b in zip(self, other))

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __repr__(self):
        msg = '(['
        for i in self:
            msg += '{},'.format(str(i))
        msg += "]:{})".format(self.support)
        return msg

    def __add__(self, other):
        """ apriori join step """
        msg = "{} cannot apriori join".format(other)

        transaction_size = len(self)
        if transaction_size != len(other):
            raise TypeError(msg)
        new_transaction = []
        for index, (it1, it2) in enumerate(zip(self, other)):
            if index == transaction_size-1:
                if it1 < it2:
                    new_transaction.extend([it1, it2])
                else:
                    raise TypeError(msg)
            elif it1 == it2:
                new_transaction.append(it1)
            else:
                raise TypeError(msg)
        return Transaction(new_transaction)

    def k1_Subset(self):
        """ get k-1 subset of transaction """
        yield from combinations(self, len(self)-1)


class FrequentItemSet:

    __slots__ = ['transactions', 'frozenTran']

    def __init__(self, transactions=None):
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = list(transactions)

    def __len__(self):
        return len(self.transactions)

    def __getitem__(self, item):
        return self.transactions[item]

    def __iadd__(self, other):
        """ set marge """
        self.transactions.extend(other.transactions)
        return self

    def __contains__(self, item):
        """ 优化 in。事实上FrequentItemSet承担了两种职责，不太好。 """
        try:
            return frozenset(item) in self.frozenTran
        except AttributeError:
            self.frozenTran = frozenset(map(frozenset, self))
            return frozenset(item) in self.frozenTran

    def __repr__(self):
        msg = 'Frequent Itemset:{'
        k_itemset = {}
        times = {}
        smsg = '\n\t{}-Itemset:  {{}} itemset\n\t\t'
        for tran in self:
            len_t = len(tran)
            try:
                k_itemset[len_t] += str(tran) + ', '
                times[len_t] += 1
            except KeyError:
                k_itemset[len_t] = smsg.format(len_t) + str(tran) + ', '
                times[len_t] = 1
        for key in sorted(k_itemset.keys()):
            msg += k_itemset[key].format(times[key])
        msg += '\n}'
        return msg

    def addTransaction(self, tran):
        self.transactions.append(tran)

    def getSubset(self, t: Set):
        """ get subset of t"""
        subset = []
        for transaction in self:
            if set(transaction) <= t:
                subset.append(transaction)
        return FrequentItemSet(subset)

    def getSubsetWithSupport(self, support):
        """ get subset of candidate with min support count"""
        subset = []
        for transaction in self:
            if transaction.support >= support:
                subset.append(transaction)
        return FrequentItemSet(subset)


if __name__ == '__main__':
    # read_csv('T10I4D100K.dat', set)
    data = read_csv('test.txt', set)
    f_1_set = findFrequent1ItemSet(data, 10)
    print(f_1_set)
