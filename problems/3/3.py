# problems/3/3.py
"""
Longest Substring Without Repeating Characters
"""

class Solution:
    """
    Main problem-solving class.
    """

    def solve(self, string) -> int:
        """
        Given a string `s`, find the length of the **longest** **substring** without duplicate characters.
        """

        set_chars = set()
        left = 0
        max_length = 0

        print(f"Input string: {string}")
        print(f"Initial set of characters: {set_chars}")

        for i, char in enumerate(string):
            print(f"  Current set of characters: {set_chars}")
            while char in set_chars:
                set_chars.remove(string[left])
                left += 1
                print(f"    Removed character: {string[left-1]}, New left index: {left}, Current set of characters: {set_chars}")
            set_chars.add(char)
            max_length = max(max_length, i - left + 1)
            print(f"      Added character: {char}, Current set of characters: {set_chars}, Current max length: {max_length}")

        print(f"Final set of characters: {set_chars}")
        print(f"Length of the longest substring without repeating characters: {max_length}")

        return max_length

class Example:
    """
    Examples for the solve function.
    """

    def example1(self):
        """
        Example 1:
        Input: s = "abcabcbb"
        Output: 3
        Explanation: The answer is "abc", with the length of 3.
        """

        # Input
        input_data = "abcabcbb"

        # Expected Output
        expected_output = 3

        return input_data, expected_output

    def example2(self):
        """
        Example 2:
        Input: s = "bbbbb"
        Output: 1
        Explanation: The answer is "b", with the length of 1.
        """

        # Input
        input_data = "bbbbb"

        # Expected Output
        expected_output = 1

        return input_data, expected_output

def main():
    """
    Test the solve function with a sample input.
    """
    # Create an instance of the Solution class
    solution = Solution()

    # Get example input and expected output
    example = Example()

    for example_method in [example.example1, example.example2]:
        input_data, expected_output = example_method()

        # Call the solve method with the example input
        result = solution.solve(input_data)

        # Print the result and check if it matches the expected output
        print(f"Input: {input_data}")
        print(f"Output: {result}")
        print(f"Expected Output: {expected_output}")
        print(f"Test Passed: {result == expected_output}")

if __name__ == "__main__":
    main()
