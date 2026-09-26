# problems/4/4.py
"""
Median of Two Sorted Arrays
"""

class Solution:
    """
    Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively,
     return **the median** of the two sorted arrays.

    The overall run time complexity should be `O(log (m+n))`.
    """

    def solve(self, input_data, *args, **kwargs):
        """
        Main method to solve the problem.
        """

        nums1, nums2 = input_data

        nums1.extend(nums2) # Combine the two sorted arrays into one
        nums1.sort()        # Sort the combined array to find the median
        n = len(nums1)      # Length of the combined array
        if n % 2 == 1:      # If the length is odd, return the middle element
            return float(nums1[n // 2])
        else:               # If the length is even, return the average of the two middle elements
            return (nums1[n // 2 - 1] + nums1[n // 2]) / 2.0

class Example:
    """
    Examples for the solve function.
    """

    def example1(self):
        """
        Example 1:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = [1,3], [2]

        # Expected Output
        expected_output = 2.00000

        return input_data, expected_output

    def example2(self):
        """
        Example 2:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = [1,2], [3,4]

        # Expected Output
        expected_output = 2.50000

        return input_data, expected_output

def main():
    """
    Test the solve function with a sample input.
    """

    # Create an instance of the Solution class
    solution = Solution()

    # Loop over the examples and test the solve function
    examples = Example()
    for example_method in [examples.example1, examples.example2]:
        input_data, expected_output = example_method()
        result = solution.solve(input_data)
        print(f"Input: {input_data}")
        print(f"Output: {result}")
        print(f"Expected Output: {expected_output}")
        print(f"Test {'Passed' if result == expected_output else 'Failed'}\n")
    
if __name__ == "__main__":
    main()