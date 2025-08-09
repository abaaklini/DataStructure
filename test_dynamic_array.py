import pytest
from dynamic_array import UnsortedDynamicArray, SortedDynamicArray

def test_unsorted_dynamic_insert_and_resize():
    arr = UnsortedDynamicArray(2)
    arr.insert(1)
    arr.insert(2)
    arr.insert(3)  # triggers resize
    assert arr._capacity == 4
    assert 3 in arr._array

def test_unsorted_dynamic_delete_and_halve():
    arr = UnsortedDynamicArray(4)
    for i in range(4):
        arr.insert(i)
    arr.delete(0)
    arr.delete(0)
    arr.delete(0)
    assert arr._capacity == 2

def test_unsorted_dynamic_setitem_and_delitem():
    arr = UnsortedDynamicArray(2)
    arr[0] = 10
    arr[1] = 20
    assert 10 in arr._array
    assert 20 in arr._array
    del arr[0]
    assert 10 not in arr._array

def test_sorted_dynamic_insert_sorted_and_resize():
    arr = SortedDynamicArray(2)
    arr.insert(5)
    arr.insert(3)
    arr.insert(7)  # triggers resize
    assert arr._capacity == 4
    active = arr._array[:arr.last]
    assert active == sorted(active)

def test_sorted_dynamic_delete_and_halve():
    arr = SortedDynamicArray(4)
    for i in [1, 2, 3, 4]:
        arr.insert(i)
    arr.delete(0)
    arr.delete(0)
    arr.delete(0)
    assert arr._capacity == 2

def test_sorted_dynamic_setitem_and_delitem():
    arr = SortedDynamicArray(2)
    arr[0] = 100
    arr[1] = 50
    assert 100 in arr._array
    assert 50 in arr._array
    del arr[0]
    assert 50 not in arr._array