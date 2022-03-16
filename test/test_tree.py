import unittest
from tree.node import SingleNode, GroupedNode

class TestTree(unittest.TestCase):
    def test_single_nodes(self):
        test_dict = {
            1: 2,
            2: 2,
            3: 2,
        }

        root_node = SingleNode(depth=0, predecessor=None, action='None', probability=1, board=None, value=1)
        root_node.is_root = True
        all_nodes = [root_node]

        for depth, num_nodes in test_dict.items():

            root_nodes = list(filter(lambda x: x.depth == depth - 1, all_nodes))

            for node in root_nodes:
                for node_idx in range(num_nodes):
                    all_nodes += [SingleNode(depth=depth, predecessor=node, action='Deterministic action', probability=1, board=None, value=depth * node_idx)]

        self.assertEqual(15, len(all_nodes))
        self.assertEqual(3 * 1, max(list(map(lambda x: x.value, all_nodes))))

    def test_grouped_nodes(self):
        root_node = SingleNode(depth=0, predecessor=None, action='None', probability=1, board=None, value=1)
        root_node.is_root = True
        all_nodes = [root_node]

        num_grouped_nodes = 3
        num_single_nodes_in_grouped_nodes = 3

        for _ in range(num_grouped_nodes):
            grouped_single_nodes = []
            for _ in range(num_single_nodes_in_grouped_nodes):
                grouped_single_nodes.append(SingleNode(depth=1, predecessor=None, action='Determine random action', probability=1/3, board=None, value=1))
            grouped_node = GroupedNode(depth=1, predecessor=root_node, action='Random action', nodes=grouped_single_nodes)
            all_nodes += grouped_single_nodes
            all_nodes.append(grouped_node)

        grouped_nodes = list(filter(lambda x: x.in_grouped_node, all_nodes))
        self.assertEqual(num_grouped_nodes * num_single_nodes_in_grouped_nodes, len(grouped_nodes))

        for node in grouped_nodes:
            self.assertTrue(node.ger_predecessor().is_root)








if __name__ == '__main__':
    unittest.main()
