#Cấu trúc ArrayList

class ArrayList:
    def __init__(self):
        self._size = 0
        self._capacity = 10
        self._array = [None] * self._capacity

    def _resize(self, new_capacity):
        new_array = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    def add(self, item):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._array[self._size] = item
        self._size += 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        return self._array[index]

    def remove(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        self._array[self._size - 1] = None
        self._size -= 1
        if 0 < self._size < self._capacity // 4:
            self._resize(self._capacity // 2)

    def contains(self, item):
        for i in range(self._size):
            if self._array[i] == item:
                return True
        return False

    def size(self):
        return self._size

    def toString(self):
        return str([self.get(i) for i in range(self._size)])