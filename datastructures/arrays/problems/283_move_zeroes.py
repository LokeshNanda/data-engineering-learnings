'''
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
Note that you must do this in-place without making a copy of the array.

Example 1:
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:
Input: nums = [0]
Output: [0]

Approach: Two-Pointer Problem
Take Left Pointer at 0th element, Right pointer iterates from index 1,
When we find non-zero num, swap. Move left pointer by 1.
'''

class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        """
        l = 0
        for r in range(1,len(nums)):
            if nums[l] == 0 and nums[r]!= 0:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
            elif nums[l] != 0:
                l += 1        
        return nums

s = Solution()
print(s.moveZeroes([1,0,2,3]))
print(s.moveZeroes([0,0,1]))