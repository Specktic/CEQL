from collections import Counter


class Node(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right


def huffman_tree(node, string=''):
    if type(node) == str:
        return {node: string}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_tree(l, string + '0'))
    d.update(huffman_tree(r, string + '1'))
    return d


def tree_maker(nodes):
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = Node(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


def compress(thing):
    string = thing
    frequency = dict(Counter(string))
    frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    nodes = tree_maker(frequency)
    encoding = huffman_tree(nodes)
    for character in encoding:
        print(character)
        print(encoding[character])