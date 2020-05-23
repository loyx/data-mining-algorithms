""" FP tree and others """
from collections.abc import Sequence
from itertools import combinations
from typing import List, Iterator, Optional
from trandataset import Transaction


class Node:
    """ FP tree's node """

    __slots__ = ['tid', 'support', 'father', 'next', 'children']

    def __init__(self, tid, support=0, father=None, next_node=None):
        self.tid = tid
        self.support = support
        self.father: Node = father
        self.next: Node = next_node
        self.children: List[Node] = []

    def __eq__(self, other):
        """ Node 可以等于任何数值或Node """
        try:
            return self.tid == other.tid
        except AttributeError:
            return self.tid == other

    def __lt__(self, other):
        return self.support < other.support

    def __repr__(self):
        msg = "Node(id:{}, sp:{}".format(self.tid, self.support)
        if self.father is not None:
            msg += ", fa:{}".format(self.father.tid)
        return msg + ')'


class FPTransaction(Transaction):
    """ Transaction 特殊化， 这样可以使用apriori中的一些function """

    __slots__ = ['items', 'support']

    def __init__(self, iterable=None, support=1):
        if iterable is None:
            iterable = []
        super().__init__(iterable, support)

    def __contains__(self, item):
        return item in self.items

    @classmethod
    def union(cls, tran_a, tran_b, support):
        return cls(tran_a.items + tran_b.items, support)


class FPTree(Sequence):  # 我有强迫症啊
    """ Frequent pattern tree """

    def __init__(self, root=None, header_table: Optional[List[Node]] = None):
        if header_table is None:
            self.headerTable = []
            self.root = Node(None)
        else:
            self.headerTable = list(header_table)
            self.root = root

    @classmethod
    def createTree(cls, condition_base: List[FPTransaction], support):
        """ create FP tree
            :param support: min support count
            :param condition_base: a list contained sorted transaction data
        """

        ''' step 1: find header table & prepare database'''
        new_header_table = cls.findHeaderTable(condition_base, support)

        def gen_transaction(sub_tran):
            """ closure  return a node in header_table"""
            for item in new_header_table:
                if item in sub_tran:
                    yield item

        ''' step 2: create FP-tree '''
        root = Node(None)
        fp_tree = cls(root, new_header_table)
        for transaction in condition_base:
            fp_tree.insertTree(gen_transaction(transaction), root, transaction.support)
        return fp_tree

    @staticmethod
    def findHeaderTable(condition_base: List[FPTransaction], support):
        """ scan the condition base find 1-item sets """
        item_set = {}
        for transaction in condition_base:
            for item in transaction:
                try:
                    item_set[item] += transaction.support
                except KeyError:
                    item_set[item] = transaction.support
        header_table = []
        for key, value in item_set.items():
            if value >= support:
                header_table.append(Node(key, value))
        return sorted(header_table, reverse=True)

    def insertTree(self, tran: Iterator, father: Node, support=1):
        """ insert new Node into this tree after particular Node"""
        try:
            t_node: Node = next(tran)
        except StopIteration:
            return
        for child in father.children:
            if child == t_node:
                child.support += support
                self.insertTree(tran, child, support)
                return
        new_node = Node(t_node.tid, support, father, None)
        father.children.append(new_node)

        # while t_node.next is not None:
        #     t_node = t_node.next
        # t_node.next = new_node
        new_node.next = t_node.next
        t_node.next = new_node
        self.insertTree(tran, new_node, support)
        return

    def hasSinglePath(self):
        """ if the tree contains a single path """
        for header_node in self.headerTable:
            if header_node.next.next is not None:
                return False
        return True

    def combinations(self) -> FPTransaction:
        """ combination the node in the tree """
        length = len(self)
        while length != 0:
            for nodes in combinations(self, length):
                ids = list(map(lambda x: x.tid, nodes))
                support = min(map(lambda x: x.support, nodes))
                yield FPTransaction(ids, support)
            length -= 1

    def __len__(self):
        return len(self.headerTable)

    def __getitem__(self, item):
        """ traver the header tree """
        return self.headerTable[item]

    def __repr__(self):
        return str(self.headerTable)

    def __iter__(self):
        """ iter the header tree """
        for header_node in self.headerTable:
            yield header_node
