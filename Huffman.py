from collections import Counter


class Compressor:
    def huffman_tree(self, node, string=''):
        if type(node) == str:
            return {node: string}
        (l, r) = node.children()
        d = dict()
        d.update(self.huffman_tree(l, string + '0'))
        d.update(self.huffman_tree(r, string + '1'))
        return d

    def tree_maker(self, nodes):
        while len(nodes) > 1:
            (key1, c1) = nodes[-1]
            (key2, c2) = nodes[-2]
            nodes = nodes[:-2]
            node = Node(key1, key2)
            nodes.append((node, c1 + c2))
            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        return nodes[0][0]

    def compress(self, thing):
        string = thing
        frequency = dict(Counter(string))
        frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        nodes = self.tree_maker(frequency)
        encoding = self.huffman_tree(nodes)
        for character in encoding:
            print(character)
            print(encoding[character])


class Node(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right
