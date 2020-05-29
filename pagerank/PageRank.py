""" PageRank implement """
from typing import Dict, Set


class Graph:
    """
    存储网页网络
    不考虑性能，只实现算法
    """

    def __init__(self):
        self.linkedNodeMap: Dict[Set[int]] = {}
        self.PRMap = {}
        self.singleNode = {}

    def addNode(self, node_id):
        if node_id not in self.linkedNodeMap:
            self.linkedNodeMap[node_id] = set()
            self.PRMap[node_id] = 0
            self.singleNode[node_id] = True
        else:
            print("节点已存在")

    def addLink(self, node1, node2):
        if node1 not in self.linkedNodeMap:
            self.addNode(node1)
        if node2 not in self.linkedNodeMap:
            self.addNode(node2)
        self.singleNode[node1] = False
        self.singleNode[node2] = False
        self.linkedNodeMap[node2].add(node1)

    def __getN(self):
        return len(self.PRMap)

    def __getNodeL(self):
        node_l = {node: 0 for node in self.PRMap}
        for in_list in self.linkedNodeMap.values():
            for in_node in in_list:
                node_l[in_node] += 1
        return node_l

    def getPR(self, epoch_num=10, q=0.85):
        page_num = self.__getN()
        node_l = self.__getNodeL()
        for i in range(epoch_num):
            for node in self.PRMap:
                self.PRMap[node] = q*sum(self.PRMap[t_node]/node_l[t_node]
                                         for t_node in self.linkedNodeMap[node]) \
                                   + q*(1 if self.singleNode[node] else 0)/page_num \
                                   + (1-q)/page_num
            print("epoch:{} PR:{}".format(i, self.PRMap))


if __name__ == '__main__':
    edges = [[1, 2], [3, 2], [3, 5], [2, 3], [3, 1], [5, 1]]
    graph = Graph()
    for edge in edges:
        graph.addLink(edge[0], edge[1])
    graph.getPR(20)

