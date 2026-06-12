class ArrayList:
    """Mảng động tự quản lý size/capacity."""

    def __init__(self):
        self._size = 0
        self.capacity = 10
        self.data = [None] * self.capacity

    @property
    def _capacity(self):
        return self.capacity

    @_capacity.setter
    def _capacity(self, value):
        self.capacity = value

    @property
    def _array(self):
        return self.data

    @_array.setter
    def _array(self, value):
        self.data = value

    def _resize(self, new_capacity):
        new_array = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self.data[i]
        self.data = new_array
        self.capacity = new_capacity

    def push_back(self, item):
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

    def remove_at(self, index):
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

    def get_size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def clear(self):
        self._size = 0
        self.capacity = 10
        self.data = [None] * self.capacity

    def to_list(self):
        return [self.data[i] for i in range(self._size)]

    def contains(self, item):
        return any(self.data[i] == item for i in range(self._size))

    def add(self, item):
        self.push_back(item)

    def remove(self, index):
        self.remove_at(index)

    def size(self):
        return self.get_size()

    def toString(self):
        return str(self.to_list())


DynamicArray = ArrayList
