# problems/10/10.py
"""
Regular Expression Matching
"""

class Solution:
    """
    Given an input string `s` and a pattern `p`, implement regular expression matching with support for `'.'` and `'*'` where:

    - `'.'` Matches any single character.​​

    - `'*'` Matches zero or more of the preceding element.

    Return a boolean indicating whether the matching covers the entire input string (not partial).
    """

    def solve(self, input_data, *args, **kwargs):
        """
        Main method to solve the problem.
        """

        s, p = input_data

        # If the string s is mathed covered by the pattern p,
        #  return True; otherwise, return False

        # Check if empty
        if not p:
            return not s
        if not s:
            return all(x == '*' for x in p[1::2])

        # Check if the first character matches
        first_match = bool(s) and p[0] in {s[0], '.'}

        # If the pattern has a '*' as the second character
        if len(p) >= 2 and p[1] == '*':
            # Two cases:
            # 1. We can ignore the '*' and the preceding character in the pattern
            # 2. If the first character matches, we can move to the next character in the string
            return (self.solve((s, p[2:])) or
                    (first_match and self.solve((s[1:], p))))
        else:
            print(f"Input string: {s}, Pattern: {p}, First match: {first_match}")
            # If the first character matches, move to the next character in both the string and the pattern
            return first_match and self.solve((s[1:], p[1:]))



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
        input_data = "a", "."

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
        input_data = "aa", ".*"

        # Expected Output
        expected_output = True

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
