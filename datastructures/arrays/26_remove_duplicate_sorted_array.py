'''
Standard approach using 2 pointers.
Keep lp & rp at 1 index. 
'''

class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        lp = 1
        for rp in range(1, len(nums)):
            if nums[rp] != nums[rp-1]:
                nums[lp] = nums[rp]
                lp += 1
                rp += 1
            else:
                rp += 1
        
        return lp

s = Solution()
print(s.removeDuplicates([0,0,1,1,1,2,2,3,3,4]))