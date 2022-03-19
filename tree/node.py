from __future__ import annotations
import sys
from abc import ABC, abstractmethod
import numpy as np
from typing import List


class Node(ABC):
    """
    An abstract class which is a main component of the search tree.
    """
    def __init__(self, depth: int, predecessor_node, action, in_grouped_node=False):
        self.depth = depth
        self.is_root = False
        self.predecessor = predecessor_node
        self.action = action
        self.in_grouped_node = in_grouped_node
        self.explored = False
        self.propagated_value = 0

    @abstractmethod
    def expected_value(self):
        """
        @return: The expected value of a node, which depends on the kind of node
        """
        pass

    @abstractmethod
    def get_predecessor(self) -> Node:
        """
        @return: the predecessor of the current node. Different behaviour for each kind of node
        """
        pass

    def was_explored(self):
        self.explored = True

    def update_propagated_value(self, new_value: float):
        self.propagated_value = max(self.propagated_value, new_value)

    def get_propagated_value(self):
        """
        The propagated value which is either the propagated value or the expected value if there was no propagated value
         (aka if the node is a leave)
        @return: The propagated value
        """
        return self.propagated_value if self.propagated_value != 0 else self.expected_value()

    def __str__(self):
        return f"Depth: {self.depth} Prop: {self.get_propagated_value()} Action: {self.action}"


class SingleNode(Node):
    """
    A single node which usually represents an OR node.
    """
    def __init__(self, depth: int, predecessor, action, probability, board, value, in_grouped_node=False):
        """
        Initialization of a Single Node
        @param depth: current depth this node is at
        @param predecessor: the predecessor (None if this is the root)
        @param action: the action which lead to the node/state
        @param probability: the probability of this action happening (1.0 for deterministic actions)
        @param board: the board which represents the current state
        @param value: the value of this state
        @param in_grouped_node: boolean value if this node is part of a GroupedNode (aka. if it is part of a AND node)
        """
        super().__init__(depth, predecessor, action, in_grouped_node)

        self.board = board
        self.probability = probability
        self.value = value
        self.in_grouped_node = in_grouped_node

    def expected_value(self):
        return self.value

    def get_predecessor(self) -> Node:
        """
        If the SingleNode is in a GroupedNode, the predecessor of him is not the GroupedNode,
        it is the predecessor of the GroupedNode
        @return:
        """
        if isinstance(self.predecessor, GroupedNode):
            return self.predecessor.predecessor
        else:
            return self.predecessor

    def __str__(self):
        extra_str = " [In grouped]" if self.in_grouped_node else ""
        return f"{super().__str__()} value: {self.value}" + extra_str


class GroupedNode(Node):
    """
    A Grouped node which usually represents an AND node. This node can contain multiple single nodes!
    """
    def __init__(self, depth: int, predecessor, action, nodes: List[SingleNode]):
        """
        @param depth: current depth this node is at
        @param predecessor: the predecessor (None if this is the root)
        @param action: the action which lead to the node/state
        @param nodes: the list of single nodes which are contained inside this grouped node
        """
        super().__init__(depth, predecessor, action)
        self.nodes = nodes
        for node in self.nodes:
            node.predecessor = self
            node.in_grouped_node = True

        assert all(list(map(lambda x: x.depth == depth, self.nodes)))

    def expected_value(self):
        """
        The expected value is calculated as inner product of the nodes values and the nodes probabilities
        @return: the expected value
        """
        return np.array(list(map(lambda x: x.value, self.nodes))) @ np.array(list(map(lambda x: x.probability, self.nodes)))

    def get_predecessor(self) -> Node:
        return self.predecessor

    def get_propagated_value(self):
        """
        The propagated value is calculated as inner product of the nodes propagated values and the nodes probabilities
        @return: The __expected__ propagated value
        """
        return np.array(list(map(lambda x: x.get_propagated_value(), self.nodes))) @ np.array(list(map(lambda x: x.probability, self.nodes)))

    def __str__(self):
        return f"{super().__str__()} #_nodes: {len(self.nodes)} expected_value: {self.expected_value()} "