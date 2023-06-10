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
