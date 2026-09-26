# problems/1/1.py
"""
Two Sum
"""

class Solution:
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.
    """

    def two_sum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        num_dict = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_dict:
                return [num_dict[complement], i]
            num_dict[num] = i
        return []

def main():
    """
    Test the two_sum function with a sample input.
    """
    nums = [2, 7, 11, 15]
    target = 9
    solution = Solution()
    result = solution.two_sum(nums, target)
    print(f"Output: {result}")

if __name__ == "__main__":
    main()
