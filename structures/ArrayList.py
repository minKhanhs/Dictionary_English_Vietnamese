class ArrayList:
    """Mảng động tự quản lý size/capacity."""

    def __init__(self):
        self._size = 0
        self.capacity = 10
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_array = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self.data[i]
        self.data = new_array
        self.capacity = new_capacity

    def add(self, item):
        if self._size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self._size] = item
        self._size += 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        return self.data[index]

    def set(self, index, item):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        self.data[index] = item

    def remove(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        removed = self.data[index]
        for i in range(index, self._size - 1):
            self.data[i] = self.data[i + 1]
        self.data[self._size - 1] = None
        self._size -= 1
        if 0 < self._size < self.capacity // 4:
            self._resize(max(10, self.capacity // 2))
        return removed

    def getSize(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    def clear(self):
        self._size = 0
        self.capacity = 10
        self.data = [None] * self.capacity

    def toList(self):
        return [self.data[i] for i in range(self._size)]

    def contains(self, item):
        return any(self.data[i] == item for i in range(self._size))


DynamicArray = ArrayList
