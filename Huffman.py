class Huffman:
    def __init__(self, password):
        self.password = password
        self.compressed_password = ''

    def calc_incidence(self):
        characters = dict()
        for item in self.password:
            if characters.get(item) is None:
                characters[item] = 1
            else:
                characters[item] = + 1
        return characters


class Node:
    def __init__(self, incidence, character, left=None, right=None):
        self.incidence = incidence
        self.character = character
        self.left = left
        self.right = right
        self.binary = ''
