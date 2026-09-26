# problems/6/6.py
"""
Zigzag Conversion
"""

class Solution:
    """
    The string `"PAYPALISHIRING"` is written in a zigzag pattern on a given
    number of rows like this:

    P   A   H   N
    A P L S I I G
    Y   I   R

    And then read line by line: `"PAHNAPLSIIGYIR"`

    Write the code that will take a string and make this conversion given a number of rows:

    string convert(string s, int numRows);
    """

    def solve(self, input_data, *args, **kwargs):
        """
        Main method to solve the problem.
        """

        # So we need to pass the string into a zigzag pattern
        #   and then read it line by line.


        s, num_rows = input_data      # Get string and number of rows

        # empty lists for each row
        rows = [[] for _ in range(num_rows)]
    
        # populate the column row on all rows
        # then populate the second column on the num_rows-1 row and empty the rest
        # then populate the third column on the num_rows-2 row and empty the rest
        # till num_rows-# of rows is 0 for which we will populate the whole column
        # repeat this till we reach the end of the string

        row = 0
        direction = 1  # 1 for down, -1 for up

        for char in s:
            print(f"Adding character: {char} to row: {row}")
            print(f"Current rows: {rows}")
            rows[row].append(char)
            if row == 0:
                direction = 1
            elif row == num_rows - 1:
                direction = -1
            row += direction

        print(f"Rows: {rows}")

        # Join the rows together
        result = ''.join([''.join(row) for row in rows])

        return result

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

    def example2(self):
        """
        Example 1:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = "PAYPALISHIRING", 4

        # Expected Output
        expected_output = "PINALSIGYAHRPI"

        return input_data, expected_output

    def example1(self):
        """
        Example 2:
        Input: ...
        Output: ...
        Explanation: ...
        """

        # Input
        input_data = "PAYPALISHIRING", 3

        # Expected Output
        expected_output = "PAHNAPLSIIGYIR"

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
