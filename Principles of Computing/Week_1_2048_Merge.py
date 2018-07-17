"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    non_zero_line = []
    result = []
    is_appended = False
    # imitate slide without merging
    for number in line:
        if number != 0:
            non_zero_line.append(number)
    # merging
    for element in range(len(non_zero_line)):
        if is_appended:
            is_appended = False
        else:
            if element == len(non_zero_line) - 1:
                result.append(non_zero_line[element])
            else:
                if non_zero_line[element] == non_zero_line[element + 1]:
                    result.append(non_zero_line[element] + non_zero_line[element + 1])
                    is_appended = True
                else:
                    result.append(non_zero_line[element])
                    is_appended = False
    result.extend([0] * (len(line) - len(result)))
    return result