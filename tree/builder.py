from tree.node import SingleNode, GroupedNode, Node
from game.game_board import GameBoard
from game.action import Action
from typing import List, Union
import numpy as np


class TreeBuilder:
    """
    This class represents the construction and search of the tree
    """
    def __init__(self, root_node: SingleNode = None):
        self.root_node = root_node
        self.to_explore_nodes: List[SingleNode, GroupedNode] = []
        self.explored_nodes = []
        if not isinstance(self.root_node, type(None)):
            self.to_explore_nodes.append(self.root_node)

    def _max_depth(self) -> int:
        return self.explored_nodes[-1].depth

    def get_node_to_expand(self) -> Union[SingleNode, GroupedNode]:
        """
        Due to breath search the next list of to_explore_nodes is treated as LIFO queue
        @return: the node which should be explored (None if there is nothing more to explore)
        """
        if len(self.to_explore_nodes) > 0:
            node_to_explore = self.to_explore_nodes.pop(0)
            self.explored_nodes.append(node_to_explore)
            return node_to_explore
        return None

    def insert_board(self, board: GameBoard, value, action: Action, predecessor_node: SingleNode):
        """
        Inserting a board/state which is deterministic
        @param board: the board which was created by the action
        @param value: the values the current board has
        @param action: the action which lead to this board/state
        @param predecessor_node: the predecessor node which lead to this node
        """
        new_node = SingleNode(depth=predecessor_node.depth + 1,
                              predecessor=predecessor_node,
                              action=action,
                              probability=1,
                              board=board,
                              value=value)

        self.to_explore_nodes.append(new_node)

    def insert_multiple_boards(self, boards: List[GameBoard], values, probabilities, action: Action, predecessor_node: SingleNode):
        """
        Inserting a list of single nodes. This usually occurs when you have a non-deterministic action.
        @param boards: list of possible boards
        @param values: list of values
        @param probabilities: list of probabilities
        @param action: the action which lead to the boards/states
        @param predecessor_node: the predecessor node
        """
        internal_nodes = []
        for board, value, probability in zip(boards, values, probabilities):
            internal_nodes.append(SingleNode(depth=predecessor_node.depth + 1,
                                             predecessor=None,
                                             action=action,
                                             probability=probability,
                                             board=board,
                                             value=value,
                                             in_grouped_node=True))

        grouped_node = GroupedNode(depth=predecessor_node.depth + 1,
                                   predecessor=predecessor_node,
                                   action=action,
                                   nodes=internal_nodes)

        self.to_explore_nodes.append(grouped_node)

    def max_max(self) -> Action:
        """
        This function is propagating the values of the explored nodes upwards to
        the nodes of depth 1 where best action will be considered.
        @return: the action with the highest value
        """
        action_nodes: List[Node] = []
        for node in list(reversed(self.to_explore_nodes)) + list(reversed(self.explored_nodes)):
            if node.depth == 1:
                action_nodes.append(node)
            elif node.depth == 0:
                continue
            node: Node
            node.predecessor.update_propagated_value(node.get_propagated_value())

        action_nodes.sort(key=lambda x: x.expected_value(), reverse=True)
        action_nodes.sort(key=lambda x: x.get_propagated_value(), reverse=True)

        return action_nodes[0].action




