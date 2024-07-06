import heapq

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes

def huffman_encode(text, huffman_codes):
    return ''.join(huffman_codes[symbol] for symbol in text)

def huffman_decode(encoded_text, root):
    decoded_text = []
    node = root
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.symbol:
            decoded_text.append(node.symbol)
            node = root
    return ''.join(decoded_text)


dna_sequence = input()
freq = {}
for char in dna_sequence:
    if char in freq:
        freq[char] += 1
    else:
        freq[char] = 1

chars = list(freq.keys())
frequencies = list(freq.values())
huffman_tree = build_huffman_tree(chars, frequencies)
huffman_codes = generate_huffman_codes(huffman_tree)
encoded_text = huffman_encode(dna_sequence, huffman_codes)
decoded_text = huffman_decode(encoded_text, huffman_tree)
print((int(encoded_text), decoded_text == dna_sequence))