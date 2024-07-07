import math

class Node:
    def __init__(self, array_size=4):
        self.array = [None] * array_size
        self.len = 0
        self.next = None

def calculate_optimal_node_size(num_elements):
    bytes_per_element = 4
    total_bytes = num_elements * bytes_per_element
    min_cache_line_size = 64
    cache_lines_needed = math.ceil(total_bytes / min_cache_line_size)
    optimal_node_size = cache_lines_needed + 1
    return optimal_node_size

class UnrolledLinkedList:
    def __init__(self, array_size=4, num_elements=0):
        if num_elements > 0:
            array_size = calculate_optimal_node_size(num_elements)
        array_size = array_size if array_size > 0 else 4
        self.head = None
        self.len = 0
        self.array_size = array_size
        self.nodes_info = {}

    def insert(self, value, index=None):
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")

        if index is not None and (index[0] >= self.len or index[1] >= self.array_size):
            return False

        if not self.head:
            self.head = Node(self.array_size)
            self.head.array[0] = value
            self.head.len += 1
            self.nodes_info[0] = 1
        else:
            cur_node = self.head
            node_index = 0
            if index is not None:
                node_index, pos = index
                for _ in range(node_index):
                    cur_node = cur_node.next
                cur_node.array.insert(pos, value)
                cur_node.array.pop()
            else:
                node_index, pos = self.find_first_fit()
                cur_node = self.head
                for _ in range(node_index):
                    cur_node = cur_node.next
                cur_node.array.insert(pos, value)
                cur_node.array.pop()
                cur_node.len += 1

            self.rebalance(cur_node, node_index)

        self.len += 1
        return True

    def find_first_fit(self):
        cur_node = self.head
        node_index = 0
        while cur_node:
            if cur_node.len < self.array_size:
                return (node_index, cur_node.len)
            cur_node = cur_node.next
            node_index += 1
        return (node_index - 1, self.array_size)

    def search(self, value):
        if not self.head:
            return False

        cur_node = self.head
        node_index = 0
        while cur_node:
            try:
                pos = cur_node.array.index(value)
                return (node_index, pos)
            except ValueError:
                cur_node = cur_node.next
                node_index += 1

        return False

    def remove_by_index(self, index):
        if index[0] >= self.len or index[1] >= self.array_size:
            return False
        cur_node = self.head
        prev_node = None
        node_index, pos = index
        for _ in range(node_index):
            prev_node = cur_node
            cur_node = cur_node.next

        cur_node.array.pop(pos)
        cur_node.len -= 1
        cur_node.array.append(None)
        if cur_node.len == 0:
            if prev_node:
                prev_node.next = cur_node.next
            else:
                self.head = cur_node.next
            del self.nodes_info[node_index]
        else:
            self.nodes_info[node_index] = cur_node.len

        self.len -= 1
        self.rebalance(cur_node, node_index)
        return True

    def remove_by_value(self, value):
        if not self.head:
            return False

        cur_node = self.head
        prev_node = None
        node_index = 0
        removed = False

        while cur_node:
            while value in cur_node.array:
                pos = cur_node.array.index(value)
                self.remove_by_index((node_index, pos))
                removed = True
            prev_node = cur_node
            cur_node = cur_node.next
            node_index += 1

        return removed

    def rebalance(self, node, node_index):
        while node and node.len > self.array_size:
            new_node = Node(self.array_size)
            split_index = self.array_size // 2
            new_node.array = node.array[split_index:] + [None] * (self.array_size - len(node.array[split_index:]))
            node.array = node.array[:split_index] + [None] * (self.array_size - len(node.array[:split_index]))
            node.len = split_index
            new_node.len = self.array_size - split_index
            new_node.next = node.next
            node.next = new_node
            node = new_node
            node_index += 1
            self.nodes_info[node_index] = new_node.len

    def print(self):
        cur_node = self.head
        node_index = 0
        while cur_node:
            print(f"Node {node_index}: {' '.join(str(i) for i in cur_node.array if i is not None)}")
            cur_node = cur_node.next
            node_index += 1


num_elements = 100000
ull = UnrolledLinkedList(num_elements=num_elements)
for i in range(1, 1000001):
    ull.insert(i)
ull.print()
print("Search for 30:", ull.search(30))
print("Remove by value 10:", ull.remove_by_value(10))
ull.print()
