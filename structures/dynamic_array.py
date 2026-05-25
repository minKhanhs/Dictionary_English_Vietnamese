class DynamicArray:
    """Dynamic array that manages size and capacity explicitly."""

    def __init__(self, capacity=4):
        self.capacity = max(1, int(capacity))
        self.size = 0
        self.data = [None] * self.capacity

    def push_back(self, item):
        if self.size >= self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = item
        self.size += 1

    def get(self, index):
        self._check_index(index)
        return self.data[index]

    def set(self, index, item):
        self._check_index(index)
        self.data[index] = item

    def remove_at(self, index):
        self._check_index(index)
        removed = self.data[index]
        for current in range(index, self.size - 1):
            self.data[current] = self.data[current + 1]
        self.size -= 1
        self.data[self.size] = None
        return removed

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def clear(self):
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for index in range(self.size):
            new_data[index] = self.data[index]
        self.capacity = new_capacity
        self.data = new_data

    def to_list(self):
        return [self.data[index] for index in range(self.size)]

    def _check_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
