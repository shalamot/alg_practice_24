class DoubleHashingHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.deleted = [False] * size

    def primary_hash(self, key):
        return key % self.size

    def secondary_hash(self, key):
        return 1 + (key % (self.size - 1))

    def insert(self, key, value):
        index = self.primary_hash(key)
        step = self.secondary_hash(key)

        while self.table[index] is not None and not self.deleted[index]:
            index = (index + step) % self.size

        self.table[index] = (key, value)
        self.deleted[index] = False

    def search(self, key):
        index = self.primary_hash(key)
        step = self.secondary_hash(key)
        start_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key and not self.deleted[index]:
                return self.table[index][1]
            index = (index + step) % self.size
            if index == start_index:
                break

        return None

    def delete(self, key):
        index = self.primary_hash(key)
        step = self.secondary_hash(key)
        start_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key and not self.deleted[index]:
                self.deleted[index] = True
                return True
            index = (index + step) % self.size
            if index == start_index:
                break

        return False
