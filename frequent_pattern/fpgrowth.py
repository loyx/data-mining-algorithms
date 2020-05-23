""" FP growth """
from fptree import FPTree, FPTransaction


def FP_growth(tree: FPTree, itemset: FPTransaction, min_support):
    """ mining the FPTree """
    if tree.hasSinglePath():
        for tran in tree.combinations():
            yield FPTransaction.union(tran, itemset, tran.support)
        return
    for header_node in reversed(tree):
        conditional_itemset = FPTransaction.union(
            FPTransaction(header_node.tid, header_node.support),
            itemset,
            header_node.support
        )
        yield conditional_itemset
        conditional_base = []
        while header_node.next is not None:
            cond_node = header_node.next
            sub_support = cond_node.support
            sub_tran = []
            while cond_node.father.tid is not None:
                cond_node = cond_node.father
                sub_tran.append(cond_node.tid)
            conditional_base.append(FPTransaction(reversed(sub_tran), sub_support))
            header_node = header_node.next
        sub_tree = FPTree.createTree(conditional_base, min_support)
        if len(sub_tree) != 0:
            yield from FP_growth(sub_tree, conditional_itemset, min_support)
