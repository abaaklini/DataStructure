from static_array import StaticArray, UnsortedStaticArray, SortedStaticArray

class DynamicArray(StaticArray):
  def __init__(self, initial_capacity=1):
    super().__init__(initial_capacity)
    self._capacity = initial_capacity

  def _double_array(self):
    new_array = DynamicArray(self._capacity * 2)
    
    for i in range(self._capacity):
        new_array._array[i] = self._array[i]

    self._array = new_array._array
    self._size = new_array._size
    self._capacity = new_array._capacity


  def _halve_array(self):
    new_capacity = self._capacity // 2
    new_array = DynamicArray(new_capacity)

    for i in range(new_capacity):
        new_array._array[i] = self._array[i]

    self._array = new_array._array
    self._size = new_array._size
    self._capacity = new_capacity



class UnsortedDynamicArray(UnsortedStaticArray, DynamicArray):
  def __init__(self, size):
    super().__init__(size)

  
  def insert(self, value):
    try:
      UnsortedStaticArray.insert(self, value)
    except ValueError:
      self._double_array()
      UnsortedStaticArray.insert(self, value)

  def __setitem__(self, _, value):
    self.insert(value)


  def delete(self, index):
    UnsortedStaticArray.__delitem__(self, index)

    if self._capacity > 1 and self.last <= self._capacity // 4:
      self._halve_array()


  def __delitem__(self, index):
    self.delete(index)

class SortedDynamicArray(SortedStaticArray, DynamicArray):
  def __init__(self, size):
    super().__init__(size)

  
  def insert(self, value):
    try:
      SortedStaticArray.insert(self, value)
    except ValueError:
      self._double_array()
      SortedStaticArray.insert(self, value)

  def __setitem__(self, _, value):
    self.insert(value)


  def delete(self, index):
    SortedStaticArray.__delitem__(self, index)

    if self._capacity > 1 and self.last <= self._capacity // 4:
      self._halve_array()


  def __delitem__(self, index):
    self.delete(index)
