# Sol using o(n) & o(1) - Memory
# Reverse it | divide and then reverge again. Two Pointers - start & end
# [1,2,3,4,5,6,7] -> [7,6,5,4,3,2,1] -> [5,6,7]|[1,2,3,4]

class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums)
        l, r = 0, len(nums)-1

        def reverse_me(l, r):
            while (l < r):
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
        
        reverse_me(l, r)
        reverse_me(0, k-1)
        reverse_me(k, len(nums)-1)
        return nums
        
s = Solution()
print(s.rotate([1,2,3,4,5,6,7], 2))