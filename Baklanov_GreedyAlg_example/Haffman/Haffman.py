class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


def encode_string(string, huffman_code):
    return ''.join([huffman_code[char] for char in string])


# Input string
string = input()

# Calculating frequency
freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1

# Sorting frequency dictionary into a list of tuples
freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

# Creating nodes
nodes = freq

# Building the Huffman tree
while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

# Generating Huffman codes
huffmanCode = huffman_code_tree(nodes[0][0])

# Encoding the string
encoded_string = encode_string(string, huffmanCode)
print(encoded_string)
