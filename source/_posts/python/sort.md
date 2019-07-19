---
title: 排序
---

### 快速排序
```python
def quick_sort(array, left, right):
    if left < right:
        mid = partition(array, left, right)
        quick_sort(array, left, mid - 1)
        quick_sort(array, mid + 1, right)


def partition(array, left, right):
    tmp = array[left]
    while left < right:
        # 保证子序列中右边的数都比左边的大，右指针左移
        while left < right and array[right] >= tmp:
            right -= 1
        array[left] = array[right]

        # 保证子序列中左边的数都比右边的小，左指针右移
        while left < right and array[left] <= tmp:
            left += 1
        array[right] = array[left]

    array[left] = tmp
    # print(nums)
    return left

```

### 归并排序
```python
# 一次归并
def merge(array, low, mid, high):
    """
    两段需要归并的序列从左往右遍历，逐一比较，小的就放到
    tmp里去，再取，再比，再放。
    """
    tmp = []
    i = low
    j = mid + 1
    while i <= mid and j <= high:
        if array[i] <= array[j]:
            tmp.append(array[i])
            i += 1
        else:
            tmp.append(array[j])
            j += 1
    while i <= mid:
        tmp.append(array[i])
        i += 1
    while j <= high:
        tmp.append(array[j])
        j += 1
    array[low:high + 1] = tmp


def merge_sort(array, low=None, high=None):
    if low < high:
        mid = (low + high) // 2
        merge_sort(array, low, mid)
        merge_sort(array, mid + 1, high)
        merge(array, low, mid, high)
    return array
```