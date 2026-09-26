# problems/9/9.py
"""
Palindrome Number
"""

class Solution:
    """
    Given an integer `x`, return `true` if `x` is a **palindrome**, and `false` otherwise.
    """

    def solve(self, input_data, *args, **kwargs):
        """
        Main method to solve the problem.
        """

        # For palindrome need to check
        #   if the number is negative or not
        if input_data < 0:
            return False

        #   if the number is of uneven length
        elif len(str(input_data)) % 2 != 1:
            return False

        #   if the number is a palindrome
        elif str(input_data) == str(input_data)[::-1]:
            return True

        # All other cases, return False
        else:
            return False

    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------

    def helper_method(self, *args, **kwargs):
        """
        A helper method to assist in solving the problem.
        """
        pass  # Placeholder for the actual helper method implementation

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
        input_data = 121

        # Expected Output
        expected_output = True

        return input_data, expected_output

    def example2(self):
        """
        Example 2:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = -121

        # Expected Output
        expected_output = False

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
