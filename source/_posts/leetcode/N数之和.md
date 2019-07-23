---
title: N数之和
---

### 三数之和
```python
"""

    三数之和
    1. 排序
    2. 按顺序 固定一个值(这里选择从左到由)
"""
from typing import List


class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:

        nums.sort()

        length = len(nums)
        res = list()
        for k in range(length - 2):

            if nums[k] > 0:
                break
            if k > 0 and nums[k] == nums[k - 1]:
                continue

            l = k + 1
            r = length - 1

            while l < r:
                ss = nums[l] + nums[r] + nums[k]
                if ss > 0:
                    r -= 1
                    while l < r and nums[r] == nums[r+1]:
                        r -= 1
                elif ss < 0:
                    l += 1
                    while l < r and nums[l] == nums[l-1]:
                        l += 1
                else:
                    res.append([nums[k], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[r] == nums[r+1]:
                        r -= 1
                    while l < r and nums[l] == nums[l-1]:
                        l += 1
        return res


if __name__ == '__main__':
    S = Solution()
    res = S.threeSum(nums=[-1, 0, 1, 2, -1, -4])
    print(res)

```

### 四数之和
```python
"""
    
    1. 排序
    2. 固定值 两次固定
"""

class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        nums.sort()

        length = len(nums)
        res = set()

        for p in range(length - 3):

            for k in range(p + 1, length - 2):

                l = k + 1
                r = length - 1

                while l < r:
                    ss = nums[l] + nums[r] + nums[k] + nums[p]
                    if ss - target > 0:
                        r -= 1
                    elif ss - target < 0:
                        l += 1
                    else:
                        res.add((nums[p], nums[k], nums[l], nums[r]))
                        l += 1
                        r -= 1
        return [list(x) for x in res]

```