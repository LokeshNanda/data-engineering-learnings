'''
o(n) using 2 pointer approach.
'''

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        maxProfit = 0
        l = 0
        for r in range(1, len(prices)):
            if prices[r] > prices[l]:
                cur_profit = prices[r] - prices[l]
                if cur_profit > maxProfit:
                    maxProfit = cur_profit
            else:
                l = r
        return maxProfit

s = Solution()
print(s.maxProfit([2,1,2,1,0,1,2]))
print(s.maxProfit([7,1,5,3,6,4]))    