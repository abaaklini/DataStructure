import os
import sys
import pytest
from static_array import StaticArray, UnsortedStaticArray, SortedStaticArray


def test_static_array_get_set_and_bounds():
    a = StaticArray(3)
    assert [a[i] for i in range(3)] == [0, 0, 0]

    a[0] = 10
    a[2] = 20
    assert a[0] == 10
    assert a[1] == 0
    assert a[2] == 20

    with pytest.raises(IndexError):
        _ = a[3]
    with pytest.raises(IndexError):
        _ = a[-1]
    with pytest.raises(IndexError):
        a[3] = 1
    with pytest.raises(IndexError):
        a[-1] = 1

    # Base delete zeroes the slot and uses ValueError for out-of-range
    a[1] = 5
    del a[1]
    assert a[1] == 0
    with pytest.raises(ValueError):
        del a[-1]
    with pytest.raises(ValueError):
        del a[3]


def test_unsorted_insert_setitem_overflow_and_delete():
    u = UnsortedStaticArray(3)
    u.insert(5)
    u.insert(7)
    u.insert(9)
    assert u.last == 3
    assert [u._array[i] for i in range(3)] == [5, 7, 9]

    with pytest.raises(ValueError):
        u.insert(10)

    # __setitem__ appends (ignores index)
    v = UnsortedStaticArray(2)
    v[999] = 1
    v[123] = 2
    assert v.last == 2
    assert sorted([v._array[i] for i in range(v.last)]) == [1, 2]

    # Delete from empty
    w = UnsortedStaticArray(1)
    with pytest.raises(ValueError):
        del w[0]

    # Delete replaces with last element
    x = UnsortedStaticArray(4)
    for val in [1, 2, 3]:
        x.insert(val)
    # Before: [1,2,3,0], last=3
    del x[0]
    # After: [3,2,0,0], last=2
    assert x.last == 2
    assert [x._array[i] for i in range(4)] == [3, 2, 0, 0]


def test_unsorted_find():
    u = UnsortedStaticArray(5)
    for val in [4, 1, 7, 1]:
        u.insert(val)
    idx = u.find(1)
    assert idx in (1, 3)  # first occurrence is 1 by current implementation
    assert u._array[idx] == 1
    assert u.find(99) is None


def test_sorted_insert_order_and_overflow():
    s = SortedStaticArray(5)
    for val in [3, 1, 2, 2]:
        s.insert(val)
    # Active portion must be sorted non-decreasing
    active = [s._array[i] for i in range(s.last)]
    assert active == [1, 2, 2, 3]
    # Zeros after last
    tail = [s._array[i] for i in range(s.last, s._size)]
    assert all(v == 0 for v in tail)

    with pytest.raises(ValueError):
        s.insert(10)
        s.insert(11)


def test_sorted_delete_and_find():
    s = SortedStaticArray(5)
    for val in [1, 2, 3]:
        s.insert(val)
    del s[1]  # delete value 2
    assert s.last == 2
    assert [s._array[i] for i in range(5)] == [1, 3, 0, 0, 0]

    for val in [1, 2, 3]:
        s.insert(val)
    # Now s contains [1,1,2,3,3] (depending on order after re-inserts)
    idx = s.find(2)
    assert idx is not None and 0 <= idx < s.last and s._array[idx] == 2
    assert s.find(99) is None