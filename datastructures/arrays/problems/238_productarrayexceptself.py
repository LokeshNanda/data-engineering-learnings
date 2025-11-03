# [1,2,3,4]
# [24,12,8,6]
# Prefix | Postfix approach
# Go from left to right & store num , multiply it with prefix
# Go back from right to left - store then multiply with existing prefix and new sum

class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        res = [1] * len(nums)
        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *= nums[i]
        
        postfix = 1
        for i in range(len(nums)-1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        
        return res

s = Solution()
print(s.productExceptSelf([1,2,3,4]))