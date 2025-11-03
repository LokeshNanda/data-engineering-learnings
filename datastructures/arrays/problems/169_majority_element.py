class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        freq = {}
        max_freq = 0
        majority_elem = 0
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
            if freq[num] > max_freq:
                max_freq = freq[num]
                majority_elem = num
        return majority_elem
    
s = Solution()
print(s.majorityElement([6,5,5]))

# This should be solved with o(1) complexity. Above solution uses o(n)

