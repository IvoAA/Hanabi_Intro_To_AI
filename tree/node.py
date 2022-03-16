from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np
from typing import List


class Node(ABC):
    def __init__(self, depth: int, predecessor_node, action, in_grouped_node=False):
        self.depth = depth
        self.is_root = False
        self.predecessor = predecessor_node
        self.action = action
        self.in_grouped_node = in_grouped_node

    @abstractmethod
    def expected_value(self):
        pass

    @abstractmethod
    def ger_predecessor(self) -> Node:
        pass

    def __str__(self):
        return f"Depth: {self.depth}"


class SingleNode(Node):
    def __init__(self, depth: int, predecessor, action, probability, board, value, in_grouped_node=False):
        super().__init__(depth, predecessor, action, in_grouped_node)

        self.board = board
        self.probability = probability
        self.value = value
        self.in_grouped_node = in_grouped_node

    def expected_value(self):
        return self.value

    def ger_predecessor(self) -> Node:
        if isinstance(self.predecessor, GroupedNode):
            return self.predecessor.predecessor
        else:
            return self.predecessor

    def __str__(self):
        extra_str = " [In grouped]" if self.in_grouped_node else ""
        return f"{super().__str__()} value: {self.value}" + extra_str


class GroupedNode(Node):
    def __init__(self, depth: int, predecessor, action, nodes: List[SingleNode]):
        super().__init__(depth, predecessor, action)
        self.nodes = nodes
        for node in self.nodes:
            node.predecessor = self
            node.in_grouped_node = True

        assert all(list(map(lambda x: x.depth == depth, self.nodes)))

    def expected_value(self):
        return np.array(list(map(lambda x: x.value, self.nodes))) @ np.array(list(map(lambda x: x.probability, self.nodes)))

    def ger_predecessor(self) -> Node:
        return self.predecessor

    def __str__(self):
        return f"{super().__str__()} #_nodes: {len(self.nodes)} expected_value: {self.expected_value()} "