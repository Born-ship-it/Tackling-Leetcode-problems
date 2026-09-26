# problems/2/2.py
"""
Add Two Numbers
"""

class Solution:
    """
    You are given two non-empty linked lists representing two non-negative integers.
    The digits are stored in reverse order, and each of their nodes contains a single digit.
    Add the two numbers and return the sum as a linked list.
    """

    def add_two_numbers(self, l1, l2):
        """
        Adds two numbers represented by linked lists.
        """

        # Reverse the input lists to get the actual numbers
        num1 = int(''.join(map(str, l1[::-1])))
        num2 = int(''.join(map(str, l2[::-1])))

        # Add the two numbers
        print(f"Adding numbers: {num1} + {num2}")
        total = num1 + num2

        # Convert the sum back to a list of digits in reverse order
        result = [int(digit) for digit in str(total)[::-1]]

        return result

class Example:
    """
    Examples for the add_two_numbers function.
    """

    def example1(self):
        """
        Example 1:
        Input: l1 = [2,4,3], l2 = [5,6,4]
        Output: [7,0,8]
        Explanation: 342 + 465 = 807.
        """

        # Input
        l1 = [2, 4, 3]
        l2 = [5, 6, 4]

        # Expected Output
        expected_output = [7, 0, 8]

        return l1, l2, expected_output

    def example2(self):
        """
        Example 2:
        Input: l1 = [0], l2 = [0]
        Output: [0]
        Explanation: 0 + 0 = 0.
        """

        # Input
        l1 = [0]
        l2 = [0]

        # Expected Output
        expected_output = [0]

        return l1, l2, expected_output

    def example3(self):
        """
        Example 3:
        Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
        Output: [8,9,9,9,0,0,0,1]
        Explanation: 9999999 + 9999 = 10009998.
        """

        # Input
        l1 = [9, 9, 9, 9, 9, 9, 9]
        l2 = [9, 9, 9, 9]

        # Expected Output
        expected_output = [8, 9, 9, 9, 0, 0, 0, 1]

        return l1, l2, expected_output

def main():
    """
    Test the add_two_numbers function with a sample input.
    """

    # Create an instance of classes
    solution = Solution()
    examples = Example()

    # Loop over the examples and test the add_two_numbers function
    for example_method in [examples.example1, examples.example2, examples.example3]:
        l1, l2, expected_output = example_method()
        result = solution.add_two_numbers(l1, l2)
        print(f"Input: l1 = {l1}, l2 = {l2}")
        print(f"Output: {result}")
        print(f"Expected Output: {expected_output}")
        print(f"Test {'Passed' if result == expected_output else 'Failed'}\n")
    
if __name__ == "__main__":
    main()
