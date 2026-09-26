# problems/5/5.py
"""
Longest Palindromic Substring
"""

class Solution:
    """
    Given a string `s`, return *the longest* *palindromic* *substring* in `s`.
    """

    def solve(self, input_data, *args, **kwargs):
        """
        Main method to solve the problem.
        """

        s = input_data

        longest = ""
        for i in range(len(s)):
            # Check for odd-length palindromes
            odd = self.expand_around_center(s, i, i)
            # Check for even-length palindromes
            even = self.expand_around_center(s, i, i + 1)
            # Update the longest palindrome found so far
            if len(odd) > len(longest):
                longest = odd
            if len(even) > len(longest):
                longest = even

        return longest  # Placeholder for the actual solution implementation

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------

    def is_palindrome(self, s: str) -> bool:
        """
        Check if a given string `s` is a palindrome.
        """
        return s == s[::-1]

    def expand_around_center(self, s: str, left: int, right: int) -> str:
        """
        Expand around the center and return the longest palindromic substring.
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        return s[left + 1:right]

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
        input_data = "babad"

        # Expected Output
        expected_output = "bab"

        return input_data, expected_output

    def example2(self):
        """
        Example 2:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = "cbbd"

        # Expected Output
        expected_output = "bb"

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
