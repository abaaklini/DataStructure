import ctypes

class StaticArray:
  def __init__(self, size):
    if size <= 0:
      raise ValueError(f'Invalid array size (must be positive): {size}')
    self._size = size
    self._array = (ctypes.c_int * self._size)()

  def __getitem__(self, index):
    if index < 0 or index >= self._size:
      raise IndexError(f'Array index out of range')
    return self._array[index]

  def __setitem__(self, index, value):
    if index < 0 or index >= self._size:
      raise IndexError(f'Array index out of range')
    self._array[index] = value

  def __delitem__(self, index):
    if index < 0 or index >= self._size:
      raise ValueError(f'Index {index} out of range.')
    else:
      self._array[index] = 0

  def __repr__(self):
    temp = "|"
    for elem in self._array:
      temp += f"{elem}|"
    return temp

class UnsortedStaticArray(StaticArray):
  def __init__(self, size):
    super().__init__(size)
    self.last = 0

  def insert(self, value):
    if self.last < self._size:
      self._array[self.last] = value
      self.last += 1
    else:
      raise ValueError('The array is already full')

  def __setitem__(self, _, value):
    self.insert(value)

  def __delitem__(self, index):
    if self.last == 0:
      raise ValueError('Delete from an empty array')
    elif index < 0 or index >= self.last:
      raise ValueError(f'Index {index} out of range.')
    else:
      self._array[index] = self._array[self.last - 1]
      self._array[self.last - 1] = 0
      self.last -= 1

  def find(self, target):
    for index in range(0, self.last):
      if self._array[index] == target:
        return index
    return None

class SortedStaticArray(UnsortedStaticArray):

  def insert(self, value):
    if self.last >= self._size:
      raise ValueError(f'The array is already full, maximum size: {self._size}')
    for i in range(self.last, 0, -1):
      if self._array[i - 1] <= value:
        self._array[i] = value
        self.last += 1
        return
      else:
        self._array[i] = self._array[i - 1]
    self._array[0] = value
    self.last += 1

  def __delitem__(self, index):
    if self.last == 0:
      raise ValueError('Delete from an empty array')
    elif index < 0 or index >= self.last:
      raise ValueError(f'Index {index} out of range.')
    else:
      for i in range(index, self.last - 1):
        self._array[i] = self._array[i + 1]
      self._array[self.last - 1] = 0
      self.last -= 1

  def find(self, target):
    left = 0
    right = self.last - 1
    while left <= right:
      mid_index = (left + right) // 2
      mid_value = self._array[mid_index]
      if mid_value == target:
        return mid_index
      elif mid_value > target:
        right = mid_index - 1
      else:
        left = mid_index + 1
    return None
